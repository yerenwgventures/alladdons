# -*- coding: utf-8 -*-
################################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Manasa T P (odoo@cybrosys.info)
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
    'name': "Employee Expense Report",
    'version': "18.0.1.0.0",
    'category': 'Human Resources',
    'summary': 'The administrator has the ability to view the expense reports '
               'of any employee they choose, while regular users can only '
               'access and view their own expense reports.',
    'description': "This apps helps Admin to print multiples employee "
                   "expense reports with custom dates and the print"
                   "the report of the current status like to submit, "
                   "submitted, approved, paid, refused, all, etc.",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['hr_expense'],
    'data': [
        'security/ir.model.access.csv',
        'report/expense_report_filter_reports.xml',
        'report/expense_report_filter_templates.xml',
        'wizard/expense_report_filter_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
