from odoo import models,fields,api

class InheritClass(models.Model):
    _inherit='sale.order'


    new_field=fields.Char(string='New Field')



