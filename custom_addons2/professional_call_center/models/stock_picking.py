""" Initialize Stock Picking """

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError



class StockPicking(models.Model):
    """
        Inherit Stock Picking:
         -
    """
    _inherit = 'stock.picking'

    call_center_order_id = fields.Many2one(
        'call.center.order'
    )
    order_type = fields.Selection(
        [('in_the_branch', 'In The Branch'),
         ('delivery', 'Delivery')],
        default='in_the_branch', readonly=True,
        states={'draft': [('readonly', False)]}
    )
    delivery_date = fields.Datetime(
        string='Delivery Date & Time', copy=False, readonly=True,
        states={'draft': [('readonly', False)]}
    )
    attachment = fields.Binary(
        readonly=True, states={'draft': [('readonly', False)]}
    )
    account_move_id = fields.Many2one(
        'account.move'
    )
    delivery_type_id = fields.Many2one(
        'delivery.type', readonly=True, states={'draft': [('readonly', False)]},
    )
    street = fields.Char(
        readonly=True
    )
    street2 = fields.Char(
        readonly=True
    )
    zone_id = fields.Many2one(
        'res.country.zone', readonly=True
    )
    district_id = fields.Many2one(
        'res.country.district', readonly=True
    )
    land_mark = fields.Char(
        readonly=True,
    )
    building_type_id = fields.Many2one(
        'building.type', readonly=True,
    )
    building_number = fields.Char(
        readonly=True
    )
    floor_number = fields.Char(
        readonly=True
    )
    flat_number = fields.Char(
        readonly=True
    )
    call_center_agent_id = fields.Many2one(
        'hr.employee',
        readonly=True
    )
    state_id = fields.Many2one(
        'res.country.state', readonly=True
    )
    country_id = fields.Many2one(
        'res.country', readonly=True
    )

    def button_validate(self):
        """ Override button_validate """
        res = super(StockPicking, self).button_validate()
        if self.call_center_order_id and self.state == 'done':
            self.account_move_id = self.call_center_order_id. \
                create_account_move()
        return res

    def action_view_account_move(self):
        """ :return Account Move action """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'name': _('Invoice'),
            'view_mode': 'tree,form',
            'context': {'delivery_invoice': 1},
            'res_id': self.account_move_id.id,
            'views': [(False, 'form')],
        }


class StockLocation(models.Model):
    """
        Inherit Stock Location:
         -
    """
    _inherit = 'stock.location'

    warehouse_id = fields.Many2one(
        'stock.warehouse', store=True
    )


class StockMove(models.Model):
    """
        Inherit Stock Move:
         -
    """
    _inherit = 'stock.move'

    price_unit = fields.Float()

