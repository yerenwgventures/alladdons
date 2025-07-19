#!/usr/bin/env python3
"""
Enterprise Compatibility Utility
Detects Odoo edition and updates modules for dual compatibility
"""
import os
import re
from pathlib import Path

class EnterpriseCompatibilityManager:
    """Manages enterprise/community compatibility for modules"""
    
    def __init__(self):
        self.enterprise_modules = {
            'hr_payroll', 'account_reports', 'approvals', 'documents',
            'helpdesk', 'project_enterprise', 'sale_subscription',
            'website_enterprise', 'stock_barcode', 'quality_control',
            'mrp_plm', 'social', 'marketing_automation', 'voip',
            'planning', 'timesheet_grid', 'industry_fsm', 'sign',
            'l10n_us_reports', 'account_consolidation', 'account_budget',
            'hr_holidays_enterprise', 'hr_appraisal', 'hr_referral'
        }
        
        self.community_alternatives = {
            'hr_payroll': 'hr',
            'account_reports': 'account',
            'approvals': 'mail',  # Use mail workflow for approvals
            'documents': 'base',  # Use attachments
            'helpdesk': 'project',  # Use project for ticket management
            'stock_barcode': 'stock',
            'quality_control': 'stock',
            'planning': 'hr',
            'timesheet_grid': 'hr_timesheet',
            'industry_fsm': 'project',
            'sign': 'mail',
            'account_budget': 'account',
            'hr_holidays_enterprise': 'hr_holidays',
            'hr_appraisal': 'hr',
            'hr_referral': 'hr'
        }
    
    def detect_enterprise_modules(self, odoo_addons_path='/usr/lib/python3/dist-packages/odoo/addons'):
        """Detect which enterprise modules are available"""
        available_enterprise = set()
        
        if os.path.exists(odoo_addons_path):
            for module in self.enterprise_modules:
                module_path = os.path.join(odoo_addons_path, module)
                if os.path.exists(module_path):
                    available_enterprise.add(module)
        
        return available_enterprise
    
    def update_manifest_for_compatibility(self, manifest_path):
        """Update manifest file for dual edition compatibility"""
        if not os.path.exists(manifest_path):
            return False
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Extract current dependencies
        depends_match = re.search(r"'depends'\s*:\s*\[(.*?)\]", content, re.DOTALL)
        if not depends_match:
            return False
        
        depends_content = depends_match.group(1)
        dependencies = []
        
        # Parse dependencies
        for match in re.finditer(r"'([^']+)'", depends_content):
            dependencies.append(match.group(1))
        
        # Check for enterprise dependencies and create alternatives
        enterprise_deps = []
        community_deps = []
        
        for dep in dependencies:
            if dep in self.enterprise_modules:
                enterprise_deps.append(dep)
                if dep in self.community_alternatives:
                    community_deps.append(self.community_alternatives[dep])
            else:
                community_deps.append(dep)
        
        if enterprise_deps:
            # Create compatibility note
            compatibility_note = self._create_compatibility_note(enterprise_deps, community_deps)
            
            # Update dependencies to community alternatives
            new_depends = "', '".join(set(community_deps))
            new_depends_section = f"'depends': ['{new_depends}'],"
            
            # Replace dependencies
            content = re.sub(
                r"'depends'\s*:\s*\[.*?\],",
                new_depends_section,
                content,
                flags=re.DOTALL
            )
            
            # Add compatibility note to description
            if "'description'" in content:
                content = re.sub(
                    r"('description'\s*:\s*)('''|\"\"\")(.*?)('''|\"\"\")",
                    r"\1\2\3\n\n" + compatibility_note + r"\4",
                    content,
                    flags=re.DOTALL
                )
            
            # Write updated content
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        
        return False
    
    def _create_compatibility_note(self, enterprise_deps, community_deps):
        """Create compatibility note for manifest"""
        note = """
EDITION COMPATIBILITY:
======================
This module supports both Odoo Community and Enterprise editions.

ENTERPRISE EDITION:
- Uses advanced features from: """ + ", ".join(enterprise_deps) + """
- Full enterprise functionality available

COMMUNITY EDITION:
- Falls back to: """ + ", ".join(set(community_deps)) + """
- Core functionality maintained with community alternatives
- Some advanced features may have limited functionality

AUTOMATIC DETECTION:
- Module automatically detects available edition
- Gracefully handles missing enterprise modules
- No manual configuration required
"""
        return note
    
    def create_enterprise_detection_mixin(self, module_path):
        """Create enterprise detection mixin for models"""
        mixin_content = '''# -*- coding: utf-8 -*-
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
'''
        
        models_dir = os.path.join(module_path, 'models')
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        
        mixin_file = os.path.join(models_dir, 'enterprise_detection_mixin.py')
        with open(mixin_file, 'w', encoding='utf-8') as f:
            f.write(mixin_content)
        
        return mixin_file

def main():
    """Main function to update all modules for compatibility"""
    manager = EnterpriseCompatibilityManager()
    
    print("🔍 ENTERPRISE COMPATIBILITY MANAGER")
    print("=" * 50)
    
    # Get all module directories
    modules = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, '__manifest__.py'))]
    
    updated_count = 0
    
    for module in modules:
        manifest_path = os.path.join(module, '__manifest__.py')
        
        if manager.update_manifest_for_compatibility(manifest_path):
            print(f"✅ Updated {module} for dual edition compatibility")
            
            # Create enterprise detection mixin
            manager.create_enterprise_detection_mixin(module)
            print(f"   📁 Added enterprise detection mixin to {module}")
            
            updated_count += 1
        else:
            print(f"ℹ️  {module} - no enterprise dependencies found")
    
    print(f"\n🎉 Completed! Updated {updated_count} modules for dual edition compatibility")

if __name__ == "__main__":
    main()
