""" Initialize Purchase Order """

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    """
        Inherit Purchase Order Line:
         -
    """
    _inherit = 'purchase.order.line'

    sales_price = fields.Monetary(
        currency_field='currency_id'
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        self.sales_price = self.product_id.list_price
