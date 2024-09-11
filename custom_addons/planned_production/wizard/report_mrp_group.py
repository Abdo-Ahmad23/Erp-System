# -*- coding: utf-8 -*-
""" Report Group """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class ReportMrpGroup(models.TransientModel):
    """ Report Mrp Group """
    _name = 'report.mrp.group'
    _description = 'Report Mrp Group'

    test = fields.Char()
    mrp_group_lines_ids = fields.One2many('mrp.group.lines', 'report_mrp_group_id')


class MrpGroupLines(models.TransientModel):
    """ Mrp Group Lines """
    _name = 'mrp.group.lines'
    _description = 'Mrp Group Lines'

    product_id = fields.Many2one('product.product')
    report_mrp_group_id = fields.Many2one('report.mrp.group')
