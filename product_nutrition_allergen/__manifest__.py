# -*- coding: utf-8 -*-
#############################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
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
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Product Nutrition",
    "version": "18.0.1.0.0",
    "category": "eCommerce",
    "summary": "Nutrition and allergen information of products",
    "description": "We can add nutrition ,ingredient and allergen information"
                   "of products on the as product information and can displayed"
                   "on website for website sale",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': "https://www.cybrosys.com",
    'depends': ['product', 'website_sale'],
    'data': [
        'security/product_nutrition_allergen_groups.xml',
        'security/ir.model.access.csv',
        'report/product_nutrition_allergen_reports.xml',
        'report/product_nutrition_allergen_templates.xml',
        'views/website_product_template.xml',
        'views/product_template_views.xml'
    ],
    'assets':
        {
            'web.assets_frontend': [
                'product_nutrition_allergen/static/src/js/website_sale.js']
        },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False
}
