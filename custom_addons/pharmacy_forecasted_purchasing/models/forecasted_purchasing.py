""" Initialize Forcasted Purchasing """

from datetime import datetime

import dateutil
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

from odoo import _, api, fields, models


class ForecastedPurchasing(models.Model):
    """
        Initialize Forecasted Purchasing:
         - 
    """
    _name = 'forecasted.purchasing'
    _description = 'Forecasted Purchasing'
    _check_company_auto = True

    name = fields.Char(readonly=True, default='New')
    product_category_ids = fields.Many2many(
        'product.category'
    )
    warehouse_ids = fields.Many2many(
        'stock.warehouse', copy=False)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    product_ids = fields.Many2many(
        'product.product'
    )
    replenish_period = fields.Integer()
    minimum_replenish_period = fields.Integer()
    forecasted_purchasing_information_ids = fields.One2many(
        'forecasted.purchasing.information',
        'forecasted_purchasing_id'
    )
    Period_days = fields.Integer(compute='_period_days', store=True, )
    purchase_order_ids = fields.One2many('purchase.order',
                                         'forecasted_purchasing_id')
    purchase_order_number = fields.Integer(compute='_compute_count', store=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor')

    @api.model
    def create(self, vals_list):
        """
            Override create method
             - sequence name
        """
        if vals_list.get('name', _('New')) == _('New'):
            sequence = self.env['ir.sequence'].next_by_code(
                'forecasted.purchasing')
            vals_list.update(name=sequence or '/')
        return super(ForecastedPurchasing, self).create(vals_list)

    @api.depends('purchase_order_ids')
    def _compute_count(self):
        """ Compute  value """
        for rec in self:
            rec.purchase_order_number = len(rec.purchase_order_ids.ids)

    def action_view_purchase_order(self):
        """ Smart button to run action """
        recs = self.mapped('purchase_order_ids')
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        if len(recs) > 1:
            action['domain'] = [('id', 'in', recs.ids)]
            action['context'] = {'default_forecasted_purchasing_id': self.id}

        elif len(recs) == 1:
            action['views'] = [
                (self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = recs.ids[0]
            action['context'] = {'default_forecasted_purchasing_id': self.id}
        else:
            action['views'] = [
                (self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['context'] = {'default_forecasted_purchasing_id': self.id}

        return action

    def create_purchase_orders(self):
        vendor = []
        reb = []
        vals = []
        ven = []
        stock = []
        sto = []
        info = []

        # if any(not rec.vendor_id.id or not rec.stock_picking_id.id for rec in
        #        self.forecasted_purchasing_information_ids):
        #     raise ValidationError(_("Vendor or  Deliver To not exist"))

        if self.vendor_id:
            for rec in self.forecasted_purchasing_information_ids:
                info.append({'product_id': rec.product_id.id,
                             'product_qty': rec.expected_quantity})
            self.env['purchase.order'].create({
                'partner_id': self.vendor_id.id,
                'forecasted_purchasing_id': self.id,
                # 'picking_type_id': rec.stock_picking_id.id,
                'order_line': [(0, 0, line) for line in info]

            })

        else:
            for rec in self.forecasted_purchasing_information_ids:

                for v in self.forecasted_purchasing_information_ids:

                    if v.vendor_id.id in reb and v.stock_picking_id.id in stock:
                        pass
                    else:
                        if rec.vendor_id.id == v.vendor_id.id and rec.stock_picking_id.id == v.stock_picking_id.id:
                            vendor.append(v)

                reb.append(rec.vendor_id.id)
                stock.append(rec.stock_picking_id.id)
                if [(rec.vendor_id.id, rec.stock_picking_id.id)] in ven:
                    pass
                else:
                    for e in vendor:
                        vals.append({'product_id': e.product_id.id,
                                     'product_qty': e.expected_quantity})

                    self.env['purchase.order'].create({
                        'partner_id': rec.vendor_id.id,
                        'forecasted_purchasing_id': self.id,
                        'picking_type_id': rec.stock_picking_id.id,
                        'order_line': [(0, 0, line) for line in vals]

                    })
                    ven.append([(rec.vendor_id.id, rec.stock_picking_id.id)])
                    sto.append(rec.stock_picking_id.id)
                vendor = []
                vals = []

    @api.onchange('warehouse_ids', 'product_ids')
    def _onchange_warehouse_ids(self):
        """ Add domain to some filed """
        loc = []
        pro = []

        if self.warehouse_ids:
            for lot in self.warehouse_ids:
                loc.append(lot.lot_stock_id.id)
            product = self.env['stock.quant'].search(
                [('location_id', 'in', loc)])
            for rec in product:
                pro.append(rec.product_id.id)

            return {'domain': {
                'product_ids': [('id', 'in', pro)]
            }}
        # elif not self.warehouse_ids:
        #     self.product_ids = None
        #     return {'domain': {
        #         'product_ids': [('id', '=', False)]}}

    @api.depends('date_from', 'date_to')
    def _period_days(self):
        """ Compute birthday value """
        for rec in self:
            age = dateutil.relativedelta.relativedelta(rec.date_to,
                                                       rec.date_from)
            rec.Period_days = (int(age.years) * 365) + (int(
                age.months) * 30) + int(age.days)

    def compute_forecasted_purchasing(self):
        product = []
        orders = []
        loc = []
        orders_pur = []
        qty = 0
        total_sold = 0
        total_purchase = 0
        stock_in_qty_from = 0
        stock_out_qty_from = 0
        stock_in_qty_to = 0
        stock_out_qty_to = 0
        last_purchase_price = 0

        self.forecasted_purchasing_information_ids.unlink()
        date_from = datetime(
            year=self.date_from.year,
            month=self.date_from.month,
            day=self.date_from.day,
        )
        date_to = datetime(
            year=self.date_to.year,
            month=self.date_to.month,
            day=self.date_to.day,
        )
        if self.warehouse_ids:
            sale_order = self.env['sale.order'].search([('state', '=', 'sale')])
            purchase_order = self.env['purchase.order'].search(
                [('state', '=', 'purchase')])
            for o in sale_order:
                if o.date_order >= date_from and o.date_order <= date_to:
                    orders.append(o.date_order)
            for p in purchase_order:
                if p.date_order >= date_from and p.date_order <= date_to:
                    orders_pur.append(p.date_order)
            sale_order_id = self.env['sale.order'].search(
                [('date_order', 'in', orders)])
            purchase_order_id = self.env['purchase.order'].search(
                [('date_order', 'in', orders_pur)])
            for lot in self.warehouse_ids:
                if self.product_ids:
                    for rec in self.product_ids:
                        product.append({'product_id': rec.id})
                        stock = self.env['stock.quant'].search(
                            [('product_id', '=', rec.id)])
                        for st in stock:
                            if st.location_id.usage == 'internal':
                                last_purchase_order = self.env[
                                    'purchase.order.line'].search(
                                    [('product_id', '=', rec.id)],
                                    order='id DESC',
                                    limit=1)
                                for last in last_purchase_order:
                                    last_purchase_price = last.price_unit
                                    print(last_purchase_price)
                                for move in self.warehouse_ids:
                                    move_in_from = self.env[
                                        'stock.move'].search(
                                        [(
                                            'location_dest_id', '=',
                                            move.lot_stock_id.id),
                                            ('product_id', '=', rec.id),
                                            ('date', '<', date_from)])
                                    move_out_from = self.env[
                                        'stock.move'].search(
                                        [('location_id', '=',
                                          move.lot_stock_id.id),
                                         ('product_id', '=', rec.id),
                                         ('date', '<', date_from)])

                                    for m in move_in_from:
                                        stock_in_qty_from += m.product_qty
                                    for o in move_out_from:
                                        stock_out_qty_from += o.product_qty

                                    move_in_to = self.env['stock.move'].search(
                                        [(
                                            'location_dest_id', '=',
                                            move.lot_stock_id.id),
                                            ('product_id', '=', rec.id),
                                            ('date', '<', date_to)])
                                    move_out_to = self.env['stock.move'].search(
                                        [('location_id', '=',
                                          move.lot_stock_id.id),
                                         ('product_id', '=', rec.id),
                                         ('date', '<', date_to)])

                                    for m in move_in_to:
                                        stock_in_qty_to += m.product_qty
                                    for o in move_out_to:
                                        stock_out_qty_to += o.product_qty

                                his_from = self.env[
                                    'product.product'].with_context(
                                    to_date=date_from).search(
                                    [('id', '=', rec.id)])
                                his_to = self.env[
                                    'product.product'].with_context(
                                    to_date=date_to).search(
                                    [('id', '=', rec.id)])

                                for p in sale_order_id:
                                    for line in p.order_line:
                                        if rec.id == line.product_id.id:
                                            total_sold += line.product_uom_qty
                                for p in purchase_order_id:
                                    for line in p.order_line:
                                        if rec.id == line.product_id.id:
                                            total_purchase += line.product_qty

                                if his_from.qty_available == 0 and his_to.qty_available == 0:
                                    raise ValidationError(
                                        _("Date from balance and Date to balance = 0"))
                                else:
                                    turn_over_rate = ((
                                                              his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                             (
                                                                     his_from.qty_available + his_to.qty_available) / 2)
                                if self.Period_days == 0:
                                    raise ValidationError(_("Period Days = 0"))
                                if self.minimum_replenish_period == 0:
                                    raise ValidationError(
                                        _("Minimum Replenish Period = 0"))
                                if self.replenish_period == 0:
                                    raise ValidationError(
                                        _("Replenish Period = 0"))

                                    # loc.append(lot.lot_stock_id.id)
                                if st.location_id.id == lot.lot_stock_id.id:
                                    qty += st.available_quantity
                                    self.forecasted_purchasing_information_ids = [
                                        (0, 0, {
                                            'product_id': rec.id,
                                            'on_hand': st.product_id.qty_available,
                                            'virtual_available': st.product_id.virtual_available,
                                            'total_sold_period': total_sold,
                                            'total_purchased_period': total_purchase,
                                            'date_from_balance': stock_in_qty_from - stock_out_qty_from,
                                            'date_to_balance': stock_in_qty_to - stock_out_qty_to,
                                            'last_purchase_price': last_purchase_price,
                                            'stock_warehouse_id': lot.id,
                                            'stock_location_id': st.location_id.id,
                                            'turn_over_rate': turn_over_rate,
                                            'minimum_quantity': ((((
                                                                           his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                                          (
                                                                                  his_from.qty_available + his_to.qty_available) / 2)) / self.Period_days) * self.minimum_replenish_period,
                                            'expected_quantity': ((((
                                                                            his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                                           (
                                                                                   his_from.qty_available + his_to.qty_available) / 2)) / self.Period_days) * self.replenish_period

                                        })]
                                    total_sold = 0
                                    total_purchase = 0
                                    stock_in_qty_from = 0
                                    stock_out_qty_from = 0
                                    stock_in_qty_to = 0
                                    stock_out_qty_to = 0
                else:
                    # for rec in lot.lot_stock_id:
                    #     location_id
                    #     product.append({'location_id': rec.lot_stock_id})
                    stock = self.env['stock.quant'].search(
                        [('location_id', '=', lot.lot_stock_id.id)])
                    for st in stock:
                        if st.location_id.usage == 'internal':
                            last_purchase_order = self.env[
                                'purchase.order.line'].search(
                                [('product_id', '=', st.product_id.id)],
                                order='id DESC',
                                limit=1)
                            for last in last_purchase_order:
                                last_purchase_price = last.price_unit
                                print(last_purchase_price)
                            for move in self.warehouse_ids:
                                move_in_from = self.env[
                                    'stock.move'].search(
                                    [(
                                        'location_dest_id', '=',
                                        move.lot_stock_id.id),
                                        ('product_id', '=', st.product_id.id),
                                        ('date', '<', date_from)])
                                move_out_from = self.env[
                                    'stock.move'].search(
                                    [('location_id', '=',
                                      move.lot_stock_id.id),
                                     ('product_id', '=', st.product_id.id),
                                     ('date', '<', date_from)])

                                for m in move_in_from:
                                    stock_in_qty_from += m.product_qty
                                for o in move_out_from:
                                    stock_out_qty_from += o.product_qty

                                move_in_to = self.env[
                                    'stock.move'].search(
                                    [(
                                        'location_dest_id', '=',
                                        move.lot_stock_id.id),
                                        ('product_id', '=', st.product_id.id),
                                        ('date', '<', date_to)])
                                move_out_to = self.env[
                                    'stock.move'].search(
                                    [('location_id', '=',
                                      move.lot_stock_id.id),
                                     ('product_id', '=', st.product_id.id),
                                     ('date', '<', date_to)])

                                for m in move_in_to:
                                    stock_in_qty_to += m.product_qty
                                for o in move_out_to:
                                    stock_out_qty_to += o.product_qty

                            his_from = self.env[
                                'product.product'].with_context(
                                to_date=date_from).search(
                                [('id', '=', st.product_id.id)])
                            his_to = self.env[
                                'product.product'].with_context(
                                to_date=date_to).search(
                                [('id', '=', st.product_id.id)])

                            for p in sale_order_id:
                                for line in p.order_line:
                                    if st.product_id.id == line.product_id.id:
                                        total_sold += line.product_uom_qty
                            for p in purchase_order_id:
                                for line in p.order_line:
                                    if st.product_id.id == line.product_id.id:
                                        total_purchase += line.product_qty

                            if his_from.qty_available == 0 and his_to.qty_available == 0:
                                raise ValidationError(
                                    _("Date from balance and Date to balance = 0"))
                            else:
                                turn_over_rate = ((
                                                          his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                         (
                                                                 his_from.qty_available + his_to.qty_available) / 2)
                            if self.Period_days == 0:
                                raise ValidationError(
                                    _("Period Days = 0"))
                            if self.minimum_replenish_period == 0:
                                raise ValidationError(
                                    _("Minimum Replenish Period = 0"))
                            if self.replenish_period == 0:
                                raise ValidationError(
                                    _("Replenish Period = 0"))

                                # loc.append(lot.lot_stock_id.id)
                            if st.location_id.id == lot.lot_stock_id.id:
                                qty += st.available_quantity
                                self.forecasted_purchasing_information_ids = [
                                    (0, 0, {
                                        'product_id': st.product_id.id,
                                        'on_hand': st.product_id.qty_available,
                                        'virtual_available': st.product_id.virtual_available,
                                        'total_sold_period': total_sold,
                                        'total_purchased_period': total_purchase,
                                        'date_from_balance': stock_in_qty_from - stock_out_qty_from,
                                        'date_to_balance': stock_in_qty_to - stock_out_qty_to,
                                        'last_purchase_price': last_purchase_price,
                                        'stock_warehouse_id': lot.id,
                                        'stock_location_id': st.location_id.id,
                                        'turn_over_rate': turn_over_rate,
                                        'minimum_quantity': ((((
                                                                       his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                                      (
                                                                              his_from.qty_available + his_to.qty_available) / 2)) / self.Period_days) * self.minimum_replenish_period,
                                        'expected_quantity': ((((
                                                                        his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                                       (
                                                                               his_from.qty_available + his_to.qty_available) / 2)) / self.Period_days) * self.replenish_period

                                    })]
                                total_sold = 0
                                total_purchase = 0
                                stock_in_qty_from = 0
                                stock_out_qty_from = 0
                                stock_in_qty_to = 0
                                stock_out_qty_to = 0
        elif self.product_category_ids:
            sale_order = self.env['sale.order'].search([('state', '=', 'sale')])
            purchase_order = self.env['purchase.order'].search(
                [('state', '=', 'purchase')])

            for o in sale_order:
                if o.date_order >= date_from and o.date_order <= date_to:
                    orders.append(o.date_order)
            for p in purchase_order:
                if p.date_order >= date_from and p.date_order <= date_to:
                    orders_pur.append(p.date_order)
            sale_order_id = self.env['sale.order'].search(
                [('date_order', 'in', orders)])
            purchase_order_id = self.env['purchase.order'].search(
                [('date_order', 'in', orders_pur)])
            for lot in self.product_category_ids:
                prod = self.env['product.product'].search(
                    [('categ_id', '=', lot.id)])
                for rec in prod:
                    product.append({'product_id': rec.id})
                    stock = self.env['stock.quant'].search(
                        [('product_id', '=', rec.id)])
                    for st in stock:
                        if st.location_id.usage == 'internal':
                            last_purchase_order = self.env[
                                'purchase.order.line'].search(
                                [('product_id', '=', rec.id)], order='id DESC',
                                limit=1)
                            for last in last_purchase_order:
                                last_purchase_price = last.price_unit
                                print(last_purchase_price)
                            for move in self.warehouse_ids:
                                move_in_from = self.env['stock.move'].search(
                                    [(
                                        'location_dest_id', '=',
                                        move.lot_stock_id.id),
                                        ('product_id', '=', rec.id),
                                        ('date', '<', date_from)])
                                move_out_from = self.env['stock.move'].search(
                                    [('location_id', '=', move.lot_stock_id.id),
                                     ('product_id', '=', rec.id),
                                     ('date', '<', date_from)])

                                for m in move_in_from:
                                    stock_in_qty_from += m.product_qty
                                for o in move_out_from:
                                    stock_out_qty_from += o.product_qty

                                move_in_to = self.env['stock.move'].search(
                                    [(
                                        'location_dest_id', '=',
                                        move.lot_stock_id.id),
                                        ('product_id', '=', rec.id),
                                        ('date', '<', date_to)])
                                move_out_to = self.env['stock.move'].search(
                                    [('location_id', '=', move.lot_stock_id.id),
                                     ('product_id', '=', rec.id),
                                     ('date', '<', date_to)])

                                for m in move_in_to:
                                    stock_in_qty_to += m.product_qty
                                for o in move_out_to:
                                    stock_out_qty_to += o.product_qty

                            his_from = self.env['product.product'].with_context(
                                to_date=date_from).search([('id', '=', rec.id)])
                            his_to = self.env['product.product'].with_context(
                                to_date=date_to).search([('id', '=', rec.id)])

                            for p in sale_order_id:
                                for line in p.order_line:
                                    if rec.id == line.product_id.id:
                                        total_sold += line.product_uom_qty
                            for p in purchase_order_id:
                                for line in p.order_line:
                                    if rec.id == line.product_id.id:
                                        total_purchase += line.product_qty

                            if his_from.qty_available == 0 and his_to.qty_available == 0:

                                turn_over_rate = 0
                            else:
                                turn_over_rate = ((
                                                          his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                         (
                                                                 his_from.qty_available + his_to.qty_available) / 2)
                            if self.Period_days == 0:
                                raise ValidationError(_("Period Days = 0"))
                            if self.minimum_replenish_period == 0:
                                raise ValidationError(
                                    _("Minimum Replenish Period = 0"))
                            if self.replenish_period == 0:
                                raise ValidationError(_("Replenish Period = 0"))
                            if turn_over_rate:
                                minimum_quantity = (
                                                           turn_over_rate / self.Period_days) * self.minimum_replenish_period
                                expected_quantity = (
                                                            turn_over_rate / self.Period_days) * self.replenish_period
                            else:
                                minimum_quantity = 0
                                expected_quantity = 0
                            w = self.warehouse_ids.search

                            # loc.append(lot.lot_stock_id.id)
                            # if st.location_id.id == lot.lot_stock_id.id:
                            #     qty += st.available_quantity
                            self.forecasted_purchasing_information_ids = [
                                (0, 0, {
                                    'product_id': rec.id,
                                    'on_hand': st.product_id.qty_available,
                                    'virtual_available': st.product_id.virtual_available,
                                    'total_sold_period': total_sold,
                                    'total_purchased_period': total_purchase,
                                    'date_from_balance': stock_in_qty_from - stock_out_qty_from,
                                    'date_to_balance': stock_in_qty_to - stock_out_qty_to,
                                    'last_purchase_price': last_purchase_price,
                                    'stock_warehouse_id': st.location_id.warehouse_id.id,
                                    'stock_location_id': st.location_id.id,
                                    'turn_over_rate': turn_over_rate,
                                    'minimum_quantity': minimum_quantity,
                                    'expected_quantity': expected_quantity

                                })]
                            total_sold = 0
                            total_purchase = 0
                            stock_in_qty_from = 0
                            stock_out_qty_from = 0
                            stock_in_qty_to = 0
                            stock_out_qty_to = 0
        else:
            sale_order = self.env['sale.order'].search([('state', '=', 'sale')])
            purchase_order = self.env['purchase.order'].search(
                [('state', '=', 'purchase')])

            for o in sale_order:
                if o.date_order >= date_from and o.date_order <= date_to:
                    orders.append(o.date_order)
            for p in purchase_order:
                if p.date_order >= date_from and p.date_order <= date_to:
                    orders_pur.append(p.date_order)
            sale_order_id = self.env['sale.order'].search(
                [('date_order', 'in', orders)])
            purchase_order_id = self.env['purchase.order'].search(
                [('date_order', 'in', orders_pur)])

            for rec in self.product_ids:
                stock = self.env['stock.quant'].search(
                    [('product_id', '=', rec.id)])
                for st in stock:
                    if st.location_id.usage == 'internal':
                        product.append({'product_id': rec.id})
                        last_purchase_order = self.env[
                            'purchase.order.line'].search(
                            [('product_id', '=', rec.id)], order='id DESC',
                            limit=1)
                        for last in last_purchase_order:
                            last_purchase_price = last.price_unit
                            print(last_purchase_price)

                        move_in_from = self.env['stock.move'].search(
                            [('location_dest_id', '=', st.location_id.id),
                             ('product_id', '=', rec.id),
                             ('date', '<', date_from)])
                        move_out_from = self.env['stock.move'].search(
                            [('location_id', '=', st.location_id.id),
                             ('product_id', '=', rec.id),
                             ('date', '<', date_from)])

                        for m in move_in_from:
                            stock_in_qty_from += m.product_qty
                        for o in move_out_from:
                            stock_out_qty_from += o.product_qty

                        move_in_to = self.env['stock.move'].search(
                            [('location_dest_id', '=', st.location_id.id),
                             ('product_id', '=', rec.id),
                             ('date', '<', date_to)])
                        move_out_to = self.env['stock.move'].search(
                            [('location_id', '=', st.location_id.id),
                             ('product_id', '=', rec.id),
                             ('date', '<', date_to)])

                        for m in move_in_to:
                            stock_in_qty_to += m.product_qty
                        for o in move_out_to:
                            stock_out_qty_to += o.product_qty

                        his_from = self.env['product.product'].with_context(
                            to_date=date_from).search([('id', '=', rec.id)])
                        his_to = self.env['product.product'].with_context(
                            to_date=date_to).search([('id', '=', rec.id)])

                        for p in sale_order_id:
                            for line in p.order_line:
                                if rec.id == line.product_id.id:
                                    total_sold += line.product_uom_qty
                        for p in purchase_order_id:
                            for line in p.order_line:
                                if rec.id == line.product_id.id:
                                    total_purchase += line.product_qty

                        if his_from.qty_available == 0 and his_to.qty_available == 0:
                            raise ValidationError(
                                _("Date from balance and Date to balance = 0"))
                        else:
                            turn_over_rate = ((
                                                      his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                     (
                                                             his_from.qty_available + his_to.qty_available) / 2)
                        if self.Period_days == 0:
                            raise ValidationError(_("Period Days = 0"))
                        if self.minimum_replenish_period == 0:
                            raise ValidationError(
                                _("Minimum Replenish Period = 0"))
                        if self.replenish_period == 0:
                            raise ValidationError(_("Replenish Period = 0"))

                            # for lot in self.warehouse_ids:
                            #     print('lot ',lot,'lot name',lot.lot_stock_id.name,'lot id',lot.id)
                            #     loc.append(lot.lot_stock_id.id)
                            #     if st.location_id.id == lot.lot_stock_id.id:
                            #         qty += st.available_quantity
                        self.forecasted_purchasing_information_ids = [
                            (0, 0, {
                                'product_id': rec.id,
                                'on_hand': st.product_id.qty_available,
                                'virtual_available': st.product_id.virtual_available,
                                'total_sold_period': total_sold,
                                'total_purchased_period': total_purchase,
                                'date_from_balance': stock_in_qty_from - stock_out_qty_from,
                                'date_to_balance': stock_in_qty_to - stock_out_qty_to,
                                'last_purchase_price': last_purchase_price,
                                'stock_warehouse_id': st.location_id.warehouse_id.id,
                                'stock_location_id': st.location_id.id,
                                'turn_over_rate': turn_over_rate,
                                'minimum_quantity': ((((
                                                               his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                              (
                                                                      his_from.qty_available + his_to.qty_available) / 2)) / self.Period_days) * self.minimum_replenish_period,
                                'expected_quantity': ((((
                                                                his_from.qty_available + total_purchase) - his_to.qty_available) / (
                                                               (
                                                                       his_from.qty_available + his_to.qty_available) / 2)) / self.Period_days) * self.replenish_period

                            })]
                        total_sold = 0
                        total_purchase = 0
                        stock_in_qty_from = 0
                        stock_out_qty_from = 0
                        stock_in_qty_to = 0
                        stock_out_qty_to = 0


class ForecastedPurchasingInformation(models.Model):
    """
        Initialize Forecasted Purchasing Information:
         - 
    """
    _name = 'forecasted.purchasing.information'
    _description = 'Forecasted Purchasing Information'
    _check_company_auto = True

    forecasted_purchasing_id = fields.Many2one(
        'forecasted.purchasing'
    )
    product_id = fields.Many2one(
        'product.product'
    )
    expected_quantity = fields.Float()
    minimum_quantity = fields.Float()
    on_hand = fields.Float()
    virtual_available = fields.Float()
    stock_warehouse_id = fields.Many2one(
        'stock.warehouse'
    )
    stock_location_id = fields.Many2one(
        'stock.location'
    )
    total_sold_period = fields.Float()
    total_purchased_period = fields.Float()
    date_from_balance = fields.Float()
    date_to_balance = fields.Float()
    turn_over_rate = fields.Float()
    last_purchase_price = fields.Float()
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    stock_picking_id = fields.Many2one('stock.picking.type',
                                       string='Deliver To')


class PurchaseOrder(models.Model):
    """
        Inherit Purchase Order:
         -
    """
    _inherit = 'purchase.order'

    forecasted_purchasing_id = fields.Many2one(
        'forecasted.purchasing'
    )
