""" Initialize Call Center Report """

from itertools import groupby

from odoo import _, api, models
from odoo.exceptions import ValidationError

 

class CallCenterReportTemplate(models.AbstractModel):
    _name = 'report.professional_call_center.order_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        warehouse_ids = data.get('warehouse_ids')
        product_ids = data.get('product_ids')
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        group_by_branch = data.get('group_by_branch')
        date1 = data.get('date_from_front')
        date2 =  data.get('date_to_front')
        domain = []
        if product_ids:
            domain.append(('product_id', 'in', product_ids))
        if warehouse_ids:
            domain.append(('order_id.warehouse_id', 'in', warehouse_ids))
        if date_from:
            domain.append(('order_id.delivery_date', '>=', date_from))
        if date_to:
            domain.append(('order_id.delivery_date', '<', date_to))

        status = ['in_preparation']
        order_availability = ['manufacturing']
        domain.append(('order_id.state', 'in', status))
        domain.append(('order_id.order_available', 'in', order_availability))

        order_ids = self.env['call.center.line'].search(domain).sorted('warehouse_id')
       
        if not order_ids:
            raise ValidationError(_("There is no data to print"))

        warehouses = set(order_ids.mapped('warehouse_id'))

        return {
            'warehouses': warehouses,
            'order_ids': {k.id: list(v) for k, v in
                          groupby(order_ids, lambda r: r.warehouse_id)},
            'date_from': date1,
            'date_to': date2,
            'group_by_branch': group_by_branch,
        }
