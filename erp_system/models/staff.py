from odoo import fields,models, api, exceptions
import re

class Staff(models.Model):
    _name='staff'
    _rec_name='first_name'

    first_name=fields.Char(string='First Name')
    second_name=fields.Char(string='Second Name')
    phone=fields.Char(string='Phone')
    email=fields.Char(string='Email')
    active=fields.Boolean(string='Active',default=True)
    store_id=fields.Many2one('store',string='Stores')
    manager_id = fields.Many2one(
        'staff',  # This is the recursive relationship
        string='Manager',
        ondelete='restrict'
    )
    

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not self._is_valid_email(record.email):
                raise exceptions.ValidationError("Invalid email address: %s" % record.email)

    @staticmethod
    def _is_valid_email(email):
        """Check if the email is valid using a regular expression."""
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(email_regex, email) is not None