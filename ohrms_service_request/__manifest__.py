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
    'name': "Open HRMS Service Request",
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """For Requesting Services""",
    'description': """It allows employees to submit service requests related to 
     HR, such as IT support, asset maintenance, or administrative assistance.""",
    'author':  'Cybrosys Techno Solutions',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website':  'https://www.cybrosys.com',
    'depends': ['hr', 'stock', 'oh_employee_creation_from_user', 'project',
                'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'security/service_request_security.xml',
        'security/ohrms_service_request_groups.xml',
        'data/service_request_sequence.xml',
        'views/service_request_views.xml',
        'views/service_execute_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': "AGPL-3",
    'installable': True,
    'auto_install': False,
    'application': False,
}
