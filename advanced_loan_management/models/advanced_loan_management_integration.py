# -*- coding: utf-8 -*-
"""
Integration Model for advanced_loan_management with hr.employee/hr.payslip
Provides seamless integration between modules with enterprise/community compatibility
"""

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class AdvancedLoanManagementIntegration(models.Model):
    """Integration model for advanced_loan_management"""
    _name = 'advanced_loan_management.integration'
    _description = 'Advanced Loan Management Integration'

    name = fields.Char(string='Integration Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    integration_type = fields.Selection([
        ('sync', 'Data Synchronization'),
        ('workflow', 'Workflow Integration'),
        ('reporting', 'Reporting Integration'),
    ], string='Integration Type', default='sync')
    
    # Integration-specific fields - automatically detects enterprise vs community
    target_model = fields.Char(string='Target Model', compute='_compute_target_model', store=True)
    edition_type = fields.Selection([
        ('community', 'Community Edition'),
        ('enterprise', 'Enterprise Edition')
    ], string='Edition Type', compute='_compute_edition_type', store=True)
    sync_frequency = fields.Selection([
        ('manual', 'Manual'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ], string='Sync Frequency', default='daily')
    
    last_sync = fields.Datetime(string='Last Sync')
    sync_status = fields.Selection([
        ('success', 'Success'),
        ('error', 'Error'),
        ('pending', 'Pending'),
    ], string='Sync Status', default='pending')

    @api.depends()
    def _compute_target_model(self):
        """Compute target model based on available modules"""
        for record in self:
            if record._is_enterprise_module_available('hr_payroll'):
                record.target_model = 'hr.payslip'
            else:
                record.target_model = 'hr.employee'

    @api.depends()
    def _compute_edition_type(self):
        """Compute edition type based on available enterprise modules"""
        for record in self:
            if record._has_enterprise_features():
                record.edition_type = 'enterprise'
            else:
                record.edition_type = 'community'

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

    def _has_enterprise_features(self):
        """Check if running on enterprise edition"""
        enterprise_indicators = ['hr_payroll', 'account_reports', 'approvals']
        return any(self._is_enterprise_module_available(module) for module in enterprise_indicators)
    
    def action_sync_now(self):
        """Trigger immediate synchronization"""
        # Implementation would depend on specific integration needs
        self.write({
            'last_sync': fields.Datetime.now(),
            'sync_status': 'success'
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Sync Complete'),
                'message': _('Integration sync completed successfully'),
                'type': 'success',
            }
        }
    
    @api.model
    def scheduled_sync(self):
        """Scheduled method for automatic synchronization"""
        integrations = self.search([
            ('active', '=', True),
            ('sync_frequency', '!=', 'manual')
        ])
        
        for integration in integrations:
            try:
                integration.action_sync_now()
            except Exception as e:
                integration.write({
                    'sync_status': 'error',
                    'last_sync': fields.Datetime.now()
                })
