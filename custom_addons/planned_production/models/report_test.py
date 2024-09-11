# -*- coding: utf-8 -*-
""" Report Test """
from odoo import fields, models


class MrpProduction(models.Model):
    """ inherit Mrp Production """
    _inherit = 'mrp.production'

    def repo(self):
        """ Repo """
        for rec in self:
            pass
