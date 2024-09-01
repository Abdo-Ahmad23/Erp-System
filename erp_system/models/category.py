from odoo import models, fields

class Category(models.Model):
    _name = 'category'
    _description = 'Category Name'

    name=fields.Char(string='Category Name')
    