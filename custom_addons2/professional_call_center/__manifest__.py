# -*- coding: utf-8 -*-
{
    'name': "Professional Call Center",
    'summary': """ """,
    'description': """ """,
    'author': "Younis Mostafa Khalaf",
    'website': "www.e-shmaza.com",
    'category': 'Sales/Sales',
    'version': '0.1',
    'application': 'True',
    'depends': [
        'base',
        'sale',
        'contact_address',
        'hr',
        'sale_stock',
        'stock',
        'account',
        # 'product_card',
        # 'professional_delivery_management ',


    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/call_center_report.xml',
        'report/order_receipt_temp.xml',
        'report/reports.xml',
        'report/line_report.xml',
        'views/delivery_type.xml',
        'views/res_setting.xml',
        'views/call_center_order.xml',
        'views/stock_picking.xml',
        'views/account_move.xml',
        'views/res_partner.xml',
        'views/call_center_line.xml',
        'views/hr_employee.xml',
        'wizard/order_report_wizard.xml',
        'wizard/register_payment_wizard.xml',
        'views/ir_ui_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap'
        ],
        'web.assets_frontend': [
            'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap'
        ],
    }
}
