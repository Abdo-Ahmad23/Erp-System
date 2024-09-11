# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright © 2016 Techspawn Solutions. (<http://wwww.e-shmaza.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Warehouse Restrictions",

    'summary': """
         Warehouse and Stock Location Restriction on Users.""",

    'description': """
        This Module Restricts the User from Accessing Warehouse and Process Stock Moves other than allowed to Warehouses and Stock Locations.
    """,

    'author': "E SHMAZA",
    'website': "http://www.e-shmaza.com",
    'license': 'OPL-1',
    'category': 'Warehouse',
    'version': '15.0',
    'images': ['static/description/WarehouseRestrictions.jpg'],
    'depends': ['base', 'stock', 'sale_stock', 'sale'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/users_view.xml',
    ],

}
