from odoo import fields,models, api, exceptions
import re

class Customer(models.Model):
    _name='customer'
    _rec_name='first_name'

    first_name=fields.Char(string='First Name')
    second_name=fields.Char(string='Second Name')
    phone=fields.Char(string='Phone')
    email=fields.Char(string='Email')
    street=fields.Char(string='Street')
    city=fields.Char(string='City')
    state=fields.Char(string='State')
    zip_code=fields.Char(string='Zip Code')



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