# -*- coding: utf-8 -*-
###############################################################################
#
# CBMS TECHNOLOGIES LTD
#
# Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
# Author: Development Team (info@mycbms.com)
#
# You can modify it under the terms of the GNU AFFERO
# GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
# You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
# (AGPL v3) along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'Quick Product Publish/Unpublish',
    'version': '18.0.1.0.0',
    'category': 'Website,eCommerce',
    'summary': """Quick Product Publish & Un publish on
     Website Shop""",
    'description': """This module helps to quick product 
     publish/Unpublish 
     on website shop,Also helps in multi product
     publish/unpublish and 
     category vise publish/unpublish""",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': "https://www.cybrosys.com",
    'depends': ['web', 'stub_website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'wizard/product_publish_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
