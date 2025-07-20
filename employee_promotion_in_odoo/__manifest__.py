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
    'name': "Employee Promotion",
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': ' This module helps to manage the proper employee promotion '
               'process.',
    'description': 'With the help of this module you can set promotion for'
                   'employee. Also, the promotion is visible on each employee '
                   'form.',
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['mail', 'stub_hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_promotion_views.xml',
        'views/promotion_type_views.xml',
        'views/hr_employee_views.xml',
        'report/employee_promotion_report.xml',
        'report/employee_promotion_templates.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
