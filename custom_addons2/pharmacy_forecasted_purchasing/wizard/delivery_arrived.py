""" Initialize Delivery Assign """

from odoo import fields, models


class DeliveryArrived(models.TransientModel):
    """
        Initialize Delivery Assign:
         -
    """
    _name = 'delivery.arrived'
    _description = 'Delivery Arrived'

    delivery_arrived = fields.Datetime()

    def confirm_delivery_arrived(self):
        """ Confirm Assign Delivery """
        active_id = self._context.get('active_id')
        delivery_arrived_order = self.env['stock.picking'].browse(active_id)
        for rec in self:
            delivery_arrived_order.delivery_arrived = rec.delivery_arrived

            delivery_arrived_order.state = 'delivery_arrived'
