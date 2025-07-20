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
################################################################################
{
    'name': 'Payment Proof Attachment',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': """Proof Attachment In Website for Odoo 17 Community and 
    Enterprise Edition.""",
    'description': """This module allows the customers to attach proof 
    attachments in the website""",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': [
        'stub_website_sale',
        'sale_management'
    ],
    'data': [
        'views/attachment_templates.xml',
        'data/payment_proof_attachment.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_proof_attachment/static/src/js/*.js',
            'payment_proof_attachment/static/src/css/payment_proof.css',
        ]
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
