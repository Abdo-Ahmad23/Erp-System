from odoo import models, fields


class Tag(models.Model):
    _name = "tag"

    name = fields.Char(string="Tag", required=True)
