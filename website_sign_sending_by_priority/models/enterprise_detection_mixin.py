# -*- coding: utf-8 -*-
"""
Enterprise Detection Mixin
Provides enterprise/community edition detection and compatibility
"""

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class EnterpriseDetectionMixin(models.AbstractModel):
    """Mixin to detect enterprise modules and provide fallbacks"""
    _name = 'enterprise.detection.mixin'
    _description = 'Enterprise Detection Mixin'
    
    @api.model
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
    
    @api.model
    def _get_enterprise_model_or_fallback(self, enterprise_model, fallback_model):
        """Get enterprise model if available, otherwise fallback"""
        try:
            if enterprise_model in self.env:
                return self.env[enterprise_model]
            else:
                _logger.info(f"Enterprise model {enterprise_model} not available, using {fallback_model}")
                return self.env[fallback_model]
        except Exception as e:
            _logger.warning(f"Error accessing models: {e}, using fallback {fallback_model}")
            return self.env[fallback_model]
    
    @api.model
    def _has_enterprise_features(self):
        """Check if running on enterprise edition"""
        enterprise_indicators = [
            'hr_payroll', 'account_reports', 'approvals', 'documents'
        ]
        
        for module in enterprise_indicators:
            if self._is_enterprise_module_available(module):
                return True
        return False
    
    @api.model
    def _get_edition_info(self):
        """Get current edition information"""
        return {
            'is_enterprise': self._has_enterprise_features(),
            'available_enterprise_modules': [
                module for module in [
                    'hr_payroll', 'account_reports', 'approvals', 'documents',
                    'helpdesk', 'project_enterprise', 'sale_subscription'
                ] if self._is_enterprise_module_available(module)
            ]
        }
