# -*- coding: utf-8 -*-
{
    'name': "Payslip Payment",
    'summary': """ """,
    'description': """ """,
    'author': "E ESHMAZA",
    'website': "http://www.e-shmaza.com",
    'category': 'HR',
    'version': '0.15',
    'depends': ['base', 'hr_payroll', 'account', 'hr'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/hr_payslip.xml',
    ],
}
