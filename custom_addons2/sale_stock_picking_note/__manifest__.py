# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.e-shmaza.com).
{
    "name": "Sale Stock Picking Note",
    "summary": "Add picking note in sale and purchase order",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "website": "https://www.e-shmaza.com",
    "author": "E SHMAZA",
    "license": "AGPL-3",
    "depends": ["sale_stock"],
    "data": [
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
        "views/report_deliveryslip.xml",
    ],
    "installable": True,
}
