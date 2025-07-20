# -*- coding: utf-8 -*-
#############################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
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
    'name': "Product Low Stock Alert",
    'version': '18.0.1.0.0',
    "category": 'Warehouse,Point of Sale',
    'summary': """Product Low Stock Alert Display in Point of Sale and 
    Product Views""",
    'description': """Module adds functionality to display product stock 
    alerts in the point of sale interface, indicating low stock levels for 
    products and also in the product template kanban and list view.""",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['product', 'stub_point_of_sale'],
    'data': ['security/ir.model.access.csv','views/res_config_settings_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/low_stocks_product_alert_dashboard_dashboard_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'low_stocks_product_alert/static/src/css/template_color.css',
        ],
        'point_of_sale._assets_pos': [
            'low_stocks_product_alert/static/src/xml/product_item_template.xml',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': "LGPL-3",
    'installable': True,
    'application': False,
    'auto_install': False,
}
