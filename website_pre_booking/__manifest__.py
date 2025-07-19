# -*- coding: utf-8 -*-
#############################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Gayathri V(<https://www.cybrosys.com>)
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
#############################################################################
{
    'name': 'Website Pre Booking',
    'version': '18.0.1.0.1',
    'category': 'Website',
    'summary': 'Allows pre booking option for website',
    'description': """This module will help you to managing prebooking of
     product management in website""",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': "https://www.cybrosys.com",
    'depends': ['portal', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/portal_views.xml',
        'views/website_prebook_views.xml',
        'views/website_sale_inherit.xml',
        'views/prebook_details_template.xml',
        'views/pre_booking_template.xml',
        'views/product_template_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_pre_booking/static/src/css/prebooking.css',
            '/website_pre_booking/static/src/js/pre_booking.js'
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
