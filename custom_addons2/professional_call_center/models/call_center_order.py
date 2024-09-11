""" Initialize Call Center Order """
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
import pytz
from datetime import datetime, date, timedelta


class CallCenterOrder(models.Model):
    """
          Initialize Call Center Order:
    """
    _name = 'call.center.order'
    _description = 'Call Center Order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    @api.model
    def _default_warehouse_id(self):
        # !!! Any change to the default value may have to be repercuted
        # on _init_column() below.
        return self.env.user._get_default_warehouse_id()

    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()

    name = fields.Char(
        readonly=True, default='New', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), "
               "('company_id', '=', company_id)]",
    )
    mobile = fields.Char(
        readonly=True, states={'draft': [('readonly', False)]}
    )
    mobile_2 = fields.Char(compute='_set_mobile', save=True)
    mobile_3 = fields.Char()
    mobile_4 = fields.Char()
    mobile_5 = fields.Char()
    customer_code = fields.Char()
    street = fields.Char(
        readonly=True
    )
    street2 = fields.Char(
        readonly=True
    )
    state_id = fields.Many2one(
        'res.country.state', readonly=True
    )
    country_id = fields.Many2one(
        'res.country', readonly=True
    )
    zone_id = fields.Many2one(
        'res.country.zone', readonly=True
    )
    district_id = fields.Many2one(
        'res.country.district', readonly=True
    )
    land_mark = fields.Char(
        readonly=True
    )
    building_type_id = fields.Many2one(
        'building.type', readonly=True
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
        'hr.employee', default=lambda self: self.env.user.employee_id, readonly=True)
    order_type = fields.Selection(
        [('in_the_branch', 'In The Branch'),
         ('delivery', 'Delivery')],
        readonly=True, tracking=1,required=True,
        states={'draft': [('readonly', False)]}
    )
    cancel_reason = fields.Selection(
       [('done', 'Done'),
        ('رغبة عميل', 'رغبة عميل'),
        ('العميل اشتري مباشر', 'العميل اشتري مباشر'),
        ('مكرر', 'مكرر'),
        ('لم يكتب السبب', 'لم يكتب السبب'),
        ('العميل لم يستلم', 'العميل لم يستلم'),
        ('عمد جدية العميل', 'عمد جدية العميل'),
        ('عدم وجود المنتج', 'عدم وجود المنتج'),
        ('تأخير الاوردر', 'تأخير الاوردر'),
        ('خطأ تحضير', 'خطأ تحضير'),
        ('شكوي عميل', 'شكوي عميل')],
        default='done',
    )

    delivery_type_id = fields.Many2one(
        'delivery.type', readonly=True, states={'draft': [('readonly', False)]},
        required=True
    )
    date_order = fields.Datetime(
        string='Order Date', required=True, readonly=True, index=True,
        copy=False, default=fields.Datetime.now
    )
    delivery_date = fields.Datetime(
        string='Delivery Date & Time', readonly=True, required=True,
        states={'draft': [('readonly', False)]}
    )

    # delivery_date_n = fields.Datetime(required=True, readonly=True, index=True,
    #     copy=False,compute='_get_date',store=True)
    @api.depends('delivery_date')
    def _convert_date(self):
        for rec in self:
            print("Time in UTC", rec.delivery_date)
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            print("user_tz", user_tz)
            date_tody = pytz.utc.localize(rec.delivery_date).astimezone(user_tz)
            print("Time Local .. : ", date_tody)
            date_format = "%d/%m/%Y %I:%M:%S %p"
            date_string = date_tody.strftime(date_format)
            print("Time Local .. : ", date_string)
            print(str(date_string))
            return str(date_string)

    @api.depends('delivery_date')
    def _get_now_date(self):
        for rec in self:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            date_now = datetime.now()
            date_tody = pytz.utc.localize(date_now).astimezone(user_tz)
            # print(type(date_tody))
            # print(date_tody)
            date_format = "%d/%m/%Y %I:%M:%S %p"
            date_string = date_tody.strftime(date_format)
            # print(date_string)
            return str(date_string)

    create_date = fields.Datetime(
        string='Creation Date', readonly=True, index=True,
        help="Date on which sales order is created."
    )

    call_center_line_ids = fields.One2many(
        'call.center.line',
        'order_id', states={'draft': [('readonly', False)]}, readonly=True,
        auto_join=True, tracking=1
    )
    call_center_lines = fields.Integer(string="Lines Number", compute="_get_number_lines", tracking=1)

    state = fields.Selection(
        [('draft', 'Draft'),
         ('in_preparation', 'In Preparation'),
         ('delivery_invoices', 'Delivery Invoices'),
         ('delivery_assigned', 'Delivery Assigned'),
         ('delivery_on_way', 'Delivery On Way'),
         ('delivery_arrived', 'Delivery Arrived'),
         ('delivery_collection', 'Delivery Collection'),
         ('delivery_canceled', 'Delivery Canceled'),
         ('done', 'Done')],
        default='draft', tracking=1,
        string='Status'
    )
    order_available = fields.Selection(
        [('in_hand', 'In_Hand'),
         ('manufacturing', 'Manufacturing')],
        string="Order Availability", readonly=True, tracking=1, default='in_hand', compute="_compute_available"
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse', required=True, tracking=1,
        readonly=True, related='picking_type_id.warehouse_id'
    )
    picking_type_id = fields.Many2one(
        'stock.picking.type', required=True, readonly=True, tracking=1,
        states={'draft': [('readonly', False)]}
    )
    location_id = fields.Many2one(
        'stock.location', required=True, readonly=True,
        domain="[('usage', '=', 'internal'),('warehouse_id', '=', warehouse_id)]",
        states={'draft': [('readonly', False)]}, tracking=1,
    )
    company_id = fields.Many2one(
        'res.company', 'Company', required=True, index=True,
        default=lambda self: self.env.company, readonly=True, tracking=1,
        states={'draft': [('readonly', False)]}
    )

    team_id = fields.Many2one(
        'crm.team', 'Sales Team', readonly=True,
        states={'draft': [('readonly', False)]},
        ondelete="set null", tracking=True,
        change_default=True, default=_get_default_team, check_company=True,
        # Unrequired company
        domain="['|', ('company_id', '=', False), "
               "('company_id', '=', company_id)]")
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2,
        default=lambda self: self.env.user, readonly=True,
        states={'draft': [('readonly', False)]}
    )
    journal_id = fields.Many2one(
        'account.journal',
        string="Journal",
        required=True,
        index=True,
        readonly=True,
        tracking=1,
        compute='_get_journal_id_by_name'
    )
    amount_total = fields.Float(
        compute='_compute_amount_total', store=True
    )
    note = fields.Text()
    picking_id = fields.Many2one('stock.picking')
    attachment = fields.Binary(
        readonly=True, states={'draft': [('readonly', False)]}
    )
    account_move_id = fields.Many2one(
        'account.move'
    )
    subtotal = fields.Float(
        compute='_compute_subtotal_and_tax', store=True
    )
    tax_amount = fields.Float(
        compute='_compute_subtotal_and_tax', store=True
    )
    delivery_address_info_ids = fields.Many2many(
        'delivery.address.info'
    )
    delivery_address_info_id = fields.Many2one(
        'delivery.address.info', readonly=True,
        states={'draft': [('readonly', False)]},
        domain="[('id', 'in', delivery_address_info_ids)]"
    )
    prepaid = fields.Boolean(
        readonly=True, copy=False
    )
    paid_amount = fields.Float(
        readonly=True, copy=False
    )
    amount_due = fields.Float(
        compute='_compute_amount_due', save=True
    )

    @api.depends('call_center_line_ids')
    def _get_number_lines(self):
        for rec in self:
            # count = 0
            # for rec2 in rec.call_center_line_ids:
            #     count = count + 1
            # print(count)
            # rec.call_center_lines = count
            rec.call_center_lines = len(rec.call_center_line_ids)
    @api.depends('journal_id')
    def _get_journal_id_by_name(self):
        journals_tables = self.env['account.journal'].search([])
        for rec in journals_tables:
            if rec.type == 'sale':
                self.journal_id = rec.id
                print(rec.id)

    @api.depends('amount_total', 'paid_amount')
    def _compute_amount_due(self):
        """ Compute amount_due value """
        for rec in self:
            rec.amount_due = rec.amount_total - rec.paid_amount

    @api.depends('call_center_line_ids', 'call_center_line_ids.unit_price',
                 'call_center_line_ids.quantity',
                 'call_center_line_ids.tax_ids')
    def _compute_subtotal_and_tax(self):
        """ Compute _compute_subtotal and tax value """
        for rec in self:
            if rec.call_center_line_ids:
                rec.subtotal = sum(
                    rec.call_center_line_ids.mapped('price_subtotal'))
                rec.tax_amount = sum([rec.quantity * rec.unit_price * sum(
                    rec.tax_ids.mapped('amount')) / 100 if rec.tax_ids else 0
                                      for rec in rec.call_center_line_ids])

    @api.depends('tax_amount', 'subtotal')
    def _compute_amount_total(self):
        """ Compute amount total value """
        for rec in self:
            if rec.call_center_line_ids:
                rec.amount_total = sum(
                    rec.call_center_line_ids.mapped(
                        'price_subtotal')) + rec.tax_amount

    @api.onchange('picking_type_id')
    def _onchange_picking_type_id(self):
        """ picking_type_id """
        self.location_id = self.picking_type_id.default_location_src_id.id

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """ Partner Id """
        if self.partner_id:
            self.update_partner_address(self.partner_id)
            self.delivery_address_info_ids = [
                (6, 0, self.partner_id.delivery_address_info_ids.ids)]
        else:
            self.remove_fields_data()

    @api.onchange('mobile_2')
    def _set_mobile(self):
        partner_id1 = self.env['res.partner'].search([])
        for i in partner_id1:
            if i.id == self.partner_id.id:
                self.mobile_2 = i.mobile_2
                self.mobile_3 = i.mobile_3
                self.mobile_4 = i.mobile_4
                self.mobile_5 = i.mobile_5

    @api.onchange('mobile')
    def _onchange_mobile(self):
        """ Mobile """
        if self.mobile:
            mobile_format = f'+2{self.mobile[:1]} {self.mobile[1:4]}' \
                            f' {self.mobile[4:7]} {self.mobile[7:]}'
            partner_id = self.env['res.partner'].search([
                '|', '|', '|', '|',
                ('mobile', 'in', [mobile_format, self.mobile]),
                ('mobile_2', '=', self.mobile),
                ('mobile_3', '=', self.mobile),
                ('mobile_4', '=', self.mobile),
                ('mobile_5', '=', self.mobile),
            ], limit=1)
            if partner_id:
                self.update_partner_address(partner_id)

    @api.onchange('customer_code')
    def _onchange_customer_code(self):
        """ customer_code """
        if self.customer_code:
            partner_id = self.env['res.partner'].search(
                [('customer_code', '=', self.customer_code)], limit=1)
            if partner_id:
                self.update_partner_address(partner_id)

    @api.onchange('delivery_date')
    def _onchange_delivery_date(self):
        """ delivery_date """
        if self.delivery_date and self.date_order and self.date_order > self.delivery_date:
            raise ValidationError(
                _("The Delivery Date Must Be Longer Than Order Date"))

    @api.onchange('delivery_address_info_id')
    def _onchange_delivery_address_info_id(self):
        """ delivery_address_info_id """
        if self.delivery_address_info_id:
            self.zone_id = self.delivery_address_info_id.zone_id.id
            self.state_id = self.delivery_address_info_id.state_id.id
            self.district_id = self.delivery_address_info_id.district_id.id
            self.state_id = self.delivery_address_info_id.state_id.id
            self.country_id = self.delivery_address_info_id.country_id.id
            self.street = self.delivery_address_info_id.street
            self.street2 = self.delivery_address_info_id.street2
            self.land_mark = self.delivery_address_info_id.land_mark
            self.building_type_id = self.delivery_address_info_id \
                .building_type_id.id
            self.building_number = self.delivery_address_info_id.building_number
            self.floor_number = self.delivery_address_info_id.floor_number
            self.flat_number = self.delivery_address_info_id.flat_number

    def add_service_product(self):
        """Add Product Service in order Line"""
        delivery_product_id = self.env.company.delivery_product_id
        if self.delivery_type_id:
            if delivery_product_id:
                self.call_center_line_ids = [(0, 0, {
                    'product_id': delivery_product_id.id,
                    'name': '',
                    'product_category':delivery_product_id.categ_id.id,
                    'order_available': 'in_hand',
                    'product_type':delivery_product_id.detailed_type,
                    'unit_price': self.delivery_type_id.delivery_type_line_ids.filtered(
                        lambda
                            r: r.district_id == self.district_id and r.zone_id == self.zone_id).price
                })]
            else:
                raise ValidationError(
                    _("Please enter delivery product in setting"))
            
    
    def action_confirm(self):
        """ Action Confirm """
        for order in self:
            date_now = order._get_now_date()
            if order._convert_date() < date_now:
                raise ValidationError(
                    _("The Delivery Date Must Be Longer Than Now Date : "))
            else:
                location_dest_id = self.env.ref('stock.stock_location_suppliers').id if self.picking_type_id.code == 'incoming' \
                    else self.env.ref('stock.stock_location_customers').id
                stock_move = []
                for line in order.call_center_line_ids:
                    if line.product_id.detailed_type == 'product':
                        stock_move.append((0, 0, {
                            'product_id': line.product_id.id,
                            'product_uom': line.product_id.uom_id.id,
                            'location_id': order.location_id.id,
                            'location_dest_id': location_dest_id,
                            'name': line.name,
                            'product_uom_qty': line.quantity,
                            'price_unit': line.unit_price,
                        }))
                #-----------------------------------
                if order.order_available == 'manufacturing':
                    for line in order.call_center_line_ids:
                        if line.product_id.detailed_type == 'product' and line.order_available == 'manufacturing':
                            pc_id = self.env['product.card'].create(
                                {
                                'product_id': line.product_id.id,
                                'order_id': line.order_id.id,
                                'partner_id': line.partner_id.id,
                                'product_category': line.product_category.id,
                                'quantity': line.quantity,
                                'unit_price': line.unit_price,
                                'product_type': line.product_type,
                                'state': line.state,
                                'warehouse_id': line.warehouse_id.id,
                                'delivery_date': line.delivery_date,
                                'date_order': line.date_order,
                                'name_des': line.name_des,
                                'order_available': line.order_available
                                }
                            )

                #-----------------------------------     

                picking_id = self.env['stock.picking'].create(
                    {
                        'partner_id': order.partner_id.id,
                        'picking_type_id': order.picking_type_id.id,
                        'location_id': order.location_id.id,
                        'location_dest_id': location_dest_id,
                        'order_type': order.order_type,
                        'delivery_type_id': order.delivery_type_id.id,
                        'attachment': order.attachment,
                        'delivery_date': order.delivery_date,
                        'zone_id': order.zone_id.id,
                        'district_id': order.district_id.id,
                        'state_id': order.state_id.id,
                        'country_id': order.country_id.id,
                        'land_mark': order.land_mark,
                        'street': order.street,
                        'street2': order.street2,
                        'building_type_id': order.building_type_id.id,
                        'call_center_agent_id': order.call_center_agent_id.id,
                        'building_number': order.building_number,
                        'floor_number': order.floor_number,
                        'flat_number': order.flat_number,
                        'note': order.note,
                        'call_center_order_id': order.id,
                        'company_id': order.company_id.id,
                        'origin': order.name,
                        'move_ids_without_package': stock_move,
                    }
                )
                self.picking_id = picking_id
                self.state = 'in_preparation'

    def action_view_delivery(self):
        """ :return Stock Picking action """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'name': _('Stock Picking'),
            'view_mode': 'tree,form',
            'res_id': self.picking_id.id,
            'views': [(False, 'form')],
        }

    def action_view_account_move(self):
        """ :return Account Move action """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'name': _('Account Move'),
            'view_mode': 'tree,form',
            'context': {'delivery_invoice': 1},
            'res_id': self.account_move_id.id,
            'views': [(False, 'form')],
        }

    def action_view_register_payment_wizard(self):
        """ :return Register Payment Wizard action """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'register.payment.wizard',
            'name': _('Collection Amount Wizard'),
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_call_center_order_id': self.id},
            'views': [(False, 'form')],
        }

    def update_partner_address(self, partner_id):
        """ Update Partner Address """
        self.write({
            'partner_id': partner_id.id,
            'mobile': partner_id.mobile,
            'customer_code': partner_id.customer_code,
            'street': partner_id.street,
            'street2': partner_id.street2,
            'state_id': partner_id.state_id.id,
            'country_id': partner_id.country_id.id,
            'zone_id': partner_id.zone_id,
            'district_id': partner_id.district_id,
            'land_mark': partner_id.land_mark,
            'building_type_id': partner_id.building_type_id,
            'building_number': partner_id.building_number,
            'floor_number': partner_id.floor_number,
            'flat_number': partner_id.flat_number,
        })

    def create_account_move(self):
        """ Create Account Move """
        for rec in self:
            journal = self.sudo().env['account.move'].with_context(default_move_type='out_invoice')._compute_journal_id
            if not journal:
                raise UserError(_(
                    'Please define an accounting sales journal for the company %s (%s).',
                    self.company_id.name, self.company_id.id))
            invoice_line = []
            for line in rec.call_center_line_ids:
                invoice_line.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name_des,
                    'tax_ids': [(6, 0, line.tax_ids.ids)],
                    'price_unit': line.unit_price,
                    'quantity': line.quantity,
                    'display_type': line.display_type or 'product',
                }))
            account_move_id = self.sudo().env['account.move'].create(
                {
                    'partner_id': rec.partner_id.id,
                    'call_center_order_id': rec.id,
                    'invoice_line_ids': invoice_line,
                    'move_type': 'out_invoice',
                    'narration': rec.note,
                    'user_id': rec.user_id.id,
                    'invoice_user_id': rec.user_id.id,
                    'order_type': rec.order_type,
                    'delivery_date': rec.delivery_date,
                    'street': rec.street,
                    'street2': rec.street2,
                    'zone_id': rec.zone_id.id,
                    'district_id': rec.district_id.id,
                    'state_id': rec.state_id.id,
                    'country_id': rec.country_id.id,
                    'land_mark': rec.land_mark,
                    'building_type_id': rec.building_type_id.id,
                    'building_number': rec.building_number,
                    'floor_number': rec.floor_number,
                    'flat_number': rec.flat_number,
                    'delivery_type_id': rec.delivery_type_id.id,
                    'picking_id': rec.picking_id.id,
                    'attachment': rec.attachment,
                    'partner_bank_id': rec.company_id.partner_id.bank_ids[:1].id,
                    'journal_id': rec.journal_id.id,
                    'invoice_origin': rec.name,
                    'company_id': rec.company_id.id,
                    'delivery_state': 'delivery_invoices',
                    'prepaid': rec.prepaid,
                }
            )
            account_move_id.action_post()
            self.account_move_id = account_move_id.id
            self.state = 'delivery_invoices'
            return self.account_move_id.id

    def remove_fields_data(self):
        """ Remove Fields Data """
        self.write({
            'partner_id': False,
            'mobile': None,
            'customer_code': None,
            'street': None,
            'street2': None,
            'zone_id': False,
            'state_id': False,
            'country_id': False,
            'district_id': False,
            'land_mark': None,
            'building_type_id': False,
            'building_number': None,
            'floor_number': None,
            'flat_number': None,
        })

    def get_address(self):
        address = ''
        if self.state_id:
            address += self.state_id.name + " "
        if self.zone_id:
            address += self.zone_id.name + " "
        if self.district_id:
            address += self.district_id.name + " "
        if self.street:
            address += self.street + " "
        if self.street2:
            address += self.street2 + " "
        if self.land_mark:
            address += self.land_mark + " "
        if self.building_type_id:
            address += self.building_type_id.name
        if self.building_number:
            address += self.building_number + " "
        if self.flat_number:
            address += self.flat_number
        return address

    @api.model
    def create(self, vals_list):
        """
            Override create method
             - sequence name
        """
        if vals_list.get('name', _('New')) == _('New'):
            sequence = self.env['ir.sequence'].next_by_code('call.center.order')
            vals_list.update(name=sequence or '/')
        return super(CallCenterOrder, self).create(vals_list)

    def _convert_date_front(self, date):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        date_tody = pytz.utc.localize(date).astimezone(user_tz)
        date_format = "%d/%m/%Y %I:%M:%S %p"
        date_string = date_tody.strftime(date_format)
        return str(date_string)

    @api.depends('call_center_line_ids', 'call_center_line_ids.order_available')
    def _compute_available(self):
        for rec in self:
            rec.order_available = 'in_hand'
            if rec.call_center_line_ids:
                for line in rec.call_center_line_ids:
                    if line.order_available == "manufacturing":
                        rec.order_available = "manufacturing"
                        break


