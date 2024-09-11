""" Initialize Res Users """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class ResUsers(models.Model):
    """
        Inherit Res Users:
         -
    """
    _inherit = 'res.users'

    journal_ids = fields.Many2many(
        'account.journal'
    )
    allowed_journal_ids = fields.Many2many(
        'account.journal',
        compute='_compute_allowed_journal_ids'
    )

    @api.depends('journal_ids')
    def _compute_allowed_journal_ids(self):
        """ Compute allowed_journal_ids value """
        for rec in self:
            if rec.has_group('pcp_journal_restrictions.group_restrict_journal'):
                rec.allowed_journal_ids = self.env['account.journal'].search([('id', 'in', rec.journal_ids.ids)])

            else:
                rec.allowed_journal_ids = self.env['account.journal'].search([])
