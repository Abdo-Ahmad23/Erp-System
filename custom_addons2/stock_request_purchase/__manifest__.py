# Copyright 2017-20 ForgeFlow S.L. (https://www.e-shmaza.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock Request Purchase",
    "summary": "Internal request for stock",
    "version": "15.0.1.0.1",
    "license": "LGPL-3",
    "website": "https://www.e-shmaza.com",
    "author": "E SHMAZA",
    "category": "Warehouse Management",
    "depends": ["stock_request", "purchase_stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_request_views.xml",
        "views/stock_request_order_views.xml",
        "views/purchase_order_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
