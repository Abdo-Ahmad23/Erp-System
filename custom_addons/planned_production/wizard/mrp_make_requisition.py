# -*- coding: utf-8 -*-
""" Mrp Make Requisition """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class MrpMakeRequisition(models.TransientModel):
    """ Mrp Make Requisition """
    _name = 'mrp.make.requisition'
    _description = 'Mrp Make Requisition'

    mrp_requisition_lines_ids = fields.One2many('mrp.requisition.lines',
                                                'mrp_make_requisition_id')


class MrpRequisitionLines(models.TransientModel):
    """ Mrp Requisition Lines """
    _name = 'mrp.requisition.lines'
    _description = 'Mrp Requisition Lines'

    mrp_make_requisition_id = fields.Many2one('mrp.make.requisition')
    product_id = fields.Many2one('product.product')
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    product_qty = fields.Float(string="Planned Qty")
    type_of_requisition = fields.Selection(
        [('1', 'Purchase'), ('2', 'Internal Transfers')])
