# -*- coding: utf-8 -*-
""" Sale Order """
from odoo import api, fields, models


class SaleOrder(models.Model):
    """ inherit Sale Order """
    _inherit = 'sale.order'

    street = fields.Char()
    zone = fields.Char()
    building_floor = fields.Char(string="Building/Floor")
    special_mark = fields.Char()
    area_region = fields.Char(string="Area/Region")
    mobile = fields.Char()
    hr_employee_id = fields.Many2one('hr.employee', string="Call Center Agent")
    other_type = fields.Selection([('1', 'From Branch'), ('2', 'Home Delivery'), ('3', 'Other'), ])
    delivery_date_time = fields.Datetime(string="Delivery Date & Time")
    branch_warehouse_id = fields.Many2one('stock.warehouse', string="Brunch")

    @api.onchange('partner_id', 'mobile', 'customer_code')
    def _onchange_partner_information_mob(self):
        """ partner_id """
        if self.partner_id:
            self.special_mark = self.partner_id.special_mark
            self.area_region = self.partner_id.area_region
            self.building_floor = self.partner_id.building_floor
            self.zone = self.partner_id.zone
            self.street = self.partner_id.street
            self.customer_code = self.partner_id.customer_code
            if self.partner_id.stock_warehouse_id:
                self.warehouse_id = self.partner_id.stock_warehouse_id.id
            if self.mobile and self.partner_id.mobile:
                self.mobile = self.mobile
            else:
                self.mobile = self.partner_id.mobile
        elif self.customer_code:
            customer_code = self.env['res.partner'].search(
                [('customer_code', '=', self.customer_code)], limit=1)
            self.partner_id = customer_code.id
            if self.mobile and customer_code.mobile:
                self.mobile = self.mobile
            else:
                self.mobile = customer_code.mobile
            self.special_mark = customer_code.special_mark
            self.area_region = customer_code.area_region
            self.zone = customer_code.zone
            self.building_floor = customer_code.building_floor
            self.street = customer_code.street
            if self.partner_id.stock_warehouse_id:
                self.warehouse_id = self.partner_id.stock_warehouse_id.id

        elif self.mobile:
            mobile = self.env['res.partner'].search(
                [('mobile', '=', self.mobile)], limit=1)
            mobile_2 = self.env['res.partner'].search(
                [('mobile_2', '=', self.mobile)], limit=1)
            mobile_3 = self.env['res.partner'].search(
                [('mobile_3', '=', self.mobile)], limit=1)
            mobile_4 = self.env['res.partner'].search(
                [('mobile_4', '=', self.mobile)], limit=1)
            mobile_5 = self.env['res.partner'].search(
                [('mobile_5', '=', self.mobile)], limit=1)
            if self.mobile == mobile.mobile:
                print("partner:", mobile.id, mobile.special_mark,
                      mobile.area_region, mobile.zone, mobile.building_floor,
                      mobile.street, mobile.customer_code)
                self.partner_id = mobile.id
                self.mobile = mobile.mobile
                self.special_mark = mobile.special_mark
                self.area_region = mobile.area_region
                self.zone = mobile.zone
                self.building_floor = mobile.building_floor
                self.street = mobile.street
                self.customer_code = mobile.customer_code
                if self.partner_id.stock_warehouse_id:
                    self.warehouse_id = self.partner_id.stock_warehouse_id.id

            elif self.mobile == mobile_2.mobile_2:
                self.partner_id = mobile_2.id
                self.mobile = mobile_2.mobile_2
                self.special_mark = mobile_2.special_mark
                self.area_region = mobile_2.area_region
                self.zone = mobile_2.zone
                self.building_floor = mobile_2.building_floor
                self.street = mobile_2.street
                self.customer_code = mobile_2.customer_code
                if self.partner_id.stock_warehouse_id:
                    self.warehouse_id = self.partner_id.stock_warehouse_id.id
            elif self.mobile == mobile_3.mobile_3:
                self.partner_id = mobile_3.id
                self.mobile = mobile_3.mobile_3
                self.special_mark = mobile_3.special_mark
                self.area_region = mobile_3.area_region
                self.zone = mobile_3.zone
                self.building_floor = mobile_3.building_floor
                self.street = mobile_3.street
                self.customer_code = mobile_3.customer_code
                if self.partner_id.stock_warehouse_id:
                    self.warehouse_id = self.partner_id.stock_warehouse_id.id

            elif self.mobile == mobile_4.mobile_4:
                self.partner_id = mobile_4.id
                self.mobile = mobile_4.mobile_4
                self.special_mark = mobile_4.special_mark
                self.area_region = mobile_4.area_region
                self.zone = mobile_4.zone
                self.building_floor = mobile_4.building_floor
                self.street = mobile_4.street
                self.customer_code = mobile_4.customer_code
                if self.partner_id.stock_warehouse_id:
                    self.warehouse_id = self.partner_id.stock_warehouse_id.id
            elif self.mobile == mobile_5.mobile_5:
                self.partner_id = mobile_5.id
                self.mobile = mobile_5.mobile_5
                self.special_mark = mobile_5.special_mark
                self.area_region = mobile_5.area_region
                self.zone = mobile_5.zone
                self.building_floor = mobile_5.building_floor
                self.street = mobile_5.street
                self.customer_code = mobile_5.customer_code
                if self.partner_id.stock_warehouse_id:
                    self.warehouse_id = self.partner_id.stock_warehouse_id.id

    @api.onchange('customer_code')
    def _onchange_customer_code_info(self):
        """ customer_code """
        if self.customer_code:
            customer_code = self.env['res.partner'].search(
                [('customer_code', '=', self.customer_code)], limit=1)
            self.partner_id = customer_code.id
            if self.mobile:
                self.mobile = self.mobile
            else:
                self.mobile = customer_code.mobile
            self.special_mark = customer_code.special_mark
            self.area_region = customer_code.area_region
            self.zone = customer_code.zone
            self.building_floor = customer_code.zone
            self.street = customer_code.street

    @api.onchange('mobile')
    def _onchange_mobile_info(self):
        """ mobile """
        if self.mobile:
            mobile = self.env['res.partner'].search(
                [('mobile', '=', self.mobile)], limit=1)
            mobile_2 = self.env['res.partner'].search(
                [('mobile_2', '=', self.mobile)], limit=1)
            mobile_3 = self.env['res.partner'].search(
                [('mobile_3', '=', self.mobile)], limit=1)
            mobile_4 = self.env['res.partner'].search(
                [('mobile_4', '=', self.mobile)], limit=1)
            mobile_5 = self.env['res.partner'].search(
                [('mobile_5', '=', self.mobile)], limit=1)
            if self.mobile == mobile.mobile:
                print("partner:", mobile.id, mobile.special_mark,
                      mobile.area_region, mobile.zone, mobile.building_floor,
                      mobile.street, mobile.customer_code)
                self.partner_id = mobile.id
                self.mobile = mobile.mobile
                self.special_mark = mobile.special_mark
                self.area_region = mobile.area_region
                self.zone = mobile.zone
                self.building_floor = mobile.building_floor
                self.street = mobile.street
                self.customer_code = mobile.customer_code

            elif self.mobile == mobile_2.mobile_2:
                self.partner_id = mobile_2.id
                self.mobile = mobile_2.mobile_2
                self.special_mark = mobile_2.special_mark
                self.area_region = mobile_2.area_region
                self.zone = mobile_2.zone
                self.building_floor = mobile_2.building_floor
                self.street = mobile_2.street
                self.customer_code = mobile_2.customer_code
            elif self.mobile == mobile_3.mobile_3:
                self.partner_id = mobile_3.id
                self.mobile = mobile_3.mobile_3
                self.special_mark = mobile_3.special_mark
                self.area_region = mobile_3.area_region
                self.zone = mobile_3.zone
                self.building_floor = mobile_3.building_floor
                self.street = mobile_3.street
                self.customer_code = mobile_3.customer_code

            elif self.mobile == mobile_4.mobile_4:
                self.partner_id = mobile_4.id
                self.mobile = mobile_4.mobile_4
                self.special_mark = mobile_4.special_mark
                self.area_region = mobile_4.area_region
                self.zone = mobile_4.zone
                self.building_floor = mobile_4.building_floor
                self.street = mobile_4.street
                self.customer_code = mobile_4.customer_code
            elif self.mobile == mobile_5.mobile_5:
                self.partner_id = mobile_5.id
                self.mobile = mobile_5.mobile_5
                self.special_mark = mobile_5.special_mark
                self.area_region = mobile_5.area_region
                self.zone = mobile_5.zone
                self.building_floor = mobile_5.building_floor
                self.street = mobile_5.street
                self.customer_code = mobile_5.customer_code

    def _prepare_invoice(self):
        """ inherit _prepare_invoice() """
        res = super(SaleOrder, self)._prepare_invoice()
        res.update(street=self.partner_id.street,
                   zone=self.partner_id.zone,
                   building_floor=self.partner_id.building_floor,
                   special_mark=self.partner_id.special_mark,
                   area_region=self.partner_id.area_region,
                   mobile=self.partner_id.mobile,

                   )
        return res


class SaleOrderLine(models.Model):
    """ inherit Sale Order Line """
    _inherit = 'sale.order.line'

    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        res.update({'price_unit': self.price_unit})
        return res
