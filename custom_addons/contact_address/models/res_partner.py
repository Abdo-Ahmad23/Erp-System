""" Initialize Res Partner """

from odoo import api, fields, models


class ResPartner(models.Model):
    """
        Inherit Res Partner:
         -
    """
    _inherit = 'res.partner'

    district_id = fields.Many2one(
        'res.country.district',
        domain="[('zone_id', '=?', zone_id)]"
    )
    zone_id = fields.Many2one(
        'res.country.zone',
        domain="[('state_id', '=?', state_id)]"
    )
    land_mark = fields.Char()
    building_type_id = fields.Many2one(
        'building.type'
    )
    building_number = fields.Char()
    floor_number = fields.Char()
    flat_number = fields.Char()

    @api.onchange('district_id')
    def _onchange_district_id(self):
        """ district_id """
        if self.district_id:
            self.zone_id = self.district_id.zone_id.id
            self.state_id = self.district_id.state_id.id
            self.country_id = self.district_id.country_id.id
