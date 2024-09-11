# -*- coding: utf-8 -*-
{
    'name': "manage_delivery",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale', 'point_of_sale',
                'purchase', 'stock', 'sale_stock',
                'pharmacy_forecasted_purchasing', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/manage_delivery.xml',
        # 'views/delivery_boy.xml',
        'views/account_move.xml',
        'views/res_partner.xml',
        'views/account_payment.xml',
        'views/account_payment_register.xml',
        'views/stock_quant.xml',
        'wizard/select_delivery_invoice.xml',
        'views/sale_order.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'manage_delivery/static/src/js/partner_address.js',
        ],
        'web.assets_qweb': [
            'manage_delivery/static/src/xml/partner_address.xml',
        ],

    }
}
