# -*- coding: utf-8 -*-
""" Stock Move """
from odoo import api, fields, models, _


class StockMove(models.Model):
    """ inherit Stock Move """
    _inherit = 'stock.move'

    type_of_requisition = fields.Selection(
        [('1', 'Purchase'), ('2', 'Internal Transfers')])
