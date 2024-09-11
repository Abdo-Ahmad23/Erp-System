""" Initialize Res Partner """

from odoo.exceptions import ValidationError

from odoo import _, api, fields, models


class ResPartner(models.Model):
    """
        Inherit Res Partner:
         -
    """
    _inherit = 'res.partner'

    mobile_2 = fields.Char()
    mobile_3 = fields.Char()
    mobile_4 = fields.Char()
    mobile_5 = fields.Char()
    special_marque = fields.Char()
    customer_code = fields.Char()
    stock_warehouse_id = fields.Many2one(
        'stock.warehouse'
    )
    partner_zone_id = fields.Many2one(
        'partner.zone', string='Zone'
    )

    @api.constrains('mobile')
    def _check_mobile_1(self):
        """ Validate mobile_1 """
        if self.mobile:
            if self.mobile not in [self.mobile_2, self.mobile_3, self.mobile_4, self.mobile_5]:
                mobile = self.env['res.partner'].search(
                    [('mobile', '=', self.mobile), ('id', '!=', self.id)], limit=1)
                mobile_2 = self.env['res.partner'].search(
                    [('mobile_2', '=', self.mobile), ('id', '!=', self.id)], limit=1)
                mobile_3 = self.env['res.partner'].search(
                    [('mobile_3', '=', self.mobile), ('id', '!=', self.id)], limit=1)
                mobile_4 = self.env['res.partner'].search(
                    [('mobile_4', '=', self.mobile), ('id', '!=', self.id)], limit=1)
                mobile_5 = self.env['res.partner'].search(
                    [('mobile_5', '=', self.mobile), ('id', '!=', self.id)], limit=1)
                if mobile:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile))
                if mobile_2:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile))
                if mobile_3:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile))
                if mobile_4:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile))
                if mobile_5:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile))
            else:
                raise ValidationError(
                    _('This mobile number  %s is already exists' % self.mobile))

    @api.constrains('mobile_2')
    def _check_mobile_2(self):
        """ Validate mobile_2 """
        if self.mobile_2:
            if self.mobile_2 not in [self.mobile, self.mobile_3, self.mobile_4, self.mobile_5]:
                mobile = self.env['res.partner'].search(
                    [('mobile', '=', self.mobile_2), ('id', '!=', self.id)], limit=1)
                mobile_2 = self.env['res.partner'].search(
                    [('mobile_2', '=', self.mobile_2), ('id', '!=', self.id)], limit=1)
                mobile_3 = self.env['res.partner'].search(
                    [('mobile_3', '=', self.mobile_2), ('id', '!=', self.id)], limit=1)
                mobile_4 = self.env['res.partner'].search(
                    [('mobile_4', '=', self.mobile_2), ('id', '!=', self.id)], limit=1)
                mobile_5 = self.env['res.partner'].search(
                    [('mobile_5', '=', self.mobile_2), ('id', '!=', self.id)], limit=1)
                if mobile:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_2))
                if mobile_2:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_2))
                if mobile_3:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_2))
                if mobile_4:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_2))
                if mobile_5:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_2))
            else:
                raise ValidationError(
                    _('This mobile number  %s is already exists' % self.mobile_2))

    @api.constrains('mobile_3')
    def _check_mobile_3(self):
        """ Validate mobile_1 """
        if self.mobile_3:
            if self.mobile_3 not in [self.mobile, self.mobile_2, self.mobile_4, self.mobile_5]:
                mobile = self.env['res.partner'].search(
                    [('mobile', '=', self.mobile_3), ('id', '!=', self.id), ('id', '!=', self.id)], limit=1)
                mobile_2 = self.env['res.partner'].search(
                    [('mobile_2', '=', self.mobile_3), ('id', '!=', self.id), ('id', '!=', self.id)], limit=1)
                mobile_3 = self.env['res.partner'].search(
                    [('mobile_3', '=', self.mobile_3), ('id', '!=', self.id), ('id', '!=', self.id)], limit=1)
                mobile_4 = self.env['res.partner'].search(
                    [('mobile_4', '=', self.mobile_3), ('id', '!=', self.id), ('id', '!=', self.id)], limit=1)
                mobile_5 = self.env['res.partner'].search(
                    [('mobile_5', '=', self.mobile_3), ('id', '!=', self.id), ('id', '!=', self.id)], limit=1)
                if mobile:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_3))
                if mobile_2:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_3))
                if mobile_3:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_3))
                if mobile_4:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_3))
                if mobile_5:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_3))
            else:
                raise ValidationError(
                    _('This mobile number  %s is already exists' % self.mobile_3))

    @api.constrains('mobile_4')
    def _check_mobile_4(self):
        """ Validate mobile_4 """
        if self.mobile_4:
            if self.mobile_4 not in [self.mobile, self.mobile_2, self.mobile_3, self.mobile_5]:
                mobile = self.env['res.partner'].search(
                    [('mobile', '=', self.mobile_4), ('id', '!=', self.id)], limit=1)
                mobile_2 = self.env['res.partner'].search(
                    [('mobile_2', '=', self.mobile_4), ('id', '!=', self.id)], limit=1)
                mobile_3 = self.env['res.partner'].search(
                    [('mobile_3', '=', self.mobile_4), ('id', '!=', self.id)], limit=1)
                mobile_4 = self.env['res.partner'].search(
                    [('mobile_4', '=', self.mobile_4), ('id', '!=', self.id)], limit=1)
                mobile_5 = self.env['res.partner'].search(
                    [('mobile_5', '=', self.mobile_4), ('id', '!=', self.id)], limit=1)
                if mobile:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_4))
                if mobile_2:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_4))
                if mobile_3:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_4))
                if mobile_4:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_4))
                if mobile_5:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_4))
            else:
                raise ValidationError(
                    _('This mobile number  %s is already exists' % self.mobile_4))

    @api.constrains('mobile_5')
    def _check_mobile_5(self):
        """ Validate mobile_5 """
        if self.mobile_5:
            if self.mobile_5 not in [self.mobile_2, self.mobile_3, self.mobile_4, self.mobile]:
                mobile = self.env['res.partner'].search(
                    [('mobile', '=', self.mobile_5), ('id', '!=', self.id)], limit=1)
                mobile_2 = self.env['res.partner'].search(
                    [('mobile_2', '=', self.mobile_5), ('id', '!=', self.id)], limit=1)
                mobile_3 = self.env['res.partner'].search(
                    [('mobile_3', '=', self.mobile_5), ('id', '!=', self.id)], limit=1)
                mobile_4 = self.env['res.partner'].search(
                    [('mobile_4', '=', self.mobile_5), ('id', '!=', self.id)], limit=1)
                mobile_5 = self.env['res.partner'].search(
                    [('mobile_5', '=', self.mobile_5), ('id', '!=', self.id)], limit=1)
                if mobile:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_5))
                if mobile_2:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_5))
                if mobile_3:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_5))
                if mobile_4:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_5))
                if mobile_5:
                    raise ValidationError(
                        _('This mobile number  %s is with one of the clients' % self.mobile_5))
            else:
                raise ValidationError(
                    _('This mobile number  %s is already exists' % self.mobile_5))


class PartnerZone(models.Model):
    """
        Initialize Partner Zone:
         -
    """
    _name = 'partner.zone'
    _description = 'Partner Zone'
    _check_company_auto = True

    name = fields.Char(
        required=True,
        translate=True,
    )
    code = fields.Char(
    )
