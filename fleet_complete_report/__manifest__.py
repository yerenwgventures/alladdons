# -*- coding: utf-8 -*-
################################################################################
#
#    CBMS TECHNOLOGIES LTD
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Development Team (info@mycbms.com)
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
################################################################################
{
    'name': 'Fleet Complete Report',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'This module allow to print complete fleet report.',
    'description': """This module allows to print complete fleet report, Which
    includes vehicle and contract details, services and driver history.""",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['fleet', 'hr_expense'],
    'data': [
        'security/ir.model.access.csv',
        'report/vehicle_detail_report_templates.xml',
        'report/vehicle_detail_reports.xml',
        'wizard/vehicle_detail_views.xml'
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
