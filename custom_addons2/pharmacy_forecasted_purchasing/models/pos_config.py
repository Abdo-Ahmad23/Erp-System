# -*- coding: utf-8 -*-
""" Pos Confg """
from odoo import fields, models


class PosConfig(models.Model):
    """ inherit Pos Config """
    _inherit = 'pos.config'

    is_call_center = fields.Boolean(string='Is Call Center')
    is_branch = fields.Boolean(string='Is a branch')
