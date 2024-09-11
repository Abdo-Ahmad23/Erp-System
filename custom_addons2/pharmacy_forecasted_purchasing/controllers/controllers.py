# -*- coding: utf-8 -*-
# from odoo import http


# class Noha(http.Controller):
#     @http.route('/noha/noha', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/noha/noha/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('noha.listing', {
#             'root': '/noha/noha',
#             'objects': http.request.env['noha.noha'].search([]),
#         })

#     @http.route('/noha/noha/objects/<model("noha.noha"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('noha.object', {
#             'object': obj
#         })
