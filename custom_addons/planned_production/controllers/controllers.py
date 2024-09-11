# -*- coding: utf-8 -*-
# from odoo import http


# class PlannedProduction(http.Controller):
#     @http.route('/planned_production/planned_production', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/planned_production/planned_production/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('planned_production.listing', {
#             'root': '/planned_production/planned_production',
#             'objects': http.request.env['planned_production.planned_production'].search([]),
#         })

#     @http.route('/planned_production/planned_production/objects/<model("planned_production.planned_production"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('planned_production.object', {
#             'object': obj
#         })
