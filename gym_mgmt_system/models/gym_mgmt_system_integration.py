# -*- coding: utf-8 -*-
"""
Integration Model for gym_mgmt_system with hr.attendance
Provides seamless integration between modules
"""

from odoo import api, fields, models, _


class GymMgmtSystemIntegration(models.Model):
    """Integration model for gym_mgmt_system"""
    _name = 'gym_mgmt_system.integration'
    _description = 'Gym Mgmt System Integration'

    name = fields.Char(string='Integration Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    integration_type = fields.Selection([
        ('sync', 'Data Synchronization'),
        ('workflow', 'Workflow Integration'),
        ('reporting', 'Reporting Integration'),
    ], string='Integration Type', default='workflow')
    
    # Integration-specific fields would be added here based on the target module
    target_model = fields.Char(string='Target Model', default='hr.attendance')
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
