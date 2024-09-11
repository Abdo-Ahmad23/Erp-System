""" Initialize Res Users """

from odoo.exceptions import ValidationError

from odoo import api, fields, models


class ResUsers(models.Model):
    """
        Inherit Res Users:
         - 
    """
    _inherit = 'res.users'

    identification_number = fields.Char(
        string="National ID", size=14,
        related='partner_id.identification_number',
        inherited=True, readonly=False
    )
    transportation = fields.Selection(
        [('car', 'Car'), ('motorcycle', 'Motorcycle'), ('bike', 'Bike')],
        related='partner_id.transportation', inherited=True, readonly=False
    )
    is_delivery_boy = fields.Boolean(
        related='partner_id.is_delivery_boy', inherited=True, readonly=False
    )
    commission_fees = fields.Float(
        related='partner_id.commission_fees', inherited=True, readonly=False
    )

    @api.constrains('identification_number')
    def _check_identification_number(self):
        for record in self:
            if record.identification_number:
                if len(record.identification_number) != 14:
                    raise ValidationError(
                        "Identification ID must be 14 numbers")
                if not record.identification_number.isdigit():
                    raise ValidationError(
                        "Identification ID must be numbers only")
