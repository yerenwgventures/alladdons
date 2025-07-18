# -*- coding: utf-8 -*-
################################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Development Team (info@mycbms.com)
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
    'name': "Low Sales Report",
    'version': '18.0.1.0.0',
    'category': 'Sale',
    'summary': 'The tool to control poorly performing product',
    'description': 'Efficiently manage and analyze low sales with this module,'
                   'offering customizable criteria, flexible reporting '
                   'periods, and versatile presentation options in Odoo or '
                   'Excel. Tailor your analysis by filtering specific product'
                   'categories or sales teams, and choose between '
                   'template-wide insights or focus on individual product '
                   'variants for a comprehensive understanding of '
                   'under performing products.',
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['sale_management', 'crm', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_view.xml',
        'report/low_sale_pivot_view_report_view.xml',
        'wizard/low_sale_report_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'low_sale_report/static/src/js/low_sale_xlsx_report.js',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
