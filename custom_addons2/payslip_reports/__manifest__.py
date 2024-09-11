{
    'name': "Payslip Reports",
    'summary': """ """,
    'author': "E ESHMAZA",
    'website': "https://www.e-shmaza.com",
    'category': 'Payslip',
    'version': '0.15',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_payroll', 'hr', 'report_xlsx'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        'views/hr_employee.xml',
    ],

}
