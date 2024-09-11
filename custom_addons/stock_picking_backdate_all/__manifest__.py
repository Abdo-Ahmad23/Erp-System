{
    'name': 'Stock Picking Backdate',
    'version': '15.0.1.0.0',
    'category': 'Extra Tools',
    'author': "E SHMAZA",
    'website': "https://www.e-shmaza.com",
    'summary': 'assigning backdate to picking',
    'depends': [
        'stock', 'account'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/change_to_backdate_wiz.xml',
        'views/stock_picking_backdate_action.xml'
    ],
    'images': ['static/description/Banner.png'],
    'application': False,
    'installable': True,
    'auto_install': False,
}
