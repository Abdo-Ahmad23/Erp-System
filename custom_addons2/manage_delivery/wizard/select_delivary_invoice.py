# -*- coding: utf-8 -*-
""" Select Delivary Invoice """
from odoo import api, fields, models


class SelectDeliveryInvoice(models.TransientModel):
    """ Select Delivery Invoice """
    _name = 'select.delivery.invoice'
    _description = 'Select Delivery Invoice'

    delivery_invoice_lines_ids = fields.One2many('delivery.invoice.lines',
                                                 'select_delivery_invoice_id')

    def confirm(self):
        """ Create Pricing """
        active_id = self._context.get('active_id')
        manage_delivery = self.env['manage.delivery'].browse(active_id)
        moves = []
        for rec in self.delivery_invoice_lines_ids:
            if rec.select:
                moves.append((0, 0,
                              {'account_move_id': rec.account_move_id.id,
                               'partner_id': rec.partner_id.id,
                               'street': rec.street,
                               'zone': rec.zone,
                               'mobile': rec.mobile,
                               'amount': rec.amount,
                               'delivery_boy': manage_delivery.delivery_boy.id
                               }))

        manage_delivery.write(
            {'manage_delivery_liens_ids': moves
             })
        for m in self.delivery_invoice_lines_ids:
            m.account_move_id.delivery_moves = True


class DeliveryInvoiceLines(models.TransientModel):
    """ Delivery Invoice Lines """
    _name = 'delivery.invoice.lines'
    _description = 'Delivery Invoice Lines'

    select_delivery_invoice_id = fields.Many2one('select.delivery.invoice')
    account_move_id = fields.Many2one('account.move',
                                      domain=[('delivery_status', '=', '2')])
    partner_id = fields.Many2one('res.partner')
    street = fields.Char()
    zone = fields.Char()
    mobile = fields.Char()
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    delivery_boy = fields.Many2one('res.partner')
    select = fields.Boolean()
