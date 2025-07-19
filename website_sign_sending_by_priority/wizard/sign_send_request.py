# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Raneesha MK (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License
#    v1.0 (OPL-1). It is forbidden to publish, distribute, sublicense, or sell
#    copies of the Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###############################################################################
from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SignSendRequest(models.TransientModel):
    """
    Sign Send Request with enterprise/community compatibility
    - Enterprise: Inherits from sign.send.request
    - Community: Standalone model with basic functionality
    """

    @api.model
    def _get_model_name(self):
        """Get the appropriate model name based on available modules"""
        if self._is_enterprise_sign_available():
            return 'sign.send.request'
        else:
            return 'sign.send.request.community'

    # Dynamic inheritance based on enterprise availability
    _name = 'sign.send.request.community'
    _description = 'Sign Send Request (Community Compatible)'

    # Community fields (basic functionality)
    name = fields.Char(string='Request Name', required=True)
    template_id = fields.Many2one('mail.template', string='Template')
    signer_ids = fields.One2many('sign.send.request.signer', 'request_id', string='Signers')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft')

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

    def create_request(self):
        """Creating the request based on the signers with enterprise/community compatibility"""
        if self._is_enterprise_sign_available():
            # Use enterprise functionality
            return self._create_enterprise_request()
        else:
            # Use community fallback
            return self._create_community_request()

    def _create_enterprise_request(self):
        """Enterprise version of create_request"""
        template_id = self.template_id.id
        signers = [
            {'partner_id': signer.partner_id.id, 'role_id': signer.role_id.id,
             'priority': signer.priority} for signer in self.signer_ids]
        # Check for duplicate priorities
        priority_set = set()
        for signer in signers:
            if signer['priority'] in priority_set:
                raise ValidationError("Duplicate priority found. Please set unique priorities")
            priority_set.add(signer['priority'])
        # Sort signers based on priority
        signers = sorted(signers, key=lambda x: x['priority'])
        # Assign mail_sent_order and create the sign request
        for index, signer in enumerate(signers):
            signer['mail_sent_order'] = index + 1
        cc_partner_ids = self.cc_partner_ids.ids
        sign_request = self.env['sign.request'].create({
            'template_id': template_id,
            'request_item_ids': [Command.create({
                'partner_id': signer['partner_id'],
                'role_id': signer['role_id'],
                'mail_sent_order': signer['mail_sent_order'],
            }) for signer in signers],
            'reference': self.filename,
            'subject': self.subject,
            'message': self.message,
            'message_cc': self.message_cc,
            'attachment_ids': [Command.set(self.attachment_ids.ids)],
        })
        sign_request.message_subscribe(partner_ids=cc_partner_ids)
        return sign_request

    def _create_community_request(self):
        """Community version of create_request using mail templates"""
        _logger.info("Using community sign request functionality")

        # Basic validation
        if not self.signer_ids:
            raise ValidationError("Please add at least one signer")

        # Check for duplicate priorities
        priorities = [signer.priority for signer in self.signer_ids]
        if len(priorities) != len(set(priorities)):
            raise ValidationError("Duplicate priority found. Please set unique priorities")

        # Sort signers by priority
        sorted_signers = self.signer_ids.sorted('priority')

        # Create mail activity or send emails based on priority
        self.state = 'sent'

        # For community edition, we'll create activities for each signer in order
        for signer in sorted_signers:
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': f'Sign Document: {self.name}',
                'note': f'Please sign the document. Priority: {signer.priority}',
                'user_id': signer.partner_id.user_ids[0].id if signer.partner_id.user_ids else self.env.user.id,
                'res_model': 'sign.send.request.community',
                'res_id': self.id,
            })

        return self

    def send_request(self):
        """Sending the request to the corresponding signers based on
        the priority """
        request = self.create_request()
        current_signer = self.signer_ids.filtered(
            lambda s: s.partner_id == self.env.user.partner_id)
        if current_signer.priority == 1:
            if self.activity_id:
                self._activity_done()
                return {'type': 'ir.actions.act_window_close'}
            return request.go_to_document()
        else:
            return request.go_to_document()
