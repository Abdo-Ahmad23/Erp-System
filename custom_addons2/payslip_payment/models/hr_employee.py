""" Initialize Hr Employee """

from odoo import fields, models


class HrEmployee(models.Model):
    """
        Inherit Hr Employee:
         -
    """
    _inherit = 'hr.employee'

    journal_id = fields.Many2one(
        'account.journal', domain="[('type', 'in', ('cash','bank'))]"
    )
    fellowship_fund = fields.Boolean()


class HrEmployeePublic(models.Model):
    """
        Inherit Hr Employee Public:
         -
    """
    _inherit = 'hr.employee.public'

    journal_id = fields.Many2one(
        'account.journal', domain="[('type', 'in', ('cash','bank'))]"
    )
    fellowship_fund = fields.Boolean()
