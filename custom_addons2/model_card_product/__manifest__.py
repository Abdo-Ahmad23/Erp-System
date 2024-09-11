# See LICENSE file for full copyright and licensing details.

{
    'name': 'Model Card Product',
    'version': '14.0.1.0.0',
    'category': 'Inventory',
    'license': 'AGPL-3',
    'author': 'E SHMAZA',
    'website': 'www.e-shmaza.com',
    'summary': '',
    'depends': [
        'base', 'account', 'stock', 'display_journal_items_transfer'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/card_product_report.xml',
        'wizard/card_product_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}
