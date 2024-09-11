""" Initialize Tax Statement Wizard """

from odoo import _, fields, models


class CardProductWizard(models.TransientModel):
    """
        Initialize  Card Product Wizard:
         -
    """
    _name = 'card.product.wizard'
    _description = 'Model Card Wizard'

    date_from = fields.Date(
        required=True
    )
    date_to = fields.Date(
        required=True
    )
    product_ids = fields.Many2many(
        'product.product', required=True
    )

    def confirm(self):
        """ Confirm Report """
        records = self.env['stock.move'].search(
            [('picking_id.date_done', '>=', self.date_from),
             ('picking_id.date_done', '<=', self.date_to),
             ('picking_type_id.code', 'in', ['outgoing', 'incoming', 'internal']),
             ('picking_id.state', '=', 'done'),
             ('product_id', 'in', self.product_ids.ids)],
            order='product_id,picking_type_id'
        )
        if records:
            self.env['card.product.report'].search([]).unlink()
            stock_name = ''
            balance = amount_balance = amount = quantity = price_unit = 0
            for rec in records:
                if rec.account_move_ids:
                    for move in rec.account_move_ids:
                        if rec.picking_type_id.code == 'outgoing':
                            amount = sum(move.line_ids.mapped('credit'))
                            quantity = rec.quantity_done
                            price_unit = amount / quantity
                            balance -= quantity
                            amount_balance -= amount
                            stock_name = rec.location_id.name
                        elif rec.picking_type_id.code == 'incoming':
                            amount = sum(move.line_ids.mapped('debit'))
                            price_unit = amount / rec.quantity_done
                            quantity = rec.quantity_done
                            balance += quantity
                            amount_balance += amount
                            stock_name = rec.location_dest_id.name

                        elif rec.picking_type_id.code == 'internal':
                            amount = sum(move.line_ids.mapped('debit'))
                            price_unit = amount / rec.quantity_done
                            quantity = rec.quantity_done
                            balance += quantity
                            amount_balance += amount
                            stock_name = rec.location_dest_id.name

                    self.create_card_product_report(amount, amount_balance,
                                                    balance, price_unit,
                                                    quantity, rec, stock_name)
                else:
                    if rec.picking_type_id.code == 'outgoing':
                        quantity = rec.quantity_done
                        balance -= quantity
                        stock_name = rec.location_id.name
                        price_unit = 0
                        amount = 0
                    elif rec.picking_type_id.code == 'incoming':
                        quantity = rec.quantity_done
                        balance += quantity
                        stock_name = rec.location_dest_id.name
                        price_unit = 0
                        amount = 0
                    elif rec.picking_type_id.code == 'internal':
                        quantity = rec.quantity_done
                        balance += quantity
                        stock_name = rec.location_dest_id.name
                        price_unit = rec.product_id.standard_price
                        amount = quantity * rec.product_id.standard_price

                    self.create_card_product_report(amount, amount_balance,
                                                    balance, price_unit,
                                                    quantity, rec, stock_name)
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'card.product.report',
                'name': _('Card Product Report'),
                'context': {'search_default_group_product': 1},
                'view_mode': 'tree',
            }

    def create_card_product_report(self, amount, amount_balance, balance,
                                   price_unit, quantity, rec, stock_name):
        self.env['card.product.report'].create({
            'date': rec.picking_id.date_done,
            'picking_type_name':
                dict(rec.picking_type_id.fields_get(allfields=['code'])[
                         'code'][
                         'selection'])[rec.picking_type_id.code],
            'partner_code': rec.partner_id.ref,
            'partner_name': rec.partner_id.name,
            'stock_picking_name': rec.picking_id.name,
            'stock_name': stock_name,
            'product': rec.product_id.name,
            'quantity': quantity,
            'price_unit': price_unit,
            'amount': amount,
            'balance': balance,
            'source_location': rec.location_id.name,
            'location_dest': rec.location_dest_id.name,
            'operation_type': rec.picking_type_id.name,
            'amount_balance': amount_balance,
        })
