""" Initialize Account Payment """

# from odoo import fields, models
from odoo import models, fields, api


class AccountPayment(models.Model):
    """
        Inherit Account Payment:
         -
    """
    _inherit = 'account.payment'

    delivery_boy_bill = fields.Boolean()
    delivery_customer_invoice = fields.Boolean()


class AccountPaymentRegister(models.TransientModel):
    """
        Inherit Account Payment Register:
         -
    """
    _inherit = 'account.payment.register'

    delivery_boy_bill = fields.Boolean()

    def _create_payments(self):
        """ Override _create_payments """
        res = super(AccountPaymentRegister, self)._create_payments()
        
        account_move_ids = self.env['account.move'].browse(self._context.get('active_ids', []))
       
        for move in account_move_ids:
            if move.delivery_boy_bill:
                res.write({'delivery_boy_bill': move.delivery_boy_bill})
            if move.call_center_order_id and \
                    move.delivery_state == 'delivery_collection':
                res.write({'delivery_customer_invoice': True})
        return res