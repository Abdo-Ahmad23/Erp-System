# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'law',
    'category': 'Accounting/Accounting',
    'summary': 'Manage lowyers and customers',
    'description': "",
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'views/lines.xml',
        'reports/report_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
