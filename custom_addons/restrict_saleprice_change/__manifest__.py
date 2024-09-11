# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.
# Author: Aktiv Software.
# mail:   info@eshmaza.com.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
#           Aktiv Software:
#               - Yash Shah
#               - Mital Parmar
#               - Harshil Soni

{
    "name": "Sale Price Change Restriction",
    "summary": """Restrict price change on orders""",
    "description": """
        When a product is selected for sale, And there is already a Pricelist applicable on product.
        Then only the users having rights to change the Priceof product can change its price on sale order.
    """,
    "author": "E SHMAZA",
    "website": "http://www.e-shmaza.com",
    "license": "AGPL-3",
    "category": "Sales",
    "version": "15.0.1.0.2",
    # any module necessary for this one to work correctly
    "depends": ["sale_management"],
    # always loaded
    "data": [
        "security/price_change_security.xml",
    ],
    "images": [
        "static/description/banner.jpg",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
