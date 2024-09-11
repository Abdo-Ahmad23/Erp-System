""" Initialize Sale Order """

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'sale.order'

    # special_marque = fields.Char()
    customer_code = fields.Char()
    # mobile = fields.Char()

    # @api.onchange('partner_id', 'mobile')
    # def _onchange_partner_id(self):
    #     """ partner_id """
    #     for rec in self:
    #         if rec.partner_id:
    #             rec.mobile = rec.partner_id.mobile
    #             rec.special_marque = rec.partner_id.special_marque
    #             rec.customer_code = rec.partner_id.customer_code
    #             if rec.partner_id.stock_warehouse_id:
    #                 rec.warehouse_id = rec.partner_id.stock_warehouse_id.id
    #         if rec.mobile:
    #             partner = self.env['res.partner'].search(
    #                 [('mobile', '=', self.mobile)], limit=1)
    #             rec.partner_id = partner.id
    #             rec.special_marque = partner.special_marque
    #             rec.customer_code = partner.customer_code
    #             if rec.partner_id.stock_warehouse_id:
    #                 rec.warehouse_id = partner.stock_warehouse_id.id


class SaleOrderLine(models.Model):
    """
        Inherit Sale Order Line:
         -
    """
    _inherit = 'sale.order.line'

    purchase_price = fields.Monetary(
        currency_field='currency_id'
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        self.purchase_price = self.product_id.standard_price
