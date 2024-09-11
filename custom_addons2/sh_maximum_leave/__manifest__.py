# -*- coding: utf-8 -*-
# Copyright (C) E SHMAZA.
{
    "name": "Maximum Leave Alert",

    'author': 'E SHMAZA',

    "license": "OPL-1",

    'website': 'https://www.e-shmaza.com',

    "support": "support@e-shmaza.com",

    'version': '15.0.1',

    'category': "Human Resources",

    'summary': "Manage Maximum Leave, Maximum Leave Alert, Max Leave Alert Module, Leave Management App, Maximum Leave Alert, More Leave Notification,Leave Custom Popup, Wrong Leave Warning Popup Odoo",
    'description': """
    This module useful to set maximum vacation days in holiday type as well as this module useful to check maximum leave days applicable in leave. For example, on Christmas, your company provides only 5 days' leave and any employee applies to leave for 7 days at Christmas then it will give a warning message. You can also set a maximum number of vacations in a month. For example, If your company provides 4 days of legal leave in a month, any employee applies for 5-day leaves in a month then it will give a warning message. This module also uses to set leaves like parenthood, The Hajj, etc.
Manage Maximum Leave Odoo, Maximum Leave Alert Odoo
 Set Alert For Max Leave Module, Leave Management, More Leave Alert, Notification For Maximum Leave, Custom Popup For Some Leaves, Warning For Wrong Days Leave Odoo.
 Max Leave Alert Module, Leave Management App, Maximum Leave Alert, More Leave Notification,Leave Custom Popup, Wrong Leave Warning Popup Odoo.

""",

    "depends": ['hr', 'hr_holidays'],

    "data": [
        'views/hr_max_leaves.xml',
    ],

    'images': ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/efOsAsnDrCM",
    "installable": True,
    "application": True,
    "autoinstall": False,
    "price": 20,
    "currency": "EUR"
}
