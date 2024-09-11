from odoo import models, fields,api


class Tag(models.Model):
    _name = "tag"

    name = fields.Char(string="Tag", required=True)
    tag_code=fields.Integer(string='Tag Code')
    @api.model
    def create(self, vals):
        # Create the record first to generate the ID
        record = super(Tag, self).create(vals)
        
        # Assign tag_code to the record's ID
        record.tag_code = record.id
        
        return record