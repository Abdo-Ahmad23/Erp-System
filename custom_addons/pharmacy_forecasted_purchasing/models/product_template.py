""" Initialize Product Template """

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ProductTemplate(models.Model):
    """
        Inherit Product Template:
         - 
    """
    _inherit = 'product.template'

    unit_value = fields.Integer()
    type_of_product = fields.Many2one(
        'type.of.product'
    )
    origin = fields.Many2one('product.origin')

    using_way_id = fields.Many2one(
        'using.way'
    )
    producing_company_id = fields.Many2one(
        'producing.company'
    )
    discounted = fields.Boolean()
    max_discount = fields.Integer()
    return_security = fields.Boolean()
    effective_material = fields.Char()
    scientific_group_id = fields.Many2one('scientific.group')
    international_code = fields.Char()
    price_without_vat = fields.Monetary()
    price_vat = fields.Monetary(string="Vat")


class TypeOfProduct(models.Model):
    """
        Initialize Type Of Product:
         -
    """
    _name = 'type.of.product'
    _description = 'Type Of Product'

    name = fields.Char(
        required=True
    )


class UsingWay(models.Model):
    """
        Initialize Using Way:
         -
    """
    _name = 'using.way'
    _description = 'Using Way'

    name = fields.Char(
        required=True,
    )


class ProducingCompany(models.Model):
    """
        Initialize Producing Company:
         -
    """
    _name = 'producing.company'
    _description = 'Producing Company'

    name = fields.Char(
        required=True,
    )


class ScientificGroup(models.Model):
    """ Scientific Group """
    _name = 'scientific.group'
    _description = 'Scientific Group'

    name = fields.Char()


class ProductOrigin(models.Model):
    """ Product Origin """
    _name = 'product.origin'
    _description = 'Product Origin'

    name = fields.Char()
