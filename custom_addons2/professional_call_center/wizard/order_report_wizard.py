""" Initialize Order Report Wizard """

from odoo import api, fields, models

import pytz
from datetime import datetime, date, timedelta

class OrderReportWizard(models.TransientModel):
    """
        Initialize Order Report Wizard:
         -
    """
    _name = 'order.report.wizard'
    _description = 'Order Report Wizard'

    date_from = fields.Datetime(
        required=True
    )
    date_to = fields.Datetime(
        required=True
    )

    warehouse_ids = fields.Many2many(
        'stock.warehouse', string='Branch'
    )
    product_ids = fields.Many2many(
        'product.product'
    )
    group_by_branch = fields.Boolean()

    @api.onchange('group_by_branch')
    def _onchange_group_by_branch(self):
        """ group_by_branch """
        if not self.group_by_branch:
            self.warehouse_ids = False

    def prepare_data(self):
        return {
            'warehouse_ids': self.warehouse_ids.ids,
            'product_ids': self.product_ids.ids,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'group_by_branch': self.group_by_branch,
            'date_from_front': self._convert_date(self.date_from),
            'date_to_front': self._convert_date(self.date_to),
        }

    def print_report(self):
        data = self.prepare_data()
        return self.env.ref(
            'professional_call_center.call_center_report'
        ).report_action(self, data=data)

    def _convert_date(self,date):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        date_tody = pytz.utc.localize(date).astimezone(user_tz)
        date_format = "%d/%m/%Y %I:%M:%S %p"
        date_string = date_tody.strftime(date_format)
        return str(date_string)    