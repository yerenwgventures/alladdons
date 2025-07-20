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
    'name': 'POS Chat Box',
    'category': 'Point Of Sale',
    'version': '18.0.1.0.0',
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'summary': """POS Chat Box For Odoo18 Community and Enterprise Edition""",
    'description': """Using the POS screen, this module facilitates user '
                   'communication.""",
    'depends': ['web','stub_point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pos_chatter/static/src/xml/pos_systray_icon.xml',
            '/pos_chatter/static/src/js/pos_systray_icon.js',
            '/pos_chatter/static/src/js//pos_msg_view.js',
            '/pos_chatter/static/src/js/pos_chat_view.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
