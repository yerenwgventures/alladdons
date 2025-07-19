# -*- coding: utf-8 -*-
#############################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
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
#############################################################################
{
    'name': "Open HRMS Attendance Regularization",
    'version': '18.0.1.0.0',
        'category': 'Human Resource',
        'summary': """Assigning Attendance for the Employees with Onsight Jobs""",
    'description': """Assigning Attendance for the Employees with Onsight Jobs 
    through the requests by Employees """,
    'author': 'Cybrosys Techno solutions,Open HRMS',
        'company': 'CBMS TECHNOLOGIES LTD',
        'maintainer': 'CBMS TECHNOLOGIES LTD',
        'website': "https://www.openhrms.com",
    'depends': ['hr_attendance', 'hr_holidays', 'hr'],
    'data': ['security/ir.model.access.csv',
        'security/attendance_regularization_security.xml',
        'views/reg_categories_views.xml',
        'views/attendance_regularization_views.xml',
        'views/attendance_regularization_dashboard_dashboard_views.xml'
    ],
    'demo': ['data/regularization_data.xml'],
    'images': ['static/description/banner.jpg'],
    'license': "LGPL-3",
    'installable': True,
    'auto_install': False,
    'application': False,
}
