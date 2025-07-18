# -*- coding: utf-8 -*-
###################################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
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
###################################################################################
{
    'name': 'Ecommerce Barcode Search',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Ecommerce Barcode Search',
    'description': 'This module enables users to search for products on the website using barcodes.'
                   'It adds a barcode input field to the website’s product search functionality,'
                   'allowing customers to quickly find specific products by scanning or entering barcodes.'
                   'This is especially useful in retail or wholesale environments where barcodes are used'
                   'extensively for inventory and product identification. The module supports both standard barcode'
                   ' formats and custom codes linked to products, enhancing the overall user experience and'
                   ' streamlining the search process.',

   'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'images': ['static/description/banner.jpg'],
    'website': 'https://www.mycbms.com',
    'depends': ['website_sale'],
    'data': ['views/website_sale_template.xml'],
    'assets': {
        'web.assets_frontend': [
            'ecommerce_barcode_search/static/src/js/WebsiteSaleBarcode.js',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
