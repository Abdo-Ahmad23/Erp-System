{
    'name': 'Erp System',
    'version': '1.0',
    'summary': 'summary for erp system',
    'description': 'A longer description of what my module does',
    'author': 'Abdo',
    'category': 'Uncategorized',
    'depends': ['base'],  # List of dependencies "inhertinces"
    'data': [
    'security/ir.model.access.csv',
    'views/brand_view.xml',
    'views/base_menu.xml',
    'views/product_view.xml',
    'views/category_view.xml',
    'views/stock_view.xml',
    'views/store_view.xml',
    'views/item_view.xml',
    'views/order_view.xml',
    'views/customer_view.xml',
    'views/staff_view.xml',

    
    ],
    'installable': True,
    'application': True,
    'license':'LGPL-3'
}