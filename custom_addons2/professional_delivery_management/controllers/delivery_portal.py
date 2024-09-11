# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from operator import itemgetter

from odoo.http import request
from odoo.tools import groupby as groupbyelem

from odoo import _
from odoo import fields
from odoo import http
from odoo.addons.portal.controllers.portal import (
    CustomerPortal,
    pager as portal_pager,
)


class DeliveryOrderPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        DeliveryOrders = request.env['account.move'].sudo()
        if 'orders_count' in counters:
            values['orders_count'] = DeliveryOrders.search_count(
                [
                    ('delivery_boy_id', '=', request.env.user.id),
                    ('delivery_state', '=', 'delivery_assigned')
                ]
            )
        if 'on_way_count' in counters:
            values['on_way_count'] = DeliveryOrders.search_count(
                [
                    ('delivery_boy_id', '=', request.env.user.id),
                    ('delivery_state', '=', 'delivery_on_way')
                ]
            )
        if 'arrived_count' in counters:
            values['arrived_count'] = DeliveryOrders.search_count(
                [
                    ('delivery_boy_id', '=', request.env.user.id),
                    ('delivery_state', '=', 'delivery_arrived')
                ]
            )
        if 'received_count' in counters:
            values['received_count'] = DeliveryOrders.search_count(
                [
                    ('delivery_boy_id', '=', request.env.user.id),
                    ('delivery_state', '=', 'delivery_collection'),
                    ('delivery_billed', '=', False)
                ]
            )
        if 'canceled_count' in counters:
            values['canceled_count'] = DeliveryOrders.search_count(
                [
                    ('delivery_boy_id', '=', request.env.user.id),
                    ('delivery_state', '=', 'delivery_canceled')
                ]
            )
        return values

    @http.route(['/my/transaction', '/my/transaction/page/<int:page>'],
                type='http', auth="user", website=True)
    def delivery_transaction(self, page=1, sortby=None, groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        DeliveryOrders = request.env['account.move'].sudo()
        domain = [
            ('delivery_boy_id', '=', request.env.uid),
            ('delivery_state', '=', 'delivery_assigned')]
        orders_count = len(DeliveryOrders.search(domain).ids)
        searchbar_sortings = {
            'delivery_date': {
                'label': _('Delivery Date & Time'),
                'order': 'delivery_date desc'
            },
            'name': {'label': _('Ref'), 'order': 'name desc'},
            'call_center_order_id': {
                'label': _('Call Center Ref'),
                'order': 'call_center_order_id asc'
            },
            'district_id': {'label': _('District'), 'order': 'district_id'},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'district_id': {'input': 'district_id', 'label': _('District')},
            'zone_id': {'input': 'zone_id', 'label': _('Zone')},
        }

        # default sortby order
        if not sortby:
            sortby = 'call_center_order_id'
        order = searchbar_sortings[sortby]['order']
        # default group by value
        if not groupby:
            groupby = 'zone_id'
        pager = portal_pager(
            url="/my/transaction",
            total=orders_count,
            url_args={'sortby': sortby},
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        if groupby == 'district_id':
            order = "district_id, %s" % order
        elif groupby == 'zone_id':
            order = "zone_id, %s" % order
        transactions = DeliveryOrders.search(
            domain,
            order=order, limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_orders_history'] = transactions.ids[:100]
        if groupby == 'district_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('district_id'))]
        elif groupby == 'zone_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('zone_id'))]
        else:
            grouped_order = [transactions]

        values.update({
            'transactions': transactions.sudo(),
            'page_name': 'delivery',
            'grouped_order': grouped_order,
            'pager': pager,
            'default_url': '/my/transaction',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
        })
        return request.render(
            'professional_delivery_management.delivery_order_template', values)

    @http.route('/my/transaction/<int:assign>',
                type='http',
                auth="user",
                website=True)
    def delivery_details(self, assign):

        DeliveryOrders = request.env['account.move'].sudo()
        assign = DeliveryOrders.sudo().browse(int(assign))
        return request.render(
            'professional_delivery_management.delivery_template_form', {
                'assign': assign,
            }
        )

    @http.route(['/my/transactions'],
                type='http',
                auth="user",
                website=True)
    def delivery_action(self, res_id, state, **kw):
        DeliveryOrders = request.env['account.move'].sudo()
        assign = DeliveryOrders.sudo().browse(int(res_id))
        if state == 'delivery_assigned':
            assign.write({
                'send_date': fields.Datetime.now(),
                'delivery_state': 'delivery_on_way',
            })
            assign.call_center_order_id.state = 'delivery_on_way'
        if state == 'delivery_canceled':
            assign.write({
                'delivery_state': 'delivery_canceled',
            })
            assign.call_center_order_id.state = 'delivery_canceled'
        if state == 'delivery_assigned_tree':
            assign.write({
                'send_date': fields.Datetime.now(),
                'delivery_state': 'delivery_on_way',
            })
            assign.call_center_order_id.state = 'delivery_on_way'
            return request.redirect('/my/transaction')
        elif state == 'delivery_cancel_tree':
            assign.write({
                'delivery_state': 'delivery_canceled',
            })
            assign.call_center_order_id.state = 'delivery_canceled'
            return request.redirect('/my/transaction')
        else:
            return request.render(
                'professional_delivery_management.delivery_template_form', {
                    'assign': assign.sudo(),
                })

    #     Delivery On Way
    @http.route(
        ['/my/way-transaction', '/my/way-transaction/page/<int:page>'],
        type='http', auth="user", website=True)
    def delivery_way_transaction(self, page=1, sortby=None, groupby=None,
                                 **kw):
        values = self._prepare_portal_layout_values()
        DeliveryOrders = request.env['account.move'].sudo()
        domain = [
            ('delivery_boy_id', '=', request.env.user.id),
            ('delivery_state', '=', 'delivery_on_way')
        ]
        on_way_count = len(DeliveryOrders.search(domain).ids)
        searchbar_sortings = {
            'delivery_date': {
                'label': _('Delivery Date & Time'),
                'order': 'delivery_date desc'
            },
            'name': {'label': _('Ref'), 'order': 'name desc'},
            'call_center_order_id': {
                'label': _('Call Center Ref'),
                'order': 'call_center_order_id asc'
            },
            'district_id': {'label': _('District'), 'order': 'district_id'},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'district_id': {'input': 'district_id', 'label': _('District')},
            'zone_id': {'input': 'zone_id', 'label': _('Zone')},
        }

        # default sortby order
        if not sortby:
            sortby = 'call_center_order_id'
        order = searchbar_sortings[sortby]['order']
        # default group by value
        if not groupby:
            groupby = 'zone_id'
        pager = portal_pager(
            url="/my/way-transaction",
            total=on_way_count,
            url_args={'sortby': sortby},
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        if groupby == 'district_id':
            order = "district_id, %s" % order
        elif groupby == 'zone_id':
            order = "zone_id, %s" % order
        transactions = DeliveryOrders.search(
            domain,
            order=order, limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_orders_history'] = transactions.ids[:100]
        if groupby == 'district_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('district_id'))]
        elif groupby == 'zone_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('zone_id'))]
        else:
            grouped_order = [transactions]

        values.update({
            'transactions': transactions.sudo(),
            'page_name': 'delivery_on_way',
            'grouped_order': grouped_order,
            'pager': pager,
            'default_url': '/my/way-transaction',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
        })
        return request.render(
            'professional_delivery_management.delivery_on_way_order_template', values)

    @http.route('/my/way-transaction/<int:on_way>',
                type='http',
                auth="user",
                website=True)
    def on_way_delivery_details(self, on_way):

        DeliveryOrders = request.env['account.move'].sudo()
        on_way = DeliveryOrders.sudo().browse(int(on_way))
        return request.render(
            'professional_delivery_management.delivery_on_way_template_form', {
                'on_way': on_way,
            }
        )

    @http.route(['/my/way-transactions'],
                type='http',
                auth="user",
                website=True)
    def on_way_action(self, res_id, state, **kw):
        DeliveryOrders = request.env['account.move'].sudo()
        on_way = DeliveryOrders.sudo().browse(int(res_id))

        if state == 'delivery_on_way':
            if on_way.prepaid and on_way.amount_due == 0:
                on_way.write({
                    'arrived_date': fields.Datetime.now(),
                    'delivery_state': 'delivery_collection',
                })
                on_way.call_center_order_id.write({
                    'state': 'delivery_collection',
                })
            else:
                on_way.write({
                    'arrived_date': fields.Datetime.now(),
                    'delivery_state': 'delivery_arrived',
                })
                on_way.call_center_order_id.state = 'delivery_arrived'
        if state == 'delivery_canceled':
            on_way.write({
                'delivery_state': 'delivery_canceled',
            })
            on_way.call_center_order_id.state = 'delivery_canceled'
        if state == 'delivery_on_way_tree':
            if on_way.prepaid and on_way.amount_due == 0:
                on_way.write({
                    'arrived_date': fields.Datetime.now(),
                    'delivery_state': 'delivery_collection',
                })
                on_way.call_center_order_id.write({
                    'state': 'delivery_collection',
                })
            else:
                on_way.write({
                    'arrived_date': fields.Datetime.now(),
                    'delivery_state': 'delivery_arrived',
                })
                on_way.call_center_order_id.state = 'delivery_arrived'
            return request.redirect('/my/way-transaction')
        elif state == 'delivery_cancel_tree':
            on_way.write({
                'delivery_state': 'delivery_canceled',
            })
            on_way.call_center_order_id.state = 'delivery_canceled'
            return request.redirect('/my/way-transaction')
        else:
            return request.render(
                'professional_delivery_management.delivery_on_way_template_form', {
                    'on_way': on_way.sudo(),
                })

    #     Delivery arrived
    @http.route(
        ['/my/arrived-transaction', '/my/arrived-transaction/page/<int:page>'],
        type='http', auth="user", website=True)
    def delivery_arrived_transaction(self, page=1, sortby=None, groupby=None,
                                     **kw):
        values = self._prepare_portal_layout_values()
        DeliveryOrders = request.env['account.move'].sudo()
        domain = [
            ('delivery_boy_id', '=', request.env.user.id),
            ('delivery_state', '=', 'delivery_arrived')
        ]
        arrived_count = len(DeliveryOrders.search(domain).ids)
        searchbar_sortings = {
            'delivery_date': {
                'label': _('Delivery Date & Time'),
                'order': 'delivery_date desc'
            },
            'name': {'label': _('Ref'), 'order': 'name desc'},
            'call_center_order_id': {
                'label': _('Call Center Ref'),
                'order': 'call_center_order_id asc'
            },
            'district_id': {'label': _('District'), 'order': 'district_id'},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'district_id': {'input': 'district_id', 'label': _('District')},
            'zone_id': {'input': 'zone_id', 'label': _('Zone')},
        }

        # default sortby order
        if not sortby:
            sortby = 'call_center_order_id'
        order = searchbar_sortings[sortby]['order']
        # default group by value
        if not groupby:
            groupby = 'zone_id'
        pager = portal_pager(
            url="/my/arrived-transaction",
            total=arrived_count,
            url_args={'sortby': sortby},
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        if groupby == 'district_id':
            order = "district_id, %s" % order
        elif groupby == 'zone_id':
            order = "zone_id, %s" % order
        transactions = DeliveryOrders.search(
            domain,
            order=order, limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_orders_history'] = transactions.ids[:100]
        if groupby == 'district_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('district_id'))]
        elif groupby == 'zone_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('zone_id'))]
        else:
            grouped_order = [transactions]

        values.update({
            'transactions': transactions.sudo(),
            'page_name': 'arrived_delivery',
            'grouped_order': grouped_order,
            'pager': pager,
            'default_url': '/my/arrived-transaction',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
        })
        return request.render(
            'professional_delivery_management.arrived_delivery_order_template', values)

    @http.route('/my/arrived-transaction/<int:arrived_order>',
                type='http',
                auth="user",
                website=True)
    def arrived_delivery_details(self, arrived_order):

        DeliveryOrders = request.env['account.move'].sudo()
        arrived_order = DeliveryOrders.sudo().browse(int(arrived_order))
        return request.render(
            'professional_delivery_management.arrived_delivery_template_form', {
                'arrived_order': arrived_order,
            }
        )

    @http.route(['/my/arrived-transactions'],
                type='http',
                auth="user",
                website=True)
    def arrived_delivery_action(self, res_id, state, **kw):
        DeliveryOrders = request.env['account.move'].sudo()
        arrived_order = DeliveryOrders.sudo().browse(int(res_id))

        if state == 'delivery_arrived':
            arrived_order.write({
                'delivery_state': 'delivery_collection',
            })
            arrived_order.call_center_order_id.state = 'delivery_collection'
        if state == 'delivery_canceled':
            arrived_order.write({
                'delivery_state': 'delivery_canceled',
            })
            arrived_order.call_center_order_id.state = 'delivery_canceled'
        if state == 'delivery_arrived_tree':
            arrived_order.write({
                'delivery_state': 'delivery_collection',
            })
            arrived_order.call_center_order_id.state = 'delivery_collection'
            return request.redirect('/my/arrived-transaction')
        elif state == 'delivery_cancel_tree':
            arrived_order.write({
                'delivery_state': 'delivery_canceled',
            })
            arrived_order.call_center_order_id.state = 'delivery_canceled'
            return request.redirect('/my/way-transaction')
        else:
            return request.render(
                'professional_delivery_management.arrived_delivery_template_form', {
                    'arrived_order': arrived_order.sudo(),
                })

    #     Delivery Received Money
    @http.route(
        ['/my/received-transaction',
         '/my/received-transaction/page/<int:page>'],
        type='http', auth="user", website=True)
    def delivery_delivery_collection_transaction(self, page=1, sortby=None,
                                                 groupby=None,
                                                 **kw):
        values = self._prepare_portal_layout_values()
        DeliveryOrders = request.env['account.move'].sudo()
        domain = [
            ('delivery_boy_id', '=', request.env.user.id),
            ('delivery_state', '=', 'delivery_collection'),
            ('delivery_billed', '=', False)
        ]
        received_count = len(DeliveryOrders.search(domain).ids)
        searchbar_sortings = {
            'delivery_date': {
                'label': _('Delivery Date & Time'),
                'order': 'delivery_date desc'
            },
            'name': {'label': _('Ref'), 'order': 'name desc'},
            'call_center_order_id': {
                'label': _('Call Center Ref'),
                'order': 'call_center_order_id asc'
            },
            'district_id': {'label': _('District'), 'order': 'district_id'},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'district_id': {'input': 'district_id', 'label': _('District')},
            'zone_id': {'input': 'zone_id', 'label': _('Zone')},
        }

        # default sortby order
        if not sortby:
            sortby = 'call_center_order_id'
        order = searchbar_sortings[sortby]['order']
        # default group by value
        if not groupby:
            groupby = 'zone_id'
        pager = portal_pager(
            url="/my/received-transaction",
            total=received_count,
            url_args={'sortby': sortby},
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        if groupby == 'district_id':
            order = "district_id, %s" % order
        elif groupby == 'zone_id':
            order = "zone_id, %s" % order
        transactions = DeliveryOrders.search(
            domain,
            order=order, limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_orders_history'] = transactions.ids[:100]
        if groupby == 'district_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('district_id'))]
        elif groupby == 'zone_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('zone_id'))]
        else:
            grouped_order = [transactions]

        values.update({
            'transactions': transactions.sudo(),
            'page_name': 'received_money_delivery',
            'grouped_order': grouped_order,
            'pager': pager,
            'default_url': '/my/received-transaction',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
        })
        return request.render(
            'professional_delivery_management.delivery_collection_delivery_order_template',
            values)

    @http.route('/my/received-transaction/<int:received_money>',
                type='http',
                auth="user",
                website=True)
    def received_delivery_details(self, received_money):

        DeliveryOrders = request.env['account.move'].sudo()
        received_money = DeliveryOrders.sudo().browse(int(received_money))
        return request.render(
            'professional_delivery_management.delivery_collection_delivery_template_form', {
                'received_money': received_money,
            }
        )

    #     Delivery Canceled
    @http.route(
        ['/my/canceled-transaction',
         '/my/canceled-transaction/page/<int:page>'],
        type='http', auth="user", website=True)
    def delivery_canceled_order_transaction(self, page=1, sortby=None,
                                            groupby=None,
                                            **kw):
        values = self._prepare_portal_layout_values()
        DeliveryOrders = request.env['account.move'].sudo()
        domain = [
            ('delivery_boy_id', '=', request.env.user.id),
            ('delivery_state', '=', 'delivery_canceled')
        ]
        canceled_count = len(DeliveryOrders.search(domain).ids)
        searchbar_sortings = {
            'delivery_date': {
                'label': _('Delivery Date & Time'),
                'order': 'delivery_date desc'
            },
            'name': {'label': _('Ref'), 'order': 'name desc'},
            'call_center_order_id': {
                'label': _('Call Center Ref'),
                'order': 'call_center_order_id asc'
            },
            'district_id': {'label': _('District'), 'order': 'district_id'},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'district_id': {'input': 'district_id', 'label': _('District')},
            'zone_id': {'input': 'zone_id', 'label': _('Zone')},
        }

        # default sortby order
        if not sortby:
            sortby = 'call_center_order_id'
        order = searchbar_sortings[sortby]['order']
        # default group by value
        if not groupby:
            groupby = 'zone_id'
        pager = portal_pager(
            url="/my/canceled-transaction",
            total=canceled_count,
            url_args={'sortby': sortby},
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        if groupby == 'district_id':
            order = "district_id, %s" % order
        elif groupby == 'zone_id':
            order = "zone_id, %s" % order
        transactions = DeliveryOrders.search(
            domain,
            order=order, limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_orders_history'] = transactions.ids[:100]
        if groupby == 'district_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('district_id'))]
        elif groupby == 'zone_id':
            grouped_order = [DeliveryOrders.concat(*g) for
                             k, g in
                             groupbyelem(transactions,
                                         itemgetter('zone_id'))]
        else:
            grouped_order = [transactions]

        values.update({
            'transactions': transactions.sudo(),
            'page_name': 'canceled_order',
            'grouped_order': grouped_order,
            'pager': pager,
            'default_url': '/my/canceled-transaction',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
        })
        return request.render(
            'professional_delivery_management.canceled_order_delivery_order_template',
            values)

    @http.route('/my/canceled-transaction/<int:canceled_order>',
                type='http',
                auth="user",
                website=True)
    def canceled_delivery_details(self, canceled_order):

        DeliveryOrders = request.env['account.move'].sudo()
        canceled_order = DeliveryOrders.sudo().browse(int(canceled_order))
        return request.render(
            'professional_delivery_management.canceled_order_delivery_template_form', {
                'canceled_order': canceled_order,
            }
        )
