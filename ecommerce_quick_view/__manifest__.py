# -*- coding: utf-8 -*-
################################################################################
#
#    CBMS TECHNOLOGIES LTD
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Development Team (info@mycbms.com)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
################################################################################
{
    'name': 'Product Quickview in e-Commerce',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': "Quick View of Products in Product-listing Page.",
    'description': "Website Product Quickview module is used for enable the"
    "quickview option in eCommerce product listing, So that the"
    "visitors can load product info without redirected to another"
    "page.",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['stub_website_sale'],
    'data': [
        'views/quick_view_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/ecommerce_quick_view/static/src/js/quick_view_modal.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
