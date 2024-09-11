""" Initialize Building Type """

from odoo import fields, models


class BuildingType(models.Model):
    """
        Initialize Building Type:
         -
    """
    _name = 'building.type'
    _description = 'Building Type'
    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True,
    )
