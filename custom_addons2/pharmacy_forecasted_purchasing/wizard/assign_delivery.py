""" Initialize Assign Delivery """

from odoo import api, fields, models


class AssignDelivery(models.TransientModel):
    """
        Initialize Assign Delivery:
         - 
    """
    _name = 'assign.delivery'
    _description = 'Assign Delivery'

    hr_employee_id = fields.Many2one(
        'hr.employee', string='Employee'
    )
    date_time_delivery = fields.Datetime(string='Date & Time Delivery')
    partner_zone_id = fields.Many2one(
        'partner.zone', string='Zone'
    )
    region = fields.Char()

    def confirm_assign_delivery(self):
        """ Confirm Assign Delivery """
        active_id = self._context.get('active_id')
        delivery_order = self.env['stock.picking'].browse(active_id)
        for rec in self:
            delivery_order.hr_employee_id = rec.hr_employee_id.id
            delivery_order.date_time_delivery = rec.date_time_delivery
            delivery_order.partner_zone_id = rec.partner_zone_id.id
            delivery_order.region = rec.region
            delivery_order.state = 'on_delivery'
