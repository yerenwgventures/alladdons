# -*- coding: utf-8 -*-
################################################################################

#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    This program is under the terms of the Odoo Proprietary License v1.0
#    (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#    USE OR OTHER DEALINGS IN THE SOFTWARE.
#
################################################################################
{
    'name': 'Account Report Send By Mail',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': "Create account report based on user requirements and send it "
               "by mail",
    'description': """
This app enables users to generate personalized account reports based on their email address.
Users have the flexibility to choose the type of report they want, catering to their specific needs.
After selecting the desired report type, users can input the recipients email address to seamlessly send the generated report.

EDITION COMPATIBILITY:
======================
This module supports both Odoo Community and Enterprise editions.

ENTERPRISE EDITION:
- Uses advanced account_reports module for enhanced reporting
- Full enterprise report templates and features
- Advanced scheduling and automation

COMMUNITY EDITION:
- Uses standard account module for basic reporting
- Core email functionality maintained
- Basic report templates available

AUTOMATIC DETECTION:
- Module automatically detects available edition
- Falls back to community reports if enterprise not available
- No manual configuration required
    """,
    'company': 'CBMS TECHNOLOGIES LTD',
    'author': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': 'https://www.mycbms.com',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/account_report_mail_template.xml',
        'wizard/send_mail_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'account_report_send_by_mail/static/src/css/send_mail_report.css',
            'account_report_send_by_mail/static/src/js/report_action.js',
            'account_report_send_by_mail/static/src/xml/report_action.xml',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': True,
    'application': True,
}
