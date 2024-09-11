""" Initialize Assign Delivery Boy """

from odoo import api, fields, models


class AssignDeliveryBoy(models.TransientModel):
    """
        Initialize Assign Delivery Boy:
         -
    """
    _name = 'assign.delivery.boy'
    _description = 'Assign Delivery Boy'

    account_move_ids = fields.Many2many(
        'account.move'
    )
    delivery_boy_id = fields.Many2one(
        'res.users', required=True

    )
    transportation = fields.Selection(
        [('car', 'Car'), ('motorcycle', 'Motorcycle'), ('bike', 'Bike')],
        required=True, default='car'
    )

    @api.onchange('transportation')
    def _onchange_transportation(self):
        """ Add domain to some filed """
        self.delivery_boy_id = False
        if self.transportation:
            return {
                'domain': {
                    'delivery_boy_id': [
                        ('transportation', '=', self.transportation),
                        ('groups_id', '=',
                         self.env.ref('base.group_portal').id)]
                }
            }

    def delivery_assigned(self):
        """ Delivery Assigned """
        for order in self.account_move_ids:
            order.write({
                'delivery_boy_id': self.delivery_boy_id.id,
                'delivery_state': 'delivery_assigned',
            })
            order.call_center_order_id.state = 'delivery_assigned'
