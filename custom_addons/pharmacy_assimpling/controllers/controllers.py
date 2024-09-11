# -*- coding: utf-8 -*-
# from odoo import http


# class StockPickingKanban(http.Controller):
#     @http.route('/stock_picking_kanban/stock_picking_kanban/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_kanban/stock_picking_kanban/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_kanban.listing', {
#             'root': '/stock_picking_kanban/stock_picking_kanban',
#             'objects': http.request.env['stock_picking_kanban.stock_picking_kanban'].search([]),
#         })

#     @http.route('/stock_picking_kanban/stock_picking_kanban/objects/<model("stock_picking_kanban.stock_picking_kanban"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_kanban.object', {
#             'object': obj
#         })
