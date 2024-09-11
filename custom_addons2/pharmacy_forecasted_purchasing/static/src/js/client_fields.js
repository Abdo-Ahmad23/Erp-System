odoo.define('pharmacy_forecasted_purchasing.client_fields', function (require) {
"use strict";

var models = require('point_of_sale.models');
var PaymentScreen = require('point_of_sale.PaymentScreen');
var ProductScreen = require('point_of_sale.ProductScreen');
var ActionpadWidget = require('point_of_sale.ActionpadWidget');
var core = require('web.core');
var utils = require('web.utils');

var round_pr = utils.round_precision;

var _t = core._t;

var chrome = require("point_of_sale.chrome");

models.load_fields('pos.config','is_call_center');
models.load_fields('res.partner','special_marque');
models.load_fields('res.partner','customer_code');
models.load_fields('res.partner','mobile');
models.load_fields('res.partner','mobile_2');
models.load_fields('res.partner','mobile_3');
models.load_fields('res.partner','mobile_4');
models.load_fields('res.partner','mobile_5');
models.load_fields('res.partner','stock_warehouse_id');


    ActionpadWidget.addControlButton({
            component: ActionpadWidget,
            condition: function() {
                return this.env.pos.config.is_call_center;
            },
        });


});
