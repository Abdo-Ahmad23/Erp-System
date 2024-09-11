# -*- coding: utf-8 -*-
""" Delivery Boy """
from odoo import fields, models


class DeliveryBoy(models.Model):
    """ Delivery Boy """
    _name = 'delivery.boy'
    _description = 'Delivery Boy'

    name = fields.Char()
    national = fields.Char(string="National ID")
    mobile = fields.Char()
    image = fields.Binary()
    transportation = fields.Selection(
        [('1', 'Car'), ('2', 'Motorcycle'), ('3', 'Bike')])
