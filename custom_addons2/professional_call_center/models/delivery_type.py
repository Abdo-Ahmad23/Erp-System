""" Initialize Delivery Type """

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DeliveryType(models.Model):
    """
        Initialize Delivery Type:
         -
    """
    _name = 'delivery.type'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Delivery Type'
    _sql_constraints = [
        ('unique_code',
         'UNIQUE(code)',
         'Code must be unique'),
    ]

    name = fields.Char(
        required=True,
        translate=True,
    )
    code = fields.Char(
        required=True
    )
    active = fields.Boolean(
        default=True
    )
    delivery_type_line_ids = fields.One2many(
        'delivery.type.line',
        'delivery_type_id'
    )


class DeliveryTypeLine(models.Model):
    """
        Initialize Delivery Type Line:
         - 
    """
    _name = 'delivery.type.line'
    _description = 'Delivery Type Line'

    zone_id = fields.Many2one(
        'res.country.zone', required=True
    )
    district_id = fields.Many2one(
        'res.country.district', required=True,
        domain="[('zone_id', '=', zone_id)]"
    )
    price = fields.Float(
        required=True
    )
    delivery_type_id = fields.Many2one(
        'delivery.type'
    )

    @api.model
    def create(self, vals_list):
        """ Override create """
        # vals_list ={'field': value}  -> dectionary contains only new filled fields
        if vals_list['delivery_type_id']:
            delivery_line_count = self.env['delivery.type.line'].search_count(
                [('delivery_type_id', '=', vals_list['delivery_type_id']),
                 ('district_id', '=', vals_list['district_id'])])
            if delivery_line_count > 0:
                raise ValidationError(
                    _(
                        "You cannot select the type of delivery"
                        " with the same district"))
        return super(DeliveryTypeLine, self).create(vals_list)

    def write(self, vals):
        """ Override write """
        res = super(DeliveryTypeLine, self).write(vals)
        delivery_line_count = self.env['delivery.type.line'].search_count(
            [('delivery_type_id', '=', self.delivery_type_id.id),
             ('district_id', '=', self.district_id.id),
             ('id', '!=', self.id),
             ])
        if delivery_line_count > 0:
            raise ValidationError(
                _(
                    "You cannot select the type of delivery "
                    "with the same district"))
        return res
