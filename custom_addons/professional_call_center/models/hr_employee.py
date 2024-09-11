""" Initialize Hr Employee """

from odoo import fields, models


class HrEmployee(models.Model):
    """
        Inherit Hr Employee:
         -
    """
    _inherit = 'hr.employee'

    is_call_center = fields.Boolean()
