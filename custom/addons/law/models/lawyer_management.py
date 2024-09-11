from odoo import models, fields,api
from odoo.exceptions import ValidationError
from datetime import date,datetime

class LawyerManagement(models.Model):
    _name = 'lawyers'
    _description = 'Lawyer Management'
    lawyer_id=fields.Many2one('res.users',string='Lawyer')


    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string="Age",compute='compute_age')
    date=fields.Date(string="Date of Birth")
    notes=fields.Text(string='Notes')

    @api.depends('date')
    def compute_age(self):
        for rec in self:
            today=date.today()
            if rec.date:
                rec.age=today.year-rec.date.year
            else:
                rec.age=18