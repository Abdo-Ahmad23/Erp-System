import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Timesheet(models.Model):
    _inherit = "account.analytic.line"
    payslip_id = fields.Many2one('hr.payslip', 'Payslip')
