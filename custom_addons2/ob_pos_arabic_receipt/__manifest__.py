{
    "name": "Arabic PoS Receipt",
    "summary": """Custom Arabic Receipt POS.""",
    "category": "Point Of Sale",
    "version": "15.0",
    'author': 'Odoo Bin',
    'maintainer': 'Odoo Bin',
    'company': 'Odoo Bin',
    "depends": ['point_of_sale'],
    "data": [
        'security/ir.model.access.csv',
        'demo/demo.xml',
        'views/pos_config_view.xml',
        'views/receipt_design_view.xml',
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    'assets': {
        'point_of_sale.assets': [
            'ob_pos_arabic_receipt/static/src/js/models.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    "price": 4,
    "currency": 'USD',

}
