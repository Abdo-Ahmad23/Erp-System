""" Initialize Account Asset """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models


class AccountAssetAsset(models.Model):
    """
        Inherit Account Asset Asset:
         - 
    """
    _inherit = 'account.asset'

    asset_code = fields.Char()
