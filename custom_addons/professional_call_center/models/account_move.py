""" Initialize Account Move """

from odoo import fields, models


class AccountMove(models.Model):
    """
        Inherit Account Move:
         -
    """
    _inherit = 'account.move'

    call_center_order_id = fields.Many2one(
        'call.center.order', readonly=True
    )
    order_type = fields.Selection(
        [('in_the_branch', 'In The Branch'),
         ('delivery', 'Delivery')],
        default='in_the_branch', readonly=True
    )
    delivery_date = fields.Datetime(
        string='Delivery Date & Time', copy=False, readonly=True
    )
    delivery_type_id = fields.Many2one(
        'delivery.type', readonly=True
    )
    picking_id = fields.Many2one(## 
        'stock.picking', string='Delivery Order', readonly=True
    )
    attachment = fields.Binary(
        readonly=True
    )
    street = fields.Char(
        readonly=True
    )
    street2 = fields.Char(
        readonly=True
    )
    state_id = fields.Many2one(
        'res.country.state', readonly=True
    )
    country_id = fields.Many2one(
        'res.country', readonly=True
    )
    zone_id = fields.Many2one(
        'res.country.zone', readonly=True,
    )
    district_id = fields.Many2one(
        'res.country.district', readonly=True
    )
    land_mark = fields.Char(
        readonly=True
    )
    building_type_id = fields.Many2one(
        'building.type', readonly=True
    )
    building_number = fields.Char(
        readonly=True
    )
    floor_number = fields.Char(
        readonly=True
    )
    flat_number = fields.Char(
        readonly=True
    )
    prepaid = fields.Boolean(
        readonly=True, copy=False, related='call_center_order_id.prepaid',
        tracking=True
    )
    paid_amount = fields.Float(
        related='call_center_order_id.paid_amount', copy=False, tracking=True
    )
    amount_due = fields.Float(
        related='call_center_order_id.amount_due', tracking=True
    )
