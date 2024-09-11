# -*- coding: utf-8 -*-
""" Stock Quant """
from odoo import api, fields, models


class StockQuant(models.Model):
    """ inherit Stock Quant """
    _inherit = 'stock.quant'

    product_categ_id = fields.Many2one(related='product_tmpl_id.categ_id',
                                       store=1)


class Picking(models.Model):
    _inherit = "stock.picking"

    invoice_status = fields.Integer(default=0)
    sale_order_id = fields.Many2one('sale.order')
    account_move_id = fields.Many2one('account.move')
    invoice_is_created = fields.Boolean()

    def button_validate(self):
        self.invoice_status = 1
        self.invoice_is_created = True
        self.user_id = self.env.user.id
        return super(Picking, self).button_validate()

    def create_invoice_to_delivery(self):
        """ :return Action Out Deposit Wizard"""
        self.ensure_one()
        lines = []
        print(self.sale_id.order_line)
        for rec in self.sale_id.order_line:
            rec.qty_invoiced += 1
            if rec.product_id.detailed_type == 'service':
                lines.append((0, 0,
                              {'product_id': rec.product_id.id,
                               'product_uom_id': rec.product_uom.id,
                               'price_unit': rec.price_unit,
                               'quantity': rec.product_uom_qty
                               }))
            else:
                lines.append((0, 0,
                              {'product_id': rec.product_id.id,
                               'product_uom_id': rec.product_uom.id,
                               'price_unit': rec.price_unit,
                               'quantity': rec.qty_delivered
                               }))

        self.account_move_id = self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'street': self.partner_id.street,
            'zone': self.partner_id.zone,
            'mobile': self.partner_id.mobile,
            'building_floor': self.partner_id.building_floor,
            'special_mark': self.partner_id.special_mark,
            'area_region': self.partner_id.area_region,
            'stock_picking_id': self.id,
            'invoice_line_ids': lines,
        }).id
        self.account_move_id.action_post()
        self.account_move_id.send_to_delivery()
        self.sale_id.invoice_status = 'invoiced'
        self.sale_id.invoice_ids = [(4, self.account_move_id.id)]
        self.invoice_is_created = False


class StockMove(models.Model):
    """ inherit Stock Move """
    _inherit = 'stock.move'

    price_unit = fields.Float()
