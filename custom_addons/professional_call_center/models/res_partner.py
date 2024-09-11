# -*- coding: utf-8 -*-
""" Initialize Res Partner """

from odoo import api, fields, models


class ResPartner(models.Model):
    """
        Inherit Res Partner:
         -
    """
    _inherit = 'res.partner'
    _sql_constraints = [
        ('unique_customer_code',
         'UNIQUE(customer_code)',
         'Customer Code must be unique'),
    ]

    is_customer = fields.Boolean(
        string='Is a Customer'
    )
    is_vendor = fields.Boolean(
        string='Is a Vendor'
    )
    mobile = fields.Char(
        string='Mobile 1'
    )
    mobile_2 = fields.Char()
    mobile_3 = fields.Char()
    mobile_4 = fields.Char()
    mobile_5 = fields.Char()
    customer_code = fields.Char()
    delivery_address_info_ids = fields.One2many(
        'delivery.address.info',
        'partner_id'
    )


class DeliveryAddressInfo(models.Model):
    """
        Initialize Delivery Address Info:
         -
    """
    _name = 'delivery.address.info'
    _description = 'Delivery Address Info'

    street = fields.Char(
        required=True
    )
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    district_id = fields.Many2one(
        'res.country.district',
        domain="[('zone_id', '=?', zone_id)]"
    )
    zone_id = fields.Many2one(
        'res.country.zone',
        domain="[('state_id', '=?', state_id)]"
    )
    state_id = fields.Many2one("res.country.state", string='State',
                               ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country',
                                 ondelete='restrict')
    land_mark = fields.Char()
    building_type_id = fields.Many2one(
        'building.type'
    )
    building_number = fields.Char()
    floor_number = fields.Char()
    flat_number = fields.Char()
    partner_id = fields.Many2one(
        'res.partner'
    )

    @api.onchange('district_id')
    def _onchange_district_id(self):
        """ district_id """
        if self.district_id:
            self.zone_id = self.district_id.zone_id.id
            self.state_id = self.district_id.state_id.id
            self.country_id = self.district_id.country_id.id

    def name_get(self):
        result = []
        for rewrite in self:
            name = "%s - %s- %s- %s" % (
                rewrite.district_id.name, rewrite.zone_id.name,
                rewrite.state_id.name, rewrite.country_id.name)
            result.append((rewrite.id, name))
        return result
