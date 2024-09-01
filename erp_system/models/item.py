from odoo import fields,models, api, exceptions

class Item(models.Model):
    _name='item'
    _description='Item Model'
    
    name = fields.Char(string="Item Name")
    
    def name_get(self):
        result = []
        for record in self:
            name = "item {}".format(record.id)
            result.append((record.id, name))
        return result

    product_ids=fields.Many2one('product',string='Products')
    quantity=fields.Integer(string='Quantity')
    price=fields.Float(string='Price')
    discount=fields.Float(string='discount')
    order_id=fields.Many2one('order',string='Order')
    @api.constrains('quantity')
    def _check_quantity(self):
        """Ensure quantity is not set to 0."""
        for record in self:
            if record.quantity == 0:
                raise exceptions.ValidationError("Quantity cannot be 0. Please enter a valid quantity.")
    