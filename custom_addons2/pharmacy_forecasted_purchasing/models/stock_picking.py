""" Initialize Stock Picking """

from odoo import fields, models


class StockPicking(models.Model):
    """
        Inherit Stock Picking:
         - 
    """
    _inherit = 'stock.picking'

    hr_employee_id = fields.Many2one(
        'hr.employee', string='Employee'
    )
    date_time_delivery = fields.Datetime(string='Date & Time Delivery')
    partner_zone_id = fields.Many2one(
        'partner.zone', string='Zone'
    )
    region = fields.Char()
    delivery_arrived = fields.Datetime()

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('on_delivery', 'On Delivery'),
        ('delivery_arrived', 'Delivery Arrived'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    from_sale = fields.Boolean()

    # @api.depends('sale_id')
    # def _compute_from_sale(self):
    #     """ Compute from_sale value """
    #     for rec in self:
    #         if rec.sale_id:
    #             rec.from_sale = True
    #         else:
    #             rec.from_sale = False

    def action_view_assign_delivery(self):
        self.ensure_one()

        action = \
            self.env.ref(
                'pharmacy_forecasted_purchasing.assign_delivery_action').read()[
                0]

        action['views'] = [
            (self.env.ref(
                'pharmacy_forecasted_purchasing.assign_delivery_form').id,
             'form')]
        action['context'] = {
            "default_partner_zone_id": self.partner_id.partner_zone_id.id,
            "default_region": self.partner_id.street
        }

        return action

    def _action_done(self):
        """ inherit _action_done() """
        res = super(StockPicking, self)._action_done()
        self.write({'date_done': self.scheduled_date, 'priority': '0'})
        return res
