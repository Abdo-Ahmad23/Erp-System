""" Initialize Hr Payslip """

from odoo.exceptions import ValidationError

from odoo import _, fields, models


class HrPayslip(models.Model):
    """
        Inherit Hr Payslip:
         - 
    """
    _inherit = 'hr.payslip'

    payment_id = fields.Many2one(
        'account.payment'
    )

    def action_payslip_done(self):
        """ Override action_payslip_done """
        res = super(HrPayslip, self).action_payslip_done()
        self.create_payment()
        return res

    def create_payment(self):
        """ Create Payment """
        for rec in self:
            if rec.employee_id.journal_id:
                amount = rec.line_ids.filtered(
                    lambda
                        r: r.code == 'NET' and r.category_id.name == 'Net').total
                rec.payment_id = self.env['account.payment'].create(
                    {
                        'partner_id': rec.employee_id.address_home_id.id,
                        'journal_id': rec.employee_id.journal_id.id,
                        'payment_type': 'outbound',
                        'amount': amount
                    })
                if rec.employee_id.journal_id.type == 'bank':
                    rec.payment_id.action_post()

            else:
                raise ValidationError(_("Please Enter Journal in Employee"))

    def action_payslip_cancel(self):
        """ Override action_payslip_cancel """
        res = super(HrPayslip, self).action_payslip_cancel()
        if self.payment_id and self.payment_id.state != 'draft':
            self.payment_id.action_draft()
            self.payment_id.unlink()
        else:
            self.payment_id.unlink()
        self.write({'payment_id': False})
        return res

    def action_view_account_payment(self):
        """ :return Account Payment action """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'name': _('Account Payment'),
            'view_mode': 'form',
            # 'context': {'form_view_initial_mode': 'edit',},
            'domain': [],
            'res_id': self.payment_id.id,
            'views': [(False, 'form')],
        }
