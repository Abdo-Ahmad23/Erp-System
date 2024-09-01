from odoo import models, fields

class Brand(models.Model):
    _name = 'brand'
    _description = 'Brand Name'

    name=fields.Char(string='Brand Name')