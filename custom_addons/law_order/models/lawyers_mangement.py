
from odoo import  fields, models ,api


class LawyersManagement(models.Model):

    _name = 'lawyers'
    _description = 'Lawyers Management'

    name = fields.Char(string='Name', default="Hashem")
    national_id = fields.Char(string='National ID', default="300026389437526")
