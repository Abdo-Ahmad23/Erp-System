# -*- coding: utf-8 -*-
from odoo.http import request

from odoo import http


class ManageDelivery(http.Controller):
    @http.route('/manage/delivery', type='http', auth="user", website=True)
    def portal_products(self, **kw):
        print(request.env.user.name)
        print(request.env['manage.delivery.liens'].sudo().search(
            [('manage_delivery_id.delivery_boy', '=', request.env.user.partner_id.id)]))
        return request.render("manage_delivery.delivery_orders_portal",
                              {'orders': request.env[
                                  'manage.delivery.liens'].sudo().search(
                                  [('delivery_boy', '=', request.env.user.partner_id.id)])})

    @http.route('/manage/delivery/<model("manage.delivery.liens"):o>',
                type='http', auth="user", website=True)
    def portal_products_orders(self, o):
        record = request.env['manage.delivery.liens'].sudo().search(
            [('id', '=', o.id)])
        if record:
            print(record)
            record.state = '2'
            record.account_move_id.delivery_status = '3'

        return request.render("manage_delivery.delivery_orders_portal",
                              {'orders': request.env[
                                  'manage.delivery.liens'].sudo().search(
                                  [])})

    @http.route('/delivery/order/<model("manage.delivery.liens"):o>',
                type='http', auth="user", website=True)
    def portal_delivery_orders(self, o):
        return request.render("manage_delivery.detail_delivery_orders",
                              {'o': o})
