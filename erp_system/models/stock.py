from odoo import fields,models

class Stock(models.Model):
    _name='stock'
    _description='stock description'

    name=fields.Char(string='Stock Name')
    product_ids=fields.Many2many('product',string='Products')
    store_ids=fields.Many2many('store',string='Stores')