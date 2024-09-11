# pylint: disable=missing-docstring, manifest-required-author
{
    'name': 'Contact Address',
    'summary': 'Base module for Contact Address',
    'author': 'Younis Mostafa Khalaf',
    'website': '',
    'category': 'Hidden',
    'version': '16.0.1.0.0',
    'license': 'OPL-1',
    'depends': [
        'base',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/res_district.xml',
        'views/res_zone.xml',
        'views/building_type.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
