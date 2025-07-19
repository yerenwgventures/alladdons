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
from odoo import fields, models, _


class ApprovalRequest(models.Model):
    _name = 'approval.request'
    _description = 'Approval Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    """Standalone approval request model for sale order approvals"""

    name = fields.Char(string='Name', required=True, default='New')
    category_id = fields.Many2one('approval.category', string='Category', required=True)
    order_id = fields.Many2one('sale.order', string='Document',
                               help="Connection id for the sale order")
    state = fields.Selection([
        ('new', 'New'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancelled')
    ], string='Status', default='new', tracking=True)
    request_owner_id = fields.Many2one('res.users', string='Request Owner', default=lambda self: self.env.user)
    approver_ids = fields.One2many('approval.approver', 'request_id', string='Approvers')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)


    def action_approve(self, approver=None):
        """This method is used to confirm the order Approval"""
        self.state = 'approved'
        for order in [self.order_id]:
            if order:
                order.write({'state': 'approved', 'is_approved': True})
                order.message_post(
                    body=_('Requested approval is Confirmed'),
                    message_type='comment')
        return res

    def action_refuse(self, approver=None):
        """This method is used to reject the approval request"""
        self.state = 'refused'
        if self.order_id:
            self.order_id.write({'state': 'refused', 'is_approved': False})
            self.order_id.message_post(
                body=_('Requested approval is Refused'),
                message_type='comment')


class ApprovalApprover(models.Model):
    _name = 'approval.approver'
    _description = 'Approval Approver'

    request_id = fields.Many2one('approval.request', string='Request', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    status = fields.Selection([
        ('new', 'New'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], string='Status', default='new')
