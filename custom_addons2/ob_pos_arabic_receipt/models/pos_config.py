from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_arabic_receipt = fields.Boolean(string="Enable Arabic Receipt", default=False)
    receipt_design_id = fields.Many2one('arabic.receipt', string="Receipt Design")

    @api.onchange('enable_arabic_receipt')
    def _onchange_enable_arabic_receipt(self):
        if self.enable_arabic_receipt:
            receipt_design = self.env['arabic.receipt'].search([])
            self.receipt_design_id = receipt_design.id
