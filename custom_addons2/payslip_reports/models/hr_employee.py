""" Initialize Hr Employee """

from odoo.exceptions import ValidationError

from odoo import _, api, fields, models


class HrEmployee(models.Model):
    """
        Inherit Hr Employee:
         -
    """
    _inherit = 'hr.employee'

    branch = fields.Char()
    bank_id = fields.Char(string='Bank ID')
    bank_account = fields.Char()

    @api.constrains('branch')
    def _check_branch(self):
        """ Validate branch """
        for rec in self:
            if rec.branch:
                if not rec.branch.isdigit():
                    raise ValidationError(_("Branch Must be Number"))

    @api.constrains('bank_id')
    def _check_bank_id(self):
        """ Validate bank_id """
        for rec in self:
            if rec.bank_id:
                if not rec.bank_id.isdigit():
                    raise ValidationError(_("Bank Id Must be Number"))

    @api.constrains('bank_account')
    def _check_bank_account(self):
        """ Validate bank_account """
        for rec in self:
            if rec.bank_account:
                if not rec.bank_account.isdigit():
                    raise ValidationError(_("Bank Account Must be Number"))


class HrEmployeePublic(models.Model):
    """
        Inherit Hr Employee Public:
         -
    """
    _inherit = 'hr.employee.public'

    branch = fields.Char()
    bank_id = fields.Char(string='Bank ID')
    bank_account = fields.Char()
