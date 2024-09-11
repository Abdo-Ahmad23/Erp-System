# -*- coding: utf-8 -*-
""" Mrp Bom """
from odoo import api, fields, models, _


class MrpBom(models.Model):
    """ inherit Mrp Bom """
    _inherit = 'mrp.bom'

    direct_labour_cost_ids = fields.One2many('direct.labour.cost', 'mrp_bom_id')
    direct_overhead_cost_ids = fields.One2many('direct.overhead.cost',
                                               'mrp_bom_id')
    total_material_cost = fields.Monetary(currency_field='currency_id',
                                          compute='_compute_bom_line',
                                          store=True, readonly=1)
    total_labour_cost = fields.Monetary(currency_field='currency_id',
                                        compute='_compute_direct_labour_cost',
                                        store=True)
    total_overhead_cost = fields.Monetary(currency_field='currency_id',
                                          compute='_compute_direct_overhead_cost',
                                          store=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)

    @api.depends('product_qty', 'direct_labour_cost_ids.total_cost')
    def _compute_direct_labour_cost(self):
        """ Compute direct_labour_cost value """
        for rec in self:
            total_amount = 0
            for line in rec.direct_labour_cost_ids:
                line.planned_quantity = line.planned_quantity * self.product_qty
                total_amount += line.planned_quantity * line.unit_cost
            rec.update({'total_labour_cost': total_amount})

    @api.depends('product_qty', 'direct_overhead_cost_ids.total_cost')
    def _compute_direct_overhead_cost(self):
        """ Compute direct_labour_cost value """
        for rec in self:
            total_amount = 0
            for line in rec.direct_overhead_cost_ids:
                line.planned_quantity = line.planned_quantity * self.product_qty
                total_amount += line.planned_quantity * line.unit_cost
            rec.update({'total_overhead_cost': total_amount})

    @api.depends('product_qty', 'bom_line_ids')
    def _compute_bom_line(self):
        """ Compute direct_labour_cost value """
        for rec in self:
            total_amount = 0
            for line in rec.bom_line_ids:
                line.product_qty = line.product_qty * self.product_qty
                total_amount += line.product_id.lst_price * line.product_qty
            rec.update({'total_material_cost': total_amount})


class DirectLabourCost(models.Model):
    """ Direct Labour Cost """
    _name = 'direct.labour.cost'
    _description = 'Direct Labour Cost'

    mrp_bom_id = fields.Many2one('mrp.bom')
    mrp_production_id = fields.Many2one('mrp.production')
    operation_id = fields.Many2one(
        'mrp.routing.workcenter', 'Operation Type')
    product_id = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')])
    planned_quantity = fields.Float(default=1)
    unit_cost = fields.Float()
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    actual_hours = fields.Float()
    total_cost = fields.Float()
    total_actual_cost = fields.Float()

    @api.onchange('actual_hours', 'unit_cost')
    def _onchange_actual_cost(self):
        """ actual_cost """
        self.total_actual_cost = self.actual_hours * self.unit_cost

    @api.onchange('product_id', 'planned_quantity', 'unit_cost')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            rec.uom_id = rec.product_id.uom_id.id
            rec.unit_cost = rec.product_id.lst_price
            rec.total_cost = rec.unit_cost * rec.planned_quantity


class DirectOverheadCost(models.Model):
    """ Direct Overhead Cost """
    _name = 'direct.overhead.cost'
    _description = 'Direct Overhead Cost'

    mrp_bom_id = fields.Many2one('mrp.bom')
    mrp_production_id = fields.Many2one('mrp.production')
    operation_id = fields.Many2one(
        'mrp.routing.workcenter', 'Operation Type')
    product_id = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')])
    planned_quantity = fields.Float(default=1)
    unit_cost = fields.Float()
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    actual_hours = fields.Float()
    total_cost = fields.Float()
    total_actual_cost = fields.Float()

    @api.onchange('product_id', 'planned_quantity', 'unit_cost')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            rec.uom_id = rec.product_id.uom_id.id
            rec.unit_cost = rec.product_id.lst_price
            rec.total_cost = rec.unit_cost * rec.planned_quantity

    @api.onchange('actual_hours', 'unit_cost')
    def _onchange_actual_cost(self):
        """ actual_cost """
        self.total_actual_cost = self.actual_hours * self.unit_cost
