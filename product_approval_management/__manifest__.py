# -*- coding: utf-8 -*-
###############################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
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
#
###############################################################################
{
    'name': "Product Approval",
    'version': '18.0.1.0.1',
    'category': "Extra tools",
    'summary': 'Product approval allow you to control the product creation',
    'description': "Using this module a user can create product which"
                   "will be in draft state and only a product manager can"
                   "confirm the product.Also only the confirmed products"
                   "can be selected from sale order line",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': "https://www.cybrosys.com",
    'depends': ['sale_management'],
    'data': ['security/product_approval_management_groups.xml',
             'security/ir.model.access.csv',
             'views/product_template_views.xml',
             'views/product_product_views.xml',
             'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'post_init_hook': '_default_product_confirm',
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
