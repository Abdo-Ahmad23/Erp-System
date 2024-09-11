# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.

from odoo.exceptions import UserError

from odoo import _, api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, values):
        rtn = super(SaleOrder, self).write(values)
        # If we only get pricelist_id in values then
        # we have to update unit_price who have value lessthen fixed_price value of price list.
        if "pricelist_id" in values:
            self.order_line.filtered(lambda line: line.update_price_unit())
        return rtn


class SaleOrderline(models.Model):
    _inherit = "sale.order.line"

    def update_price_unit(self):
        """
        This method will update unit_price who have value less then fixed_price value of price list.
        return: Only return message containing last updated line.
        """
        message = ""
        if self.order_id.pricelist_id:
            price_unit = self.price_unit
            # Check if price has been changed manually
            if (
                    self.order_id.pricelist_id
                    and self.product_id
                    and not self.user_has_groups(
                "restrict_saleprice_change.groups_restrict_price_change"
            )
            ):
                product_context = dict(
                    self.env.context,
                    partner_id=self.order_id.partner_id.id,
                    date=self.order_id.date_order,
                    uom=self.product_uom.id,
                )
                # Here variable price calculates the price of product after
                # applying pricelist on it and rule_id is the id of the rule
                # of pricelist which is applied on product
                price, rule_id = self.order_id.pricelist_id.with_context(
                    product_context
                ).get_product_price_rule(
                    self.product_id,
                    self.product_uom_qty or 1.0,
                    self.order_id.partner_id,
                )
                if (price_unit < price) and rule_id:
                    self.price_unit = price
                    message = _(
                        "You don't have Access to change the Price Less than"
                        + str(price)
                    )
        return message

    @api.constrains("price_unit")
    def price_unit_change_constrains(self):
        """
        This constrain will update unit_price who have value less then fixed_price value of price list.
        """
        self.mapped(lambda line: line.update_price_unit())

    @api.onchange("price_unit")
    def price_unit_change(self):
        """
        if 'update_price_unit' has try to update unit_price it will raise UserError.
        """
        message = self.update_price_unit()
        if message:
            raise UserError(message)
