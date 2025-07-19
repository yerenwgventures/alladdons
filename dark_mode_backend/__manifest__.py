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
    "name": "Dark Mode Backend Theme",
    "version": "18.0.1.0.0",
    "category": "Theme/Backend",
    "summary": "Dark Mode Backend Theme for Odoo 18 community edition",
    "description": "Minimalist and elegant backend theme for Odoo 18,"
                   "Backend Theme, Theme",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': "https://www.cybrosys.com",
    'assets': {
        'web.assets_backend': {
            '/dark_mode_backend/static/src/scss/theme_accent.scss',
            '/dark_mode_backend/static/src/scss/datetimepicker.scss',
            '/dark_mode_backend/static/src/scss/theme.scss',
            'https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&amp;display=swap" rel="stylesheet',
        },
        'web.assets_frontend': {
            '/dark_mode_backend/static/src/scss/login.scss',
            'https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&amp;display=swap" rel="stylesheet',
        },
    },
    'images': [
        'static/description/banner.jpg',
        'static/description/theme_screenshot.jpg',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
