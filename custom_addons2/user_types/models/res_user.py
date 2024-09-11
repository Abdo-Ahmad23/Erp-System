""" Initialize Res User """

from odoo import api, fields, models


class ResUsers(models.Model):
    """
        Inherit Res Users:
         - 
    """
    _inherit = 'res.users'

    user_types = fields.Selection(
        [('internal', 'Internal'),
         ('portal', 'Portal')],
        compute='_compute_user_types', store=True
    )

    @api.depends('share')
    def _compute_user_types(self):
        """ Compute user_types value """
        for rec in self:
            if rec.share:
                rec.user_types = 'portal'
            else:
                rec.user_types = 'internal'
