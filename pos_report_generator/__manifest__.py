# -*- coding: utf-8 -*-
################################################################################
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
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC
#    LICENSE (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
{
	'name': 'POS All in One Report Generator',
	'version': '18.0.1.0.0',
	'category': 'Point of Sale',
	'summary': """Dynamic Point Of Sale Reports.""",
	'description': """This module helps to generate reports based on Orders,
	Order Details, Products, Categories, Salespersons and Payments.""",
	'author': 'CBMS TECHNOLOGIES LTD',
	'company': 'CBMS TECHNOLOGIES LTD',
	'maintainer': 'CBMS TECHNOLOGIES LTD',
	'website': 'https://www.mycbms.com',
	'depends': ['stub_point_of_sale', 'stock', 'web'],
	'data': [
		'security/ir.model.access.csv',
		'report/pos_order_report_templates.xml',
		'views/pos_report_menus.xml',
	],
	'assets': {
		'web.assets_backend': [
			'pos_report_generator/static/src/js/PosReport.js',
			'pos_report_generator/static/src/xml/PosReport.xml',
			'pos_report_generator/static/src/css/pos_report.css',
		],
	},
	'images': ['static/description/banner.png'],
	'license': 'AGPL-3',
	'installable': True,
	'auto_install': False,
	'application': False,
}
