from odoo import models, fields


class SaleOrder(models.Model):
    _inherit='sale.order'


    def action_confirm(self):
        res=super(SaleOrder,self).action_confirm()
        print('inside sale of order')
        return res
    

    property_id=fields.Many2one('property') 