class CallCenterLine(models.Model):
    """
        Initialize Call Center Line:
         -
    """
    _name = 'call.center.line'
    _description = 'Call Center Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name_des = fields.Char(
        string='Description', tracking=1)
    product_id = fields.Many2one(
        'product.product', tracking=1
    )
    product_category = fields.Many2one(
        'product.category',
        string="Product Category",
        related = 'product_id.categ_id',
        store=True
    )
    product_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Storable Product')],
        string="Product Type",
        related='product_id.detailed_type', store=True
    )
    qty_available = fields.Float(
        string="Quantity On Hand", readonly=True
    )
    virtual_available = fields.Float(
        string="Forecasted Quantity", readonly=True,
    )
    qty_in_location = fields.Float(
        string="Quantity In Location", compute='_compute_qty_in_location',
        store=True
    )
    quantity = fields.Float(
        default='1', tracking=1
    )
    unit_price = fields.Float(
        readonly=True
    )
    price_subtotal = fields.Float(
        compute='_compute_price_subtotal', store=True
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Branch', related='order_id.warehouse_id',
        store=True
    )
    order_id = fields.Many2one(
        'call.center.order'
    )
    name = fields.Many2one(
      store=True, related='order_id'
    )
    tax_ids = fields.Many2many('account.tax')
    product_description = fields.Char(compute='_compute_product_description', store=True)
    delivery_date = fields.Datetime(
        string='Delivery Date & Time', readonly=True, related='order_id.delivery_date'
    )
    date_order = fields.Datetime(
        string='Order Date', required=True, readonly=True, index=True,
        copy=False, default=fields.Datetime.now, related='order_id.date_order', store=True
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('in_preparation', 'In Preparation'),
         ('delivery_invoices', 'Delivery Invoices'),
         ('delivery_assigned', 'Delivery Assigned'),
         ('delivery_on_way', 'Delivery On Way'),
         ('delivery_arrived', 'Delivery Arrived'),
         ('delivery_collection', 'Delivery Collection'),
         ('delivery_canceled', 'Delivery Canceled'),
         ('done', 'Done')],
        default='draft', tracking=1,
        string='Status', related='order_id.state', store=True
    )
    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True, store=True, related='order_id.partner_id'
    )

    # Fields specifying custom line logic
    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line_note', "Note"),
            ('product', 'Product'),
        ],
        default=False)
        
    order_available = fields.Selection(
       [('in_hand', 'In_Hand'),
        ('manufacturing', 'Manufacturing')],
       string='Order Availability', tracking=1, required=1
    )

    @api.depends('product_id')
    def _compute_qty_in_location(self):
        """ Compute qty_in_location value """
        for rec in self:
            rec.qty_in_location = self.env['stock.quant'].search(
                [('product_id', '=', rec.product_id.id),
                 ('location_id', '=',
                  rec.order_id.location_id.id)]).available_quantity

    @api.depends('product_id', 'unit_price', 'quantity')
    def _compute_price_subtotal(self):
        """ Compute _compute_price_subtotal value """
        for rec in self:
            rec.price_subtotal = rec.quantity * rec.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        if self.product_id:
            self.name_des = ''
            self.unit_price = self.product_id.list_price
            self.qty_available = self.product_id.qty_available
            self.virtual_available = self.product_id.virtual_available

    @api.depends('product_id', 'name_des')
    def _compute_product_description(self):
        """ compute_product_description  """
        for record in self:
            record.product_description = record.product_id.name.strip(' [1234567890]')  # this method to delete # this method to delete internal referance

    @api.model
    def create(self, values):
        if values.get('display_type', self.default_get(['display_type'])['display_type']):
            values.update(product_id=False, tax_ids=False, unit_price=0, quantity=0,)
        line = super(CallCenterLine, self).create(values)
        return line

    def write(self, values):
        if 'display_type' in values and self.filtered(
                lambda line: line.display_type != values.get('display_type')):
            raise UserError(
                "You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type.")
        result = super(CallCenterLine, self).write(values)
        return result


