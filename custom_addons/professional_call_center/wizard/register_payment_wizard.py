""" Initialize Register Payment Wizard """

from odoo import fields, models


class RegisterPaymentWizard(models.TransientModel):
    """
        Initialize Register Payment Wizard:
         -
    """
    _name = 'register.payment.wizard'
    _description = 'Register Payment Wizard'

    amount = fields.Float()
    paid_amount = fields.Float(
        related='call_center_order_id.paid_amount', readonly=True
    )
    call_center_order_id = fields.Many2one(
        'call.center.order'
    )

    def paid_action(self):
        """ Paid Action """
        self.call_center_order_id.write({
            'paid_amount': self.call_center_order_id.paid_amount + self.amount,
            'prepaid': True
        })
