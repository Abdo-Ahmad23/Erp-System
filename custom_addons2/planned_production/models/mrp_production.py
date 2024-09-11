# -*- coding: utf-8 -*-
""" Mrp Production """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class MrpProduction(models.Model):
    """ inherit Mrp Production """
    _inherit = 'mrp.production'

    direct_labour_cost_ids = fields.One2many('direct.labour.cost',
                                             'mrp_production_id')
    direct_overhead_cost_ids = fields.One2many('direct.overhead.cost',
                                               'mrp_production_id')
    total_material_cost = fields.Monetary(currency_field='currency_id',
                                          compute='_compute_move_raw_ids',
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
    total_actual_labour = fields.Float()
    actual_labour_cost = fields.Float()
    total_actual_overhead = fields.Float()
    actual_overhead_cost = fields.Float()
    product_unit_cost = fields.Float()
    planned_manufacturing_id = fields.Many2one('planned.manufacturing')

    def view_action_requisition_type(self):
        """ View Action Send To Pricing """
        purchase_requisition = []
        internal_transfers_requisition = []
        for rec in self.move_raw_ids:
            # if rec.type_of_requisition == '1':
            purchase_requisition.append((0, 0,
                                         {'product_id': rec.product_id.id,
                                          'uom_id': rec.product_id.uom_id.id,
                                          'product_qty': rec.product_qty,
                                          'type_of_requisition': rec.type_of_requisition
                                          }))
            # if rec.type_of_requisition == '2':
            #     internal_transfers_requisition.append((0, 0,
            #                                            {
            #                                                'product_id': rec.product_id.id,
            #                                                'uom_id': rec.uom_id.id,
            #                                                'product_qty': rec.product_qty,
            #                                                'type_of_requisition': rec.type_of_requisition,
            #                                            }))
        action = \
            self.env.ref('planned_production.mrp_make_requisition_action').read()[
                0]
        action['views'] = [
            (self.env.ref('planned_production.mrp_make_requisition_form').id, 'form')]
        action['context'] = {
            'default_mrp_requisition_lines_ids': purchase_requisition}
        # if purchase_requisition and internal_transfers_requisition:
        #     action['context'] = {
        #         'default_purchase_requisition_type_line_ids': purchase_requisition,
        #         'default_internal_transfers_requisition_line_ids': internal_transfers_requisition,
        #         'default_empty_purchase_requisition': True,
        #         'default_empty_internal_transfers': True}
        # elif purchase_requisition and not internal_transfers_requisition:
        #     action['context'] = {
        #         'default_purchase_requisition_type_line_ids': purchase_requisition,
        #         'default_empty_purchase_requisition': True,
        #         'default_empty_internal_transfers': False}
        # elif internal_transfers_requisition and not purchase_requisition:
        #     action['context'] = {
        #         'default_internal_transfers_requisition_line_ids': internal_transfers_requisition,
        #         'default_empty_purchase_requisition': False,
        #         'default_empty_internal_transfers': True}
        # else:
        #     raise ValidationError(
        #         _("you are not select any line in the requisition agreement line"))

        return action

    def select_r(self):
        """ Select Delivery Invoice """

        res = []
        pro = []
        pro = self.env['mrp.production'].search([('id', '=', self.id)])
        print("id", self.id)
        for p in self.move_raw_ids:
            print(self.product_id.id)

            res.append((0, 0,
                        {'product_id': p.product_id.id
                         }))
        action = \
            self.env.ref('planned_production.report_mrp_group_action').read()[0]
        action['context'] = {
            'default_mrp_group_lines_ids': res}

        action['views'] = [(self.env.ref(
            'planned_production.report_mrp_group_form').id, 'form')]
        return action

    def pppp(self):
        """ Pppp """
        print(self.id)

    @api.onchange('direct_labour_cost_ids')
    def _onchange_direct_labour_cost_ids(self):
        """ direct_labour_cost_ids """
        total_actual_labour = 0
        actual_labour_cost = 0
        for rec in self.direct_labour_cost_ids:
            total_actual_labour += rec.actual_hours
            print('labour', total_actual_labour)
            actual_labour_cost += rec.total_actual_cost
            print('labour2', actual_labour_cost)
        self.total_actual_labour = total_actual_labour
        self.actual_labour_cost = actual_labour_cost

    @api.onchange('direct_overhead_cost_ids')
    def _onchange_direct_overhead_cost_ids(self):
        """ direct_labour_cost_ids """
        total_actual_overhead = 0
        actual_overhead_cost = 0
        for rec in self.direct_overhead_cost_ids:
            total_actual_overhead += rec.actual_hours
            print('overhead', total_actual_overhead)
            actual_overhead_cost += rec.total_actual_cost
            print('overhead2', actual_overhead_cost)
        self.total_actual_overhead = total_actual_overhead
        self.actual_overhead_cost = actual_overhead_cost

    @api.onchange('bom_id')
    def _onchange_bom_direct_material(self):
        """ bom_id """
        self.direct_labour_cost_ids = False
        direct_labour = []
        direct_overhead = []
        for labour in self.bom_id.direct_labour_cost_ids:
            direct_labour.append((0, 0,
                                  {
                                      'product_id': labour.product_id.id,
                                      'uom_id': labour.uom_id.id,
                                      'planned_quantity': labour.planned_quantity,
                                      'operation_id': labour.operation_id.id,
                                      'unit_cost': labour.unit_cost,
                                      'total_cost': labour.planned_quantity * labour.unit_cost,

                                  }))

        for lines in self.bom_id.direct_overhead_cost_ids:
            direct_overhead.append((0, 0,
                                    {
                                        'product_id': lines.product_id.id,
                                        'uom_id': lines.uom_id.id,
                                        'planned_quantity': lines.planned_quantity,
                                        'operation_id': lines.operation_id.id,
                                        'unit_cost': lines.unit_cost,
                                        'total_cost': lines.planned_quantity * lines.unit_cost,

                                    }))
        self.update(
            {'direct_labour_cost_ids': direct_labour,
             'direct_overhead_cost_ids': direct_overhead})

    # @api.depends('product_qty', 'direct_labour_cost_ids.total_cost')
    # def _compute_direct_labour_cost(self):
    #     """ Compute direct_labour_cost value """
    #     for rec in self:
    #         total_amount = 0
    #         for line in rec.direct_labour_cost_ids:
    #             line.planned_quantity = line.planned_quantity * self.product_qty
    #             total_amount += line.planned_quantity * line.unit_cost
    #         rec.update({'total_labour_cost': total_amount})
    #
    # @api.depends('product_qty', 'direct_overhead_cost_ids.total_cost')
    # def _compute_direct_overhead_cost(self):
    #     """ Compute direct_labour_cost value """
    #     for rec in self:
    #         total_amount = 0
    #         for line in rec.direct_overhead_cost_ids:
    #             line.planned_quantity = line.planned_quantity * self.product_qty
    #             total_amount += line.planned_quantity * line.unit_cost
    #         rec.update({'total_overhead_cost': total_amount})
    #
    # @api.depends('product_qty', 'move_raw_ids')
    # def _compute_move_raw_ids(self):
    #     """ Compute direct_labour_cost value """
    #     for rec in self:
    #         total_amount = 0
    #         for line in rec.move_raw_ids:
    #             line.product_qty = line.product_qty * self.product_qty
    #             total_amount += line.product_id.lst_price * line.product_qty
    #         rec.update({'total_material_cost': total_amount})

    #
    # @api.onchange('field_study_item_pricing_id')
    # def _onchange_field_study_item_pricing(self):
    #     """ field_study_item_pricing_id """
    #     self.requisition_agreement_line_ids = False
    #     requisition_agreement_lines = []
    #     for rec in self.field_study_item_pricing_id.item_pricing_lines_ids:
    #         product_quant = self.env['stock.quant'].search([
    #             ('location_id', '=', self.stock_location_id.id),
    #             ('product_id', '=', rec.product_id.id)])
    #         requisition_agreement_lines.append((0, 0,
    #                                             {
    #                                                 'product_id': rec.product_id.id,
    #                                                 'uom_id': rec.uom_id.id,
    #                                                 'product_qty': rec.planned_quantity,
    #                                                 'location_qty': product_quant,
    #                                                 'inventory_qy': rec.product_id.qty_available
    #                                             }))
    #     self.update(
    #         {'requisition_agreement_line_ids': requisition_agreement_lines})
