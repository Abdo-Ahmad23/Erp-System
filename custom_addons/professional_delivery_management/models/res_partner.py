# -*- coding: utf-8 -*-
""" Initialize Res Partner """

from odoo import api, fields, models


class ResPartner(models.Model):
    """
        Inherit Res Partner:
         -
    """
    _inherit = 'res.partner'

    is_delivery_boy = fields.Boolean()
    identification_number = fields.Char(
        string="National ID", size=14
    )
    transportation = fields.Selection(
        [('car', 'Car'), ('motorcycle', 'Motorcycle'), ('bike', 'Bike')],
    )
    plate_number = fields.Char()
    commission_fees = fields.Float()

    @api.onchange('company_type')
    def _onchange_company_type(self):
        """ company_type """
        if self.company_type == 'company':
            self.is_delivery_boy = False
            self.transportation = False
