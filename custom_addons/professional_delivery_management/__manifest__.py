# -*- coding: utf-8 -*-
{
    'name': "Professional Delivery Management",
    'summary': """""",
    'description': """""",
    'author': "Younis Mostafa Khalaf",
    'website': "www.e-shmaza.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base',
        'account',
        'contact_address',
        'professional_call_center',
        'user_types',
        'portal',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/server_action.xml',
        'views/account_move.xml',
        'views/res_partner.xml',
        'views/res_users.xml',
        'views/delivery_portal_template.xml',
        'views/account_payment.xml',
        'wizard/assign_delivery_boy.xml',
        'wizard/delivery_boy_bill.xml',
        'views/ir_ui_menu.xml',
        'reports/report_order.xml'
    ],
}
