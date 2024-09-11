""" Initialize Stock Return Picking """

from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round

from odoo import _, api, models


class ReturnPicking(models.TransientModel):
    """
        Inherit Stock Return Picking:
         -
    """
    _inherit = 'stock.return.picking'

    @api.onchange('picking_id')
    def _onchange_picking_id(self):
        move_dest_exists = False
        product_return_moves = [(5,)]
        if self.picking_id and self.picking_id.state != 'done':
            raise UserError(_("You may only return Done pickings."))
        # In case we want to set specific default values (e.g. 'to_refund'), we must fetch the
        # default values for creation.
        line_fields = [f for f in
                       self.env['stock.return.picking.line']._fields.keys()]
        product_return_moves_data_tmpl = self.env[
            'stock.return.picking.line'].default_get(line_fields)
        for move in self.picking_id.move_lines:
            if move.state == 'cancel':
                continue
            if move.scrapped:
                continue
            if move.move_dest_ids:
                move_dest_exists = True
            product_return_moves_data = dict(product_return_moves_data_tmpl)
            product_return_moves_data.update(
                self._prepare_stock_return_picking_line_vals_from_move(move))
            print('product_return_moves_data=', product_return_moves_data)
            if product_return_moves_data and not move.product_id.return_security:
                product_return_moves.append((0, 0, product_return_moves_data))
        if self.picking_id and not product_return_moves:
            raise UserError(
                _("No products to return (only lines in Done state and not fully returned yet can be returned)."))
        if self.picking_id:
            self.product_return_moves = product_return_moves
            self.move_dest_exists = move_dest_exists
            self.parent_location_id = self.picking_id.picking_type_id.warehouse_id and self.picking_id.picking_type_id.warehouse_id.view_location_id.id or self.picking_id.location_id.location_id.id
            self.original_location_id = self.picking_id.location_id.id
            location_id = self.picking_id.location_id.id
            if self.picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.return_location:
                location_id = self.picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.id
            self.location_id = location_id

    @api.model
    def _prepare_stock_return_picking_line_vals_from_move(self, stock_move):
        quantity = stock_move.product_qty
        for move in stock_move.move_dest_ids:
            if move.origin_returned_move_id and move.origin_returned_move_id != stock_move:
                continue
            if move.state in ('partially_available', 'assigned'):
                quantity -= sum(move.move_line_ids.mapped('product_qty'))
            elif move.state in ('done'):
                quantity -= move.product_qty
        quantity = float_round(quantity,
                               precision_rounding=stock_move.product_id.uom_id.rounding)
        if stock_move.product_id.return_security:
            return {'to_refund': False}
        else:
            return {
                'product_id': stock_move.product_id.id,
                'quantity': quantity,
                'move_id': stock_move.id,
                'uom_id': stock_move.product_id.uom_id.id,
            }
