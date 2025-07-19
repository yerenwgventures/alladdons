# -*- coding: utf-8 -*-
###############################################################################
#
#    CBMS TECHNOLOGIES LTD
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Development Team (info@mycbms.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0(OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#    OTHERWISE,ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#    USE OR OTHER DEALINGS IN THE SOFTWARE.
#
###############################################################################
{
    'name': 'Product Multi Document',
    'version': '18.0.1.0.0',
    'category': 'Purchases,Discuss',
    'summary': """Multiple documents can be attached to a product with the help
    of this module.""",
    'description': """This module helps to add multiple documents in product
    and we can see these documents while we are selecting a product in purchase
    order line and automatically get attached in Email.


EDITION COMPATIBILITY:
======================
This module supports both Odoo Community and Enterprise editions.

ENTERPRISE EDITION:
- Uses advanced features from: documents
- Full enterprise functionality available

COMMUNITY EDITION:
- Falls back to: base, purchase
- Core functionality maintained with community alternatives
- Some advanced features may have limited functionality

AUTOMATIC DETECTION:
- Module automatically detects available edition
- Gracefully handles missing enterprise modules
- No manual configuration required
""",
    'author': 'CBMS TECHNOLOGIES LTD',
    'company': 'CBMS TECHNOLOGIES LTD',
    'maintainer': 'CBMS TECHNOLOGIES LTD',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'purchase'],
    'data': [
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
