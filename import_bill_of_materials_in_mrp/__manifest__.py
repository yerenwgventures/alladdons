# -*- coding: utf-8 -*-
#############################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Ranjith R (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Import Bill Of Materials',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': """Import Bill of materials using CSV, Excel file""",
    'description': 'Using this module we can import bom by searching'
                   ' the products in diffrent ways in csv or excel files',
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['base', 'stock', 'mrp'],
    'data': {
        'security/ir.model.access.csv',
        'security/import_bom_security.xml',
        'views/bom_import_menu_view.xml',
        'wizards/bom_import_view.xml',
        'wizards/success_message_view.xml',
    },
    'assets': {
        'web.assets_backend': [
            'import_bill_of_materials_in_mrp/static/src/css/style.css'
        ],
    },
    'external_dependencies': {
        'python': [
            'openpyxl'
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
