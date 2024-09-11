""" Initialize Pos Payment """

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class PosPayment(models.Model):
    """
        Inherit Pos Payment:
         - 
    """
    _inherit = 'pos.payment'

    batch_number = fields.Char()
    machine_number = fields.Char()
