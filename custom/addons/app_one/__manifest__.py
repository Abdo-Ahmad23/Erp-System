{
    'name': 'app_one',
    'version': '1.0',
    'summary': 'A brief description of my module',
    'description': 'A longer description of what my module does',
    'author': 'Abdo',
    'category': 'Uncategorized',
    'depends': 
    [
        'base',
        'sale',
        'stock',
        'mail',
        'contacts',
        

    ],  # List of dependencies "inhertinces"
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',


        ],
    'assets': {
    'web.assets_backend': [
        'app_one/static/src/css/style.css',
    ],
    },
    'installable': True,
    'application': True,
    'license':'LGPL-3'
}