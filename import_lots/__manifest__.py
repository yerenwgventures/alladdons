# -*- coding: utf-8 -*-
###############################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Development Team (info@mycbms.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC
#    LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'Import Lot from Excel',
    'version': '18.0.1.0.0',
    'category': 'Warehouse',
    'summary': """Import/add lots while validating a purchase order picking.""",
    'description': """This module helps to import lots and add to products in
    purchase order line while validating stock picking.""",
    'author': 'Cybrosys Techno Solution',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'Cybrosys Techno Solution',
    'website': 'https://www.mycbms.com',
    'depends': ['stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_move_views.xml',
        'wizard/lots_attachment_view_form.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'import_lots/static/src/*.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto-install': False,
    'application': False,
}
