""" Initialize Delivery Boy Bill """

from odoo import _, api, fields, models


class DeliveryBoyBill(models.TransientModel):
    """
        Initialize Delivery Boy Bill:
         -
    """
    _name = 'delivery.boy.bill'
    _description = 'Delivery Boy Bill'

    account_move_ids = fields.Many2many(
        'account.move'
    )
    delivery_boy_id = fields.Many2one(
        'res.users', readonly=True

    )
    commission_fees = fields.Float(
        related='delivery_boy_id.commission_fees',
        readonly=True
    )
    amount_total = fields.Float(
        compute='_compute_amount_total', store=True
    )
    commission_amount = fields.Float(
        compute='_compute_commission_amount', store=True
    )

    @api.depends('amount_total')
    def _compute_commission_amount(self):
        """ Compute commission_amount value """
        for rec in self:
            rec.commission_amount = (
                    rec.amount_total * rec.commission_fees / 100)

    @api.depends('account_move_ids')
    def _compute_amount_total(self):
        """ Compute amount_total value """
        for rec in self:
            if rec.account_move_ids:
                amount_total = 0
                for order in rec.account_move_ids:
                    amount_total += sum(order.invoice_line_ids.filtered(lambda
                                                                            r: r.product_id.id == self.env.company.delivery_product_id.id).mapped(
                        'price_subtotal'))
                rec.amount_total = amount_total

    def create_delivery_boy_bill(self):
        """ Create Vendor Bill for delivery boy orders with commission fees"""
        product_id = self.env.company.delivery_product_id
        account_move_id = self.env['account.move'].create(
            {
                'partner_id': self.delivery_boy_id.partner_id.id,
                'move_type': 'in_invoice',
                'invoice_date': fields.Date.today(),
                'delivery_boy_bill': True,
                'invoice_origin':
                    f"Commission Fees({self.account_move_ids.mapped('name')}",
                'invoice_line_ids': [(0, 0, {
                    'product_id': product_id.id,
                    'account_id':
                        product_id.categ_id.property_account_income_categ_id.id,
                    'name': product_id.name,
                    'price_unit': self.commission_amount,
                    'quantity': 1,
                })],
            }
        )
        account_move_id.action_post()
        self.account_move_ids.write({'delivery_billed': True})
        if self._context.get('view_bill') == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Vendor Bill'),
                'res_model': 'account.move',
                'view_mode': 'form',
                'context': {'delivery_invoice': 0},
                'res_id': account_move_id.id,
                'views': [[False, 'form']]
            }
