from odoo import fields,models

class Employee(models.Model):
    _name='employee'


    name=fields.Char(string="Name")
    