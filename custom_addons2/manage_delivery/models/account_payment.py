# -*- coding: utf-8 -*-
""" Account Payment """
from odoo import fields, models, _


class AccountPayment(models.Model):
    """ inherit Account Payment """
    _inherit = 'account.payment'

    from_delivery_move = fields.Boolean()
    delivery_boy = fields.Many2one('res.partner')
