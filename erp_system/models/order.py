from odoo import fields,models

class Order(models.Model):
    _name='order'
    _description='Order Model'
    name = fields.Char(string="Order Name")
    
    def name_get(self):
        result = []
        for record in self:
            name = "order {}".format(record.id)
            result.append((record.id, name))
        return result

    order_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft', required=True)
    order_date = fields.Datetime(string="Order Date", default=fields.Datetime.now(), required=True)
    required_date = fields.Datetime(string="Required Date",  required=True)
    shipped_date = fields.Datetime(string="Shipped Date",  required=True)
    store_id=fields.Many2one('store',string='Store')
    customer_id=fields.Many2one('customer',string='Customer')
    staff_id=fields.Many2one('staff',string='Staff')