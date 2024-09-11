""" Initialize Card Product Report """

from odoo import fields, models


class CardProductReport(models.TransientModel):
    """
        Initialize Card Product Report:
         - 
    """
    _name = 'card.product.report'
    _description = 'Card Product Report'

    date = fields.Date()
    picking_type_name = fields.Char()
    partner_code = fields.Char()
    partner_name = fields.Char()
    stock_picking_name = fields.Char()
    stock_name = fields.Char()
    product = fields.Char()
    quantity = fields.Float()
    price_unit = fields.Float()
    amount = fields.Float()
    balance = fields.Float()
    amount_balance = fields.Float()
    source_location = fields.Char()
    location_dest = fields.Char()
    operation_type = fields.Char()
