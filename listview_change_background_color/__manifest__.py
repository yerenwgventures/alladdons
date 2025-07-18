# -*- coding: utf-8 -*-
################################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Cybrosys Techno Solutions (Contact : odoo@cybrosys.com)
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
################################################################################
{
    'name': 'Listview Change Background Color',
    'version': '18.0.1.0.0',
    'summary': """Change Background Colors Of Most Priority Records In Tree or 
     List View""",
    'description': """Change background colors of important or favorite records
     or most priority records from tree/list view very easily and quickly 
     regardless of pagination limits.""",
    'category': 'Tools',
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'website': "https://www.cybrosys.com",
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'depends': ['base', 'web', 'crm', 'sale'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/banner.gif'],
    'assets': {
        'web.assets_backend': [
            'listview_change_background_color/static/src/css/color_picker.css',
            ('after', 'web/static/src/views/list/list_renderer.xml', 'listview_change_background_color/static/src/xml/color_picker.xml'),
            'listview_change_background_color/static/src/js/color_picker.js',
        ]
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
