# -*- coding: utf-8 -*-
""" Res Partner """
from odoo import fields, models


class ResPartner(models.Model):
    """ inherit Res Partner """
    _inherit = 'res.partner'

    zone = fields.Char()
    building_floor = fields.Char(string="Building/Floor")
    special_mark = fields.Char()
    area_region = fields.Char(string="Area/Region")
    is_delivery_boy = fields.Boolean()
    national = fields.Char(string="National ID")
    transportation = fields.Selection(
        [('1', 'Car'), ('2', 'Motorcycle'), ('3', 'Bike')])
    plate_number = fields.Char()
