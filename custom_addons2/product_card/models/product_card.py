""" Initialize Call Center Order """
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
import pytz
from datetime import datetime, date, timedelta

class ProductCard(models.Model):
    _name = 'product.card'
    _description = 'Product Card'
    _inherit = ['call.center.line']
