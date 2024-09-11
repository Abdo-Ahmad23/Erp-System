from odoo import models, fields , api

class Loan(models.Model):
    _name = 'loan.loan'
    _description = 'Loan'

    name = fields.Char(string='Loan Name', required=True)
    amount = fields.Float(string='Loan Amount', required=True)
    interest_rate = fields.Float(string='Interest Rate', required=True)
    tenure = fields.Integer(string='Tenure (in months)', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('closed', 'Closed'),], string='Status', default='pending')
    applicant_id = fields.Many2one('res.partner', string='Applicant')

    def _compute_end_date(self):
        for loan in self:
            loan.end_date = loan.start_date + relativedelta(months=loan.tenure)

    @api.model
    def _get_loan_default_domain(self):
        return [('state', '=', 'open')]

    @api.model
    def action_loan_list(self):
        action = self.env.ref('loan_good.action_loans')
        result = action.read()[0]
        domain = self._get_loan_default_domain()
        result['domain'] = domain
        return result