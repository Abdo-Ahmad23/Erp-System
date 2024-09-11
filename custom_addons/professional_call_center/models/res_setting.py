""" Initialize Res Setting """

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """
        Inherit Res Config Settings:
         - 
    """
    _inherit = 'res.config.settings'

    delivery_product_id = fields.Many2one(
        'product.product', related='company_id.delivery_product_id',
        domain="[('detailed_type', '=', 'service')]", readonly=False
    )


class ResCompany(models.Model):
    """
        Inherit Res Company:
         - 
    """
    _inherit = 'res.company'

    delivery_product_id = fields.Many2one(
        'product.product'
    )
