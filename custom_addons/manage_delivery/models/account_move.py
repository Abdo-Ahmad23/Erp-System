# -*- coding: utf-8 -*-
""" Account Move """
from odoo import api, fields, models


class AccountMove(models.Model):
    """ inherit Account Move """
    _inherit = 'account.move'

    delivery_status = fields.Selection(
        [('1', 'Draft'), ('2', 'Send To Delivery'), ('3', 'Delivered'),
         ('4', 'Not Delivered')], default='1')
    delivery_boy = fields.Many2one('res.partner')
    street = fields.Char()
    zone = fields.Char()
    building_floor = fields.Char(string="Building/Floor")
    special_mark = fields.Char()
    area_region = fields.Char(string="Area/Region")
    mobile = fields.Char()
    transportation = fields.Selection(
        [('1', 'Car'), ('2', 'Motorcycle'), ('3', 'Bike')])
    send_date = fields.Datetime()
    arrived_date = fields.Datetime()
    delivery_moves = fields.Boolean()
    stock_picking_id = fields.Many2one('stock.picking')

    @api.onchange('partner_id')
    def _onchange_partner_address(self):
        """ partner_id """
        if self.partner_id:
            self.street = self.partner_id.street
            self.zone = self.partner_id.zone
            self.building_floor = self.partner_id.building_floor
            self.special_mark = self.partner_id.special_mark
            self.area_region = self.partner_id.area_region
            self.mobile = self.partner_id.mobile

    def send_to_delivery(self):
        """ Send To Delivery """
        self.delivery_status = '2'
