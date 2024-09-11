# -*- coding: utf-8 -*-
""" Planned Manufacturing Orders """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class PlannedManufacturing(models.Model):
    """ Planned Manufacturing """
    _name = 'planned.manufacturing'
    _description = 'Planned Manufacturing'

    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirm')],
        default='draft',
        string='Status'
    )
    name = fields.Char(default='NEW')
    date = fields.Datetime(default=fields.Datetime.now())

    planned_manufacturing_orders_ids = fields.One2many(
        'planned.manufacturing.orders', 'planned_manufacturing_id')
    mrp_production_ids = fields.One2many('mrp.production',
                                         'planned_manufacturing_id')
    mrp_production_count = fields.Integer(
        compute='_compute_mrp_production_count', store=True)

    @api.depends('mrp_production_ids')
    def _compute_mrp_production_count(self):
        """ Compute distributed_assays_number value """
        self.mrp_production_count = len(
            self.mrp_production_ids.ids)

    def action_mrp_planned_production(self):
        """ Smart button to run action """
        recs = self.mapped('mrp_production_ids')
        action = \
            self.env.ref(
                'mrp.mrp_production_action').read()[
                0]
        if len(recs) > 1:
            action['domain'] = [('id', 'in', recs.ids)]
            action['context'] = {'planned_manufacturing_id': self.id}

        elif len(recs) == 1:
            action['views'] = [
                (
                    self.env.ref('mrp.mrp_production_form_view').id,
                    'form')]
            action['res_id'] = recs.ids[0]
            action['context'] = {'planned_manufacturing_id': self.id}
        else:
            action['views'] = [
                (
                    self.env.ref('mrp.mrp_production_form_view').id,
                    'form')]
            action['context'] = {'planned_manufacturing_id': self.id}

        return action

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'planned.manufacturing') or '/'
        return super(PlannedManufacturing, self).create(vals)

    def mrp_order_create(self):
        """ Mrp Order Create """
        order_line = []
        if self.planned_manufacturing_orders_ids:
            for rec in self.planned_manufacturing_orders_ids:
                for com in rec.bom_line_ids:
                    order_line.append((0, 0,
                                       {
                                           'product_id': com.product_id.id,
                                           'location_id': com.uom_id.id,
                                           'quantity': com.quantity,
                                       }))
                self.env['mrp.production'].create(
                    {'product_id': rec.product_tmpl_id.product_variant_id.id,
                     'planned_manufacturing_id': self.id,
                     'bom_id': rec.mrp_bom_id.id,
                     'product_qty': rec.mrp_bom_id.product_qty,
                     'date_planned_start': rec.scheduled_date,
                     'product_uom_id': rec.product_tmpl_id.product_variant_id.uom_id.id})
            self.state = 'confirm'
        else:
            raise UserError(_('lines is empty.'))


class PlannedManufacturingOrders(models.Model):
    """ Planned Manufacturing Orders """
    _name = 'planned.manufacturing.orders'
    _description = 'Planned Manufacturing Orders'

    planned_manufacturing_id = fields.Many2one('planned.manufacturing')
    product_id = fields.Many2one('product.product')
    product_tmpl_id = fields.Many2one('product.template')
    mrp_bom_id = fields.Many2one('mrp.bom')
    source = fields.Char()
    scheduled_date = fields.Datetime()

    @api.onchange('product_tmpl_id')
    def _onchange_product_id(self):
        """ Add domain to some filed """
        self.mrp_bom_id = False
        if self.product_tmpl_id:
            return {'domain': {
                'mrp_bom_id': [
                    ('product_tmpl_id', '=', self.product_tmpl_id.id)]
            }}

    @api.onchange('mrp_bom_id')
    def _onchange_mrp_bom_id(self):
        """ mrp_bom_id """
        self.product_id = self.mrp_bom_id.product_id.id
