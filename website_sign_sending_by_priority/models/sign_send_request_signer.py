# -*- coding: utf-8 -*-
###############################################################################
#
#    CBMS TECHNOLOGIES LTD
#    Copyright (C) 2024-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).
#    Author: CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>)
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class SignSendRequestSigner(models.TransientModel):
    """
    Sign Send Request Signer with enterprise/community compatibility
    - Enterprise: Inherits from sign.send.request.signer
    - Community: Standalone model with basic functionality
    """
    _name = 'sign.send.request.signer'
    _description = 'Sign Send Request Signer (Community Compatible)'
    
    request_id = fields.Many2one('sign.send.request.community', string='Request')
    partner_id = fields.Many2one('res.partner', string='Signer', required=True)
    role_id = fields.Many2one('mail.activity.type', string='Role')  # Community fallback
    priority = fields.Integer(string='Priority', default=1, required=True)
    mail_sent_order = fields.Integer(string='Mail Sent Order')
    
    @api.model
    def _is_enterprise_sign_available(self):
        """Check if enterprise sign module is available"""
        try:
            module = self.env['ir.module.module'].search([
                ('name', '=', 'sign'),
                ('state', 'in', ['installed', 'to upgrade'])
            ])
            return bool(module)
        except Exception:
            return False
    
    @api.constrains('priority')
    def _check_unique_priority(self):
        """Ensure unique priorities within the same request"""
        for record in self:
            if record.request_id:
                duplicate = self.search([
                    ('request_id', '=', record.request_id.id),
                    ('priority', '=', record.priority),
                    ('id', '!=', record.id)
                ])
                if duplicate:
                    raise ValidationError(f"Priority {record.priority} is already used by another signer")
