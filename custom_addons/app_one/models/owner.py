from odoo import models, fields


class Owner(models.Model):
    _name = "owner"

    name = fields.Char(string="Owner", required=True)
    phone = fields.Char(string="Phone", required=True)
    address = fields.Char(string="Address")
    property_ids = fields.One2many('property', 'owner_id')
