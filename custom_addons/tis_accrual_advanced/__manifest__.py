# -- coding: utf-8 --
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

{
    'name': 'Accrual Advanced',
    'version': '15.0.0.0',
    'category': 'Human Resources',
    'sequence': 1,
    'author': 'E SHMAZA.',
    'summary': 'Advanced Accrual Leaves Allocation.',
    'description': """Advanced Accrual Leaves Allocation""",
    'website': 'http://www.e-shmaza.com',
    'depends': ['hr_holidays'],
    'price': 19.99,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'data': [
        'views/hr_leave_allocation_views.xml',
        'views/hr_employee_views.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False
}
