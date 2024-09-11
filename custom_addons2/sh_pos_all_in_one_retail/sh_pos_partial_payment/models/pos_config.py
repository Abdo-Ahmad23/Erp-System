# Copyright (C) Softhealer Technologies.
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_round

from odoo import fields, models, api, _


class PosSession(models.Model):
    _inherit = 'pos.session'

    def get_closing_control_data(self):
        data = super(PosSession, self).get_closing_control_data()
        cash_payment_method_ids = self.payment_method_ids.filtered(lambda pm: pm.type == 'cash')
        default_cash_payment_method_id = cash_payment_method_ids[0] if cash_payment_method_ids else None

        other_payments = self.env['pos.payment'].search(
            [('session_id', '!=', self.id), ('pos_session_id', '=', self.id)])

        total_default_cash_payment_amount_other = 0

        if other_payments:
            total_default_cash_payment_amount_other = sum(
                other_payments.filtered(lambda p: p.payment_method_id == default_cash_payment_method_id).mapped(
                    'amount')) if default_cash_payment_method_id else 0

        if data and data.get('default_cash_details') and data.get('default_cash_details').get('amount'):
            data['default_cash_details']['amount'] = data['default_cash_details'][
                                                         'amount'] + total_default_cash_payment_amount_other
        return data


class PosPayment(models.Model):
    _inherit = 'pos.payment'

    pos_session_id = fields.Many2one('pos.session', string="Session")


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_partial_payment = fields.Boolean("Allow Partial Payment")
    sh_allow_to_pay_order = fields.Boolean(string="Allow To Pay Order")

    sh_partial_pay_product_id = fields.Many2one('product.product', string="Partial Pay Product")

    @api.onchange('sh_allow_to_pay_order')
    def _onchange_sh_allow_to_pay_order(self):
        if self.sh_allow_to_pay_order:
            product = self.env['product.product'].sudo().search([('sh_is_partial_pay_product', '=', True)], limit=1)
            if product:
                self.sh_partial_pay_product_id = product.id


class ResPartner(models.Model):
    _inherit = 'res.partner'

    not_allow_partial_payment = fields.Boolean("Not Allow Partial Payment")


class PosOrder(models.Model):
    _inherit = 'pos.order'

    sh_amount_residual = fields.Monetary(string='Amount Due',
                                         compute='_compute_amount')

    def action_pos_order_paid(self):
        self.ensure_one()

        # TODO: add support for mix of cash and non-cash payments when both cash_rounding and only_round_cash_method are True
        if not self.config_id.cash_rounding \
                or self.config_id.only_round_cash_method \
                and not any(p.payment_method_id.is_cash_count for p in self.payment_ids):
            total = self.amount_total
        else:
            total = float_round(self.amount_total, precision_rounding=self.config_id.rounding_method.rounding,
                                rounding_method=self.config_id.rounding_method.rounding_method)

        isPaid = float_is_zero(total - self.amount_paid, precision_rounding=self.currency_id.rounding)
        if self and self.state == 'on_hold':
            if not isPaid and not self.config_id.cash_rounding:
                raise UserError(_("Order %s is not fully paid.", self.name))
            elif not isPaid and self.config_id.cash_rounding:
                currency = self.currency_id
                if self.config_id.rounding_method.rounding_method == "HALF-UP":
                    maxDiff = currency.round(self.config_id.rounding_method.rounding / 2)
                else:
                    maxDiff = currency.round(self.config_id.rounding_method.rounding)

                diff = currency.round(self.amount_total - self.amount_paid)
                if not abs(diff) <= maxDiff:
                    raise UserError(_("Order %s is not fully paid.", self.name))
        self.write({'state': 'paid'})

        return True

    def _compute_amount(self):
        for each in self:
            if each.amount_paid < each.amount_total:
                each.sh_amount_residual = each.amount_total - each.amount_paid
            else:
                each.sh_amount_residual = 0.00

    @api.model
    def _process_order(self, order, draft, existing_order):
        order_id = super(PosOrder, self)._process_order(
            order, draft, existing_order)
        if order_id:
            order_obj = self.env['pos.order'].search([('id', '=', order_id)])
            if order_obj and order_obj.to_invoice and not order_obj.account_move:
                order_obj.action_pos_order_invoice()

        return order_id

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        data = super(PosOrder, self)._payment_fields(
            order, ui_paymentline)
        data['pos_session_id'] = ui_paymentline['pos_session_id']
        return data

    def _process_payment_lines(self, pos_order, order, pos_session, draft):
        """Create account.bank.statement.lines from the dictionary given to the parent function.

        If the payment_line is an updated version of an existing one, the existing payment_line will first be
        removed before making a new one.
        :param pos_order: dictionary representing the order.
        :type pos_order: dict.
        :param order: Order object the payment lines should belong to.
        :type order: pos.order
        :param pos_session: PoS session the order was created in.
        :type pos_session: pos.session
        :param draft: Indicate that the pos_order is not validated yet.
        :type draft: bool.
        """
        prec_acc = order.pricelist_id.currency_id.decimal_places

        for payments in pos_order['statement_ids']:
            if order.session_id.id != pos_session.id:
                payments[2]['pos_session_id'] = pos_session.id
            else:
                payments[2]['pos_session_id'] = order.session_id.id
            order.add_payment(self._payment_fields(order, payments[2]))

        order.amount_paid = sum(order.payment_ids.mapped('amount'))

        if not draft and not float_is_zero(pos_order['amount_return'], prec_acc):
            cash_payment_method = pos_session.payment_method_ids.filtered('is_cash_count')[:1]
            if not cash_payment_method:
                raise UserError(_("No cash statement found for this session. Unable to record returned cash."))
            return_payment_vals = {
                'name': _('return'),
                'pos_order_id': order.id,
                'amount': -pos_order['amount_return'],
                'payment_date': fields.Datetime.now(),
                'payment_method_id': cash_payment_method.id,
                'is_change': True,
            }
            order.add_payment(return_payment_vals)

    @api.model
    def create_from_ui(self, orders, draft=False):
        existing_return_order = []
        for order in orders:
            existing_order = False
            if 'server_id' in order['data']:
                existing_order = self.env['pos.order'].search(
                    ['|', ('id', '=', order['data']['server_id']), ('pos_reference', '=', order['data']['name'])],
                    limit=1)
                if existing_order:
                    existing_return_order.append(
                        {'id': existing_order.id, 'pos_reference': existing_order.pos_reference})
                    pos_session = self.env['pos.session'].browse(order['data']['pos_session_id'])
                    self._process_payment_lines(order['data'], existing_order, pos_session, draft)

                    if existing_order and existing_order.to_invoice:
                        existing_order._apply_invoice_payments()

                    existing_order.action_pos_order_paid()
                    if existing_order and existing_order.to_invoice:
                        existing_order.write({'state': 'invoiced'})

        order_id = super(PosOrder, self).create_from_ui(orders, draft=False)
        if existing_return_order and len(existing_return_order) > 0:
            for each_existing_return_order in existing_return_order:
                order_id.append(each_existing_return_order)
        return order_id


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sh_is_partial_pay_product = fields.Boolean('Partial Pay Product')
