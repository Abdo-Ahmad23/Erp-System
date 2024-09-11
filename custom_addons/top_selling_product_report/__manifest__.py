# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY E SHMAZA(<https://www.e-shamza.com>).
#    Author:E SHMAZA(info@e-shmaza.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'E SHMAZA Product Creation Approval',
    'version': '15.0.1.0.0',
    'summary': 'Top Selling and Least Selling Product Reports',
    'description': 'Top Selling Products,Fast Moving Products,Most Selling Products,Top Growing Products,Least Selling Products,',
    'author': 'E SHMAZA',
    'maintainer': 'E SHMAZA',
    'company': 'E SHMAZA',
    'website': 'https://www.e-shmaza.com',
    'depends': ['base', 'sale_management', 'stock', 'sale'],
    'category': 'Sale',
    'data': ['wizard/top_selling_wizard.xml',
             'report/top_selling_report.xml',
             'report/top_selling_report_template.xml',
             'security/ir.model.access.csv'
             ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
