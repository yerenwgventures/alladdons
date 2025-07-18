# -*- coding: utf-8 -*-
###############################################################################
#
#    CBMS TECHNOLOGIES LTD
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Development Team (info@mycbms.com)
#
#    This program is free software: you can modify
#    it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE (LGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'Customer Image And Tags In POS',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Images and tags in pos customer session',
    'description': 'Can see the image and tags of customer in '
                   'customer selection page while choosing'
                   ' the customer in pos',
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos':[
            'customer_image_and_tags_in_pos/static/src/js/PartnerLine.js',
            'customer_image_and_tags_in_pos/static/src/js/customer_tag.js',
            'customer_image_and_tags_in_pos/static/src/xml/PartnerLine.xml',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'auto_install': False,
}
