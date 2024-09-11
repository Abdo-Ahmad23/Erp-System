# -*- coding: utf-8 -*-
{
    'name': "Pharmacy Forecasted Purchasing",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "E SHMAZA",
    'website': "http://www.e-shmaza.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchasing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'stock', 'sale', 'point_of_sale', 'hr',
                'account_asset'],

    # always loaded
    'data': [
        'security/product_group.xml',
        'security/ir.model.access.csv',
        # 'wizard/assign_delivery.xml',
        # 'wizard/delivery_arrived.xml',
        # 'views/stock_picking.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/forecasted_purchasing.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
        'views/product_template.xml',
        'views/pos_payment.xml',
        'views/account_asset.xml',
        'views/res_users.xml',
        'views/pos_config.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pharmacy_forecasted_purchasing/static/src/js/client_fields.js',
        ],
        'web.assets_qweb': [
            'pharmacy_forecasted_purchasing/static/src/xml/client_fields.xml',
        ],
    }
}
