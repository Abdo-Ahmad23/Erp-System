odoo.define('manage_delivery.partner_address', function (require) {
"use strict";

var models = require('point_of_sale.models');

models.load_fields("res.partner",["zone","building_floor","special_mark","area_region"]);

});