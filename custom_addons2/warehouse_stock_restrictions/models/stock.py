# -*- coding: utf-8 -*-

from odoo.exceptions import UserError

from odoo import _, api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_locations = fields.Boolean('Restrict Location')

    stock_location_ids = fields.Many2many(
        'stock.location',
        'location_security_stock_location_users',
        'user_id',
        'location_id',
        'Stock Locations')

    default_picking_type_ids = fields.Many2many(
        'stock.picking.type', 'stock_picking_type_users_rel',
        'user_id', 'picking_type_id', string='Default Warehouse Operations')


class stock_move(models.Model):
    _inherit = 'stock.move'

    @api.constrains('state', 'location_id', 'location_dest_id')
    def check_user_location_rights(self):
        for rec in self:
            if rec.state == 'draft':
                return True

            user_locations = []
            for i in rec.env.user.stock_location_ids:
                user_locations.append(i.id)

            # user_locations = rec.env.user.stock_location_ids
            if rec.env.user.restrict_locations:
                message = _(
                    'Invalid Location. You cannot process this move since you do '
                    'not control the location "%s". '
                    'Please contact your Administrator.')

                if rec.location_id.id not in user_locations:
                    raise UserError(message % rec.location_id.name)
                elif rec.location_dest_id.id not in user_locations:
                    raise UserError(message % rec.location_dest_id.name)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _default_warehouse_id(self):
        # !!! Any change to the default value may have to be repercuted
        # on _init_column() below.
        return self.env.user._get_default_warehouse_id()

    stock_warehouse_id = fields.Many2one(
        'stock.warehouse',
        default=_default_warehouse_id
    )
    warehouse_loc_id = fields.Many2one(
        'stock.warehouse',
        default=_default_warehouse_id
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse', related='warehouse_loc_id'
    )

    @api.onchange('partner_id')
    def set_domain_for_warehouse(self):
        if self.user_has_groups(
                'warehouse_stock_restrictions.group_restrict_warehouse'):
            return {'domain': {
                'warehouse_loc_id': [
                    ('id', '=', self.env.user.property_warehouse_id.id)]
            }}

# class SaleOrderLine(models.Model):
#     """
#         Inherit Sale Order Line:
#          -
#     """
#     _inherit = 'sale.order.line'
#
#     warehouse_id = fields.Many2one(
#         'stock.warehouse', related='order_id.warehouse_loc_id'
#     )

#
# class StockQuantInherit(models.Model):
#     _inherit = 'stock.quant'
#
#     @api.model
#     def action_view_quants(self):
#         if self.env.user.has_group('stock.group_stock_manager'):
#             self = self.with_context(search_default_internal_loc=1)
#             self = self._set_view_context()
#             return self._get_quants_action(extend=True)
#         else:
#             self = self._set_view_context()
#             return self._get_quants_action(domain=[
#                 ('location_id', 'in', self.env.user.stock_location_ids.ids)],
#                 extend=True)
