from odoo import models, fields

class Product(models.Model):
    _name = 'product'
    _description = 'Product Name'

    name=fields.Char(string='Product Name')
    brand_id=fields.Many2one('brand',string='Brand') 
    category_id=fields.Many2one('category',string='Categories')
    model_year=fields.Char(string='Model Year')
    price=fields.Float(string='Price')
    