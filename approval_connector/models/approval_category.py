# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#   Author: AFRA MP (odoo@cybrosys.com)
#
#   This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#   It is forbidden to publish, distribute, sublicense, or sell copies of the
#   Software or modified copies of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#   OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#   USE OR OTHER DEALINGS IN THE SOFTWARE.
#
###############################################################################
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class ApprovalCategory(models.Model):
    _name = 'approval.category'
    _description = 'Approval Category'
    """
    Approval category model with enterprise/community compatibility
    - Uses enterprise approvals module if available
    - Falls back to custom implementation for community edition
    """

    name = fields.Char(string='Name', required=True)
    approval_type = fields.Selection([
        ('purchase', "Create RFQ's"),
        ('sale', 'Sale'),
    ], string="Approval Type", required=True)
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    sequence = fields.Integer(string='Sequence', default=10)
    has_product = fields.Selection([
        ('no', 'None'),
        ('optional', 'Optional'),
        ('required', 'Required')
    ], string='Product', default='no')
    has_quantity = fields.Selection([
        ('no', 'None'),
        ('optional', 'Optional'),
        ('required', 'Required')
    ], string='Quantity', default='no')
    automated_sequence = fields.Boolean(string='Automated Sequence', default=False)
    sequence_code = fields.Char(string='Sequence Code')

    # Enterprise compatibility fields
    is_enterprise_available = fields.Boolean(
        string='Enterprise Available',
        compute='_compute_enterprise_availability',
        help="Indicates if enterprise approvals module is available"
    )

    @api.depends()
    def _compute_enterprise_availability(self):
        """Check if enterprise approvals module is available"""
        for record in self:
            try:
                enterprise_module = self.env['ir.module.module'].search([
                    ('name', '=', 'approvals'),
                    ('state', 'in', ['installed', 'to upgrade'])
                ])
                record.is_enterprise_available = bool(enterprise_module)
            except Exception:
                record.is_enterprise_available = False

    @api.model
    def get_approval_model(self):
        """Get the appropriate approval model based on edition"""
        if self._is_enterprise_module_available('approvals'):
            try:
                return self.env['approval.category']  # Enterprise model
            except Exception:
                pass
        return self  # Community fallback

    def _is_enterprise_module_available(self, module_name):
        """Check if an enterprise module is available"""
        try:
            module = self.env['ir.module.module'].search([
                ('name', '=', module_name),
                ('state', 'in', ['installed', 'to upgrade'])
            ])
            return bool(module)
        except Exception:
            return False
