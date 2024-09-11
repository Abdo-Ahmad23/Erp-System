# -*- coding: utf-8 -*-
""" Manage Delivery """
from odoo import api, fields, models, _


class ManageDelivery(models.Model):
    """ Manage Delivery """
    _name = 'manage.delivery'
    _description = 'Manage Delivery'

    name = fields.Char(default='NEW')
    manage_delivery_liens_ids = fields.One2many('manage.delivery.liens',
                                                'manage_delivery_id')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirm'), ('arrived', 'Arrived')],
        default='draft',
        string='Status'
    )
    delivery_boy = fields.Many2one('res.partner', domain=[('is_delivery_boy', '=', True)])
    date = fields.Datetime()
    transportation = fields.Selection(
        [('1', 'Car'), ('2', 'Motorcycle'), ('3', 'Bike')])
    arrived_date = fields.Datetime()
    mobile = fields.Char()
    plate_number = fields.Char()

    @api.onchange('transportation')
    def _onchange_transportation(self):
        """ Add domain to some filed """
        self.delivery_boy = False
        if self.transportation:
            return {'domain': {
                'delivery_boy': [('transportation', '=', self.transportation)]
            }}

    def select_delivery_invoice(self):
        """ Select Delivery Invoice """
        moves = []
        lines = []
        inv = []
        moves = self.env['account.move'].search(
            [('delivery_status', '=', '2')])

        for n in self.manage_delivery_liens_ids:
            inv.append(n.account_move_id.id)
        for rec in moves:
            if not rec.delivery_moves:
                if rec.id not in inv:
                    lines.append((0, 0,
                                  {'account_move_id': rec.id,
                                   'partner_id': rec.partner_id.id,
                                   'street': rec.street,
                                   'zone': rec.zone,
                                   'mobile': rec.mobile,
                                   'amount': rec.amount_total,
                                   'delivery_boy': self.delivery_boy.id
                                   }))
        action = \
            self.env.ref(
                'manage_delivery.select_delivery_invoice_action').read()[0]
        action['context'] = {
            'default_delivery_invoice_lines_ids': lines}

        action['views'] = [(self.env.ref(
            'manage_delivery.select_delivery_invoice_form').id, 'form')]
        return action

    @api.onchange('delivery_boy')
    def _onchange_delivery_boy(self):
        """ delivery_boy """
        if self.delivery_boy:
            for rec in self.manage_delivery_liens_ids:
                rec.delivery_boy = self.delivery_boy
            self.mobile = self.delivery_boy.mobile
            self.plate_number = self.delivery_boy.plate_number

    def confirm(self):
        """ Confirm """
        self.state = 'confirm'
        self.date = fields.Datetime.now()
        for rec in self.manage_delivery_liens_ids:
            rec.parent_state = 'confirm'
            rec.account_move_id.delivery_boy = self.delivery_boy.id
            rec.account_move_id.send_date = self.date
            rec.account_move_id.transportation = self.transportation

    def arrived(self):
        """ Arrived """
        self.state = 'arrived'
        self.arrived_date = fields.Datetime.now()
        for rec in self.manage_delivery_liens_ids:
            rec.account_move_id.arrived_date = self.arrived_date
            rec.parent_state = 'arrived'

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'manage.delivery') or '/'
        return super(ManageDelivery, self).create(vals)


class ManageDeliveryLiens(models.Model):
    """ Manage Delivery Liens """
    _name = 'manage.delivery.liens'
    _description = 'Manage Delivery Liens'

    manage_delivery_id = fields.Many2one('manage.delivery')
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
    parent_state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirm'), ('arrived', 'Arrived')],
        default='draft',
        string='Status'
    )
    state = fields.Selection(
        [('1', 'Draft'),
         ('2', 'Delivered'), ('3', 'Not Delivered')],
        default='1',
        string='Status'
    )
    delivery_boy = fields.Many2one('res.partner')

    @api.onchange('account_move_id')
    def _onchange_account_move(self):
        """ account_move_id """
        if self.account_move_id:
            self.partner_id = self.account_move_id.partner_id.id
            self.street = self.account_move_id.street
            self.zone = self.account_move_id.zone
            self.mobile = self.account_move_id.mobile
            self.amount = self.account_move_id.amount_total

    def delivery_status(self):
        """ Delivery Status """
        self.state = '2'
        self.account_move_id.delivery_status = '3'

    def not_arrived(self):
        """ Not Arrived """
        self.state = '3'
        self.account_move_id.delivery_status = '2'
        self.account_move_id.delivery_moves = False
