# -*- coding: utf-8 -*-
{
    'name': 'POS Orderline Image',
    'version': '15.0.0.1',
    'summary': 'POS Orderline Image',
    'category': 'Sales/Point Of Sale',
    'author': 'Amr Gaber',
    'email': 'amrgaber024@gmail.com',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            'pos_orderline_img/static/src/css/order_line_image.css',
        ],
        'web.assets_qweb': [
            'pos_orderline_img/static/src/xml/**/*',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
