""" Initialize Res District """

from odoo import api, fields, models


class ResCountryDistrict(models.Model):
    """
        Initialize Res Country District:
         -
    """
    _name = 'res.country.district'
    _description = 'Country District'

    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True
    )
    code = fields.Char(
        required=True,
    )
    zone_id = fields.Many2one(
        'res.country.zone', required=True,
        domain="[('state_id', '=?', state_id)]"
    )
    state_id = fields.Many2one(
        'res.country.state', required=True,
        domain="[('country_id', '=?', country_id)]"
    )
    country_id = fields.Many2one(
        'res.country', required=True,
    )

    @api.onchange('state_id')
    def _onchange_state_id(self):
        """ state_id """
        if self.state_id:
            self.country_id = self.state_id.country_id.id

    @api.onchange('zone_id')
    def _onchange_zone_id(self):
        """ state_id """
        self.country_id = self.zone_id.country_id.id
        self.state_id = self.zone_id.state_id.id
