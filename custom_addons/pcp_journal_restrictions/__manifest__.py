{
    'name': 'Journal Restrictions',
    'summary': 'Journal Restrictions',
    'author': "E SHMAZA",
    'company': 'E SHMAZA',
    'website': "https://www.e-shmaza.com",
    'version': '14.0.0.1.0',
    'category': 'technical',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'account',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        # 'report/',
        # 'wizard/',
        'views/res_users.xml',
        # 'data/',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
