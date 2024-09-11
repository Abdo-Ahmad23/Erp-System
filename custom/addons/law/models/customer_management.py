from odoo import models,fields,api

class CustomerManagement(models.Model):
    _name='customers'
    _description='Customer Management'
    _inherit='lawyers'
    # name=fields.Char(string='Name')
    # age=fields.Integer(string='Age')
    # date=fields.Date(string='Date')