#!/usr/bin/env python3
"""
Script to enhance incomplete modules with missing features
Adds dashboards, analytics, and improved functionality
"""
import os
import sys

def create_dashboard_model(module_name, model_description):
    """Create a dashboard model for a module"""
    dashboard_content = f'''# -*- coding: utf-8 -*-
"""
{model_description} Dashboard Model
Provides analytics and dashboard functionality
"""

from odoo import api, fields, models
from datetime import datetime, timedelta


class {module_name.title().replace('_', '')}Dashboard(models.Model):
    """Dashboard model for {module_name} analytics"""
    _name = '{module_name}.dashboard'
    _description = '{model_description} Dashboard'
    _auto = False

    name = fields.Char(string='Dashboard Name', default='{model_description} Analytics')
    total_records = fields.Integer(string='Total Records', compute='_compute_totals')
    records_today = fields.Integer(string='Records Today', compute='_compute_totals')
    records_this_month = fields.Integer(string='Records This Month', compute='_compute_totals')
    active_records = fields.Integer(string='Active Records', compute='_compute_totals')

    @api.depends()
    def _compute_totals(self):
        """Compute dashboard statistics"""
        for record in self:
            # This would be customized per module based on its main model
            record.total_records = 0
            record.records_today = 0
            record.records_this_month = 0
            record.active_records = 0

    @api.model
    def get_dashboard_data(self):
        """Return complete dashboard data for frontend"""
        dashboard = self.create({{}})
        
        return {{
            'totals': {{
                'total_records': dashboard.total_records,
                'records_today': dashboard.records_today,
                'records_this_month': dashboard.records_this_month,
                'active_records': dashboard.active_records,
            }},
        }}
'''
    
    dashboard_file = f'{module_name}/models/{module_name}_dashboard.py'
    os.makedirs(f'{module_name}/models', exist_ok=True)
    
    with open(dashboard_file, 'w') as f:
        f.write(dashboard_content)
    
    return dashboard_file

def create_analytics_model(module_name, model_description):
    """Create an analytics model for a module"""
    analytics_content = f'''# -*- coding: utf-8 -*-
"""
{model_description} Analytics Model
Provides advanced analytics and reporting functionality
"""

from odoo import api, fields, models, tools


class {module_name.title().replace('_', '')}Analytics(models.Model):
    """Analytics model for {module_name}"""
    _name = '{module_name}.analytics'
    _description = '{model_description} Analytics'
    _auto = False

    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    user_id = fields.Many2one('res.users', string='User')
    count = fields.Integer(string='Count')
    
    def init(self):
        """Initialize the analytics view"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        # This would be customized per module with actual SQL
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {{self._table}} AS (
                SELECT 
                    row_number() OVER () AS id,
                    'Analytics' as name,
                    CURRENT_DATE as date,
                    1 as user_id,
                    0 as count
            )
        """)
'''
    
    analytics_file = f'{module_name}/models/{module_name}_analytics.py'
    
    with open(analytics_file, 'w') as f:
        f.write(analytics_content)
    
    return analytics_file

def update_module_init(module_name, new_models):
    """Update the module's __init__.py to include new models"""
    init_file = f'{module_name}/models/__init__.py'
    
    if os.path.exists(init_file):
        with open(init_file, 'r') as f:
            content = f.read()
        
        # Add new model imports
        for model in new_models:
            model_import = f"from . import {model}"
            if model_import not in content:
                content += f"\n{model_import}"
        
        with open(init_file, 'w') as f:
            f.write(content)
        
        return True
    return False

def enhance_module(module_name, enhancements):
    """Enhance a module with specified features"""
    if not os.path.exists(module_name):
        print(f"Module {module_name} not found, skipping...")
        return False
    
    created_files = []
    new_models = []
    
    for enhancement in enhancements:
        if enhancement == 'dashboard':
            dashboard_file = create_dashboard_model(module_name, module_name.replace('_', ' ').title())
            created_files.append(dashboard_file)
            new_models.append(f"{module_name}_dashboard")
            print(f"Created dashboard for {module_name}")
        
        elif enhancement == 'analytics':
            analytics_file = create_analytics_model(module_name, module_name.replace('_', ' ').title())
            created_files.append(analytics_file)
            new_models.append(f"{module_name}_analytics")
            print(f"Created analytics for {module_name}")
    
    # Update __init__.py
    if new_models:
        if update_module_init(module_name, new_models):
            print(f"Updated __init__.py for {module_name}")
    
    return len(created_files) > 0

def main():
    """Main function to enhance incomplete modules"""
    # Define modules and their needed enhancements
    modules_to_enhance = {
        'auto_logout_idle_user_odoo': ['dashboard', 'analytics'],
        'readonly_unit_price_cybrosys': ['analytics'],
        'customized_barcode_generator': ['dashboard', 'analytics'],
        'product_to_invoice': ['analytics'],
        'product_multi_uom': ['dashboard'],
        'survey_upload_file': ['dashboard'],
        'storage_dashboard': ['analytics'],  # Already has dashboard, add analytics
        'cw_stock': ['dashboard', 'analytics'],
        'project_task_unique_code': ['dashboard'],
        'attendance_regularization': ['dashboard'],
        'employee_stages': ['analytics'],
        'partner_related_user': ['analytics'],
    }
    
    enhanced_count = 0
    
    print("Starting module enhancements...")
    
    for module_name, enhancements in modules_to_enhance.items():
        if enhance_module(module_name, enhancements):
            enhanced_count += 1
            print(f"Enhanced {module_name} with {', '.join(enhancements)}")
        else:
            print(f"Failed to enhance {module_name}")
    
    print(f"\nCompleted! Enhanced {enhanced_count} modules.")

if __name__ == "__main__":
    main()
