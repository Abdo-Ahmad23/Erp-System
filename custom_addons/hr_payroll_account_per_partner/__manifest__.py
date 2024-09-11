# -*- coding: utf-8 -*-
##############################################################################
#
#    E SHMAZA,
#    Copyright (C) 2020-2021 App-script  (<http://www.e-shmaza.com>).
#
##############################################################################
{
    'name': 'Payroll Account Per Employee - Enterprise Edition',
    'author': 'E SHMAZA,',
    'website': 'http://www.e-shmaza.com',
    'category': 'Human Resources/Payroll',
    'version': '15.0',
    'description': """ 
            Customize the integration between payroll and accounting.
            =========================================================

                Add wonderful feature as option that allow you to transfer payroll
            per every partner, to determine debit and credit for every 
            employee.
        """,
    'depends': ['hr_payroll_account'],

    'images': ['static/description/banner.jpg'],
    'data': [
        'views/payslip_view.xml'

    ],
    'demo': [],
    'license': 'LGPL-3',
    'currency': 'EUR',
    'price': '100'
}
