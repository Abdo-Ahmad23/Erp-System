# -*- coding: utf-8 -*-
{
    'name': "Warehouse Assimpling",

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
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'timer'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/factory_receipt_template.xml',
        'report/report.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/stock_picking_kanban.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
