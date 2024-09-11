""" Initialize Account Move """

from odoo.exceptions import ValidationError

from odoo import _, api, fields, models


class AccountMove(models.Model):
    """ inherit Account Move """
    _inherit = 'account.move'

    delivery_state = fields.Selection(
        [('delivery_invoices', 'Invoices'),
         ('delivery_assigned', 'Delivery Assigned'),
         ('delivery_on_way', 'Delivery On Way'),
         ('delivery_arrived', 'Delivery Arrived'),
         ('delivery_collection', 'Delivery Collection'),
         ('delivery_canceled', 'Canceled'),
         ], tracking=True
    )

    delivery_boy_id = fields.Many2one(
        'res.users', readonly=True
    )
    
    mobile = fields.Char(
        related='delivery_boy_id.mobile', string='Mobile', readonly=True
    )
    transportation = fields.Selection(
        [('car', 'Car'), ('motorcycle', 'Motorcycle'), ('bike', 'Bike')],
        readonly=True
    )
    send_date = fields.Datetime(
        readonly=True, tracking=True
    )
    arrived_date = fields.Datetime(
        readonly=True, tracking=True
    )
    delivery_billed = fields.Boolean()
    delivery_boy_bill = fields.Boolean()
    call_center_done = fields.Boolean(
        compute='_compute_call_center_done', store=True,string='Done'
    )
    
    number_copy = fields.Integer(default= 1, store=True)

    paid = fields.Float(string='Paid',compute="_compute_paid_value", currency_field='company_currency_id',digits=(6, 2))
    @api.depends('state', 'payment_state')
    def _compute_call_center_done(self):
        """ Compute call_center_done value """
        print(self.delivery_boy_id)
        for rec in self:
            if rec.state == 'posted' and rec.payment_state in ['paid',
                                                               'in_payment']:
                rec.call_center_order_id.state = 'done'
            rec.call_center_done = True

    def assign_delivery_boy(self):
        """Return Action To Assign Delivery BoyAssign Delivery Boy"""
        orders = self.get_active_ids()
        if any(rec.delivery_state != 'delivery_invoices' for rec in orders):
            raise ValidationError(
                _('You can not assign orders not in status  delivery invoice'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assign To'),
            'res_model': 'assign.delivery.boy',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_account_move_ids': [(6, 0, orders.ids)],
            },
            'views': [[False, 'form']]
        }

    def create_delivery_boy_bill(self):
        """Return Action To Create Delivery Boy  Bill"""
        orders = self.get_active_ids()
        if len(orders.mapped('delivery_boy_id')) != 1:
            raise ValidationError(
                _('Please Select Orders With Same Delivery Boy'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vendor Bill Info'),
            'res_model': 'delivery.boy.bill',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_account_move_ids': [(6, 0, orders.ids)],
                'default_delivery_boy_id': orders.mapped('delivery_boy_id').id,
            },
            'views': [[False, 'form']]
        }

    def get_active_ids(self):
        active_ids = self.env.context.get('active_ids')
        orders = self.browse(active_ids)
        if len(orders) > 200:
            raise ValidationError(
                _('cannot assign more than 200 orders per time')
            )
        return orders

    def delivery_on_way(self):
        """ Delivery In Way """
        self.send_date = fields.Datetime.now()
        self.delivery_state = 'delivery_on_way'
        self.call_center_order_id.state = 'delivery_on_way'

    def delivery_arrived(self):
        """ Delivery Arrived"""
        if self.prepaid and self.amount_due == 0:
            self.arrived_date = fields.Datetime.now()
            self.delivery_collection()
        else:
            self.arrived_date = fields.Datetime.now()
            self.delivery_state = 'delivery_arrived'
            self.call_center_order_id.state = 'delivery_arrived'

    def delivery_collection(self):
        """ Delivery Received Money"""
        self.delivery_state = 'delivery_collection'
        self.call_center_order_id.state = 'delivery_collection'

    def delivery_canceled(self):
        """Delivery Canceled"""
        self.delivery_state = 'delivery_canceled'
        self.call_center_order_id.state = 'delivery_canceled'
        self.button_draft()
        self.button_cancel()

    def set_to_delivery_invoices(self):
        """Delivery Canceled"""
        self.delivery_state = 'delivery_invoices'
        self.delivery_boy_id = False
        self.call_center_order_id.state = 'delivery_invoices'
        self.button_draft()

    # def action_view_register_payment_wizard(self):
    #     """ :return Register Payment Wizard action """
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'register.payment.wizard',
    #         'name': _('Collection Amount Wizard'),
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {'default_call_center_order_id': self.id},
    #         'views': [(False, 'form')],
    #     }

    @api.depends('number_copy')
    def add_copy(self):
        self.number_copy = self.number_copy + 1

    @api.depends('amount_residual')
    def _compute_paid_value(self):
        for rec in self:
            # paid amount  total before payment 
            rec.paid=     rec.amount_total       -      rec.amount_residual