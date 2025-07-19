# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Ashwin T (odoo@cybrosys.com)
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
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    """ Inherited product.template to add field with enterprise/community compatibility """
    _inherit = 'product.template'

    # Enterprise edition: uses documents.document
    # Community edition: uses ir.attachment as fallback
    document_ids = fields.Many2many(
        comodel_name='ir.attachment',  # Default to community model
        string='Documents',
        help='Product documents (uses enterprise documents module if available, otherwise attachments)',
        domain=[('res_model', '=', 'product.template')]
    )

    # Enterprise compatibility fields
    enterprise_document_ids = fields.Many2many(
        'documents.document',
        string='Enterprise Documents',
        help='Enterprise documents (only available with documents module)',
        domain=[('type', '=', 'binary')]
    )

    @api.model
    def _is_enterprise_documents_available(self):
        """Check if enterprise documents module is available"""
        try:
            module = self.env['ir.module.module'].search([
                ('name', '=', 'documents'),
                ('state', 'in', ['installed', 'to upgrade'])
            ])
            return bool(module)
        except Exception:
            return False

    @api.depends('document_ids', 'enterprise_document_ids')
    def _compute_effective_documents(self):
        """Compute effective documents based on available edition"""
        for record in self:
            if record._is_enterprise_documents_available():
                # Use enterprise documents if available
                record.effective_document_count = len(record.enterprise_document_ids)
            else:
                # Fall back to attachments
                record.effective_document_count = len(record.document_ids)

    effective_document_count = fields.Integer(
        string='Document Count',
        compute='_compute_effective_documents',
        help='Total number of documents (enterprise or community)'
    )
