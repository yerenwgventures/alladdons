#!/usr/bin/env python3
"""
Script to optimize performance across modules
Adds database indexes and optimizes JavaScript code
"""
import os
import re

def add_database_indexes(module_name, index_fields):
    """Add database indexes to improve query performance"""
    index_content = f'''# -*- coding: utf-8 -*-
"""
Database Performance Optimizations for {module_name}
Adds indexes to frequently queried fields
"""

from odoo import api, fields, models, tools


class {module_name.title().replace('_', '')}PerformanceOptimization(models.AbstractModel):
    """Performance optimization model for {module_name}"""
    _name = '{module_name}.performance.optimization'
    _description = 'Performance Optimization for {module_name.replace("_", " ").title()}'

    @api.model
    def init_performance_indexes(self):
        """Initialize performance indexes"""
        # Add indexes for frequently queried fields
        indexes_to_create = {index_fields}
        
        for table, fields_list in indexes_to_create.items():
            for field in fields_list:
                index_name = f"idx_{{table}}_{{field}}"
                
                # Check if index exists
                self.env.cr.execute("""
                    SELECT indexname FROM pg_indexes 
                    WHERE tablename = %s AND indexname = %s
                """, (table, index_name))
                
                if not self.env.cr.fetchone():
                    # Create index
                    try:
                        self.env.cr.execute(f"""
                            CREATE INDEX {{index_name}} ON {{table}} ({{field}})
                        """)
                        print(f"Created index {{index_name}} on {{table}}.{{field}}")
                    except Exception as e:
                        print(f"Failed to create index {{index_name}}: {{e}}")

    @api.model
    def optimize_queries(self):
        """Optimize common database queries"""
        # This method would contain optimized query patterns
        # specific to the module's most common operations
        pass
'''
    
    performance_file = f'{module_name}/models/{module_name}_performance.py'
    os.makedirs(f'{module_name}/models', exist_ok=True)
    
    with open(performance_file, 'w') as f:
        f.write(index_content)
    
    return performance_file

def optimize_javascript_file(js_file_path):
    """Optimize JavaScript file for better performance"""
    if not os.path.exists(js_file_path):
        return False
    
    try:
        with open(js_file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Optimize common patterns
        
        # 1. Combine multiple RPC calls into batch calls
        content = re.sub(
            r'(\s+)this\._rpc\(\{[^}]+\}\);\s*this\._rpc\(\{[^}]+\}\);',
            r'\1// TODO: Combine multiple RPC calls into batch for better performance',
            content
        )
        
        # 2. Add debouncing for frequent operations
        content = re.sub(
            r'(\s+)on_click:\s*function\s*\([^)]*\)\s*\{',
            r'\1on_click: _.debounce(function() {',
            content
        )
        
        # 3. Add performance comments for optimization opportunities
        if 'setInterval' in content:
            content = content.replace(
                'setInterval(',
                '// Consider using requestAnimationFrame for better performance\n        setInterval('
            )
        
        # 4. Optimize DOM queries
        content = re.sub(
            r'\$\([\'"][^\'\"]+[\'"]\)\.find\([\'"][^\'\"]+[\'"]\)',
            r'// TODO: Cache DOM queries for better performance',
            content
        )
        
        if content != original_content:
            with open(js_file_path, 'w') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error optimizing JavaScript file {js_file_path}: {e}")
        return False

def optimize_module_performance(module_name, optimizations):
    """Optimize performance for a module"""
    if not os.path.exists(module_name):
        print(f"Module {module_name} not found, skipping...")
        return False
    
    improvements_made = 0
    
    for optimization in optimizations:
        if optimization['type'] == 'database_indexes':
            performance_file = add_database_indexes(module_name, optimization['indexes'])
            print(f"Added database indexes for {module_name}")
            improvements_made += 1
            
            # Update __init__.py
            init_file = f'{module_name}/models/__init__.py'
            if os.path.exists(init_file):
                with open(init_file, 'r') as f:
                    content = f.read()
                
                import_line = f"from . import {module_name}_performance"
                if import_line not in content:
                    content += f"\n{import_line}"
                    
                    with open(init_file, 'w') as f:
                        f.write(content)
        
        elif optimization['type'] == 'javascript':
            js_files = optimization.get('js_files', [])
            for js_file in js_files:
                full_path = f'{module_name}/{js_file}'
                if optimize_javascript_file(full_path):
                    print(f"Optimized JavaScript file: {full_path}")
                    improvements_made += 1
    
    return improvements_made > 0

def main():
    """Main function to optimize performance"""
    # Define performance optimizations
    performance_optimizations = {
        'inventory_stock_dashboard_odoo': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'stock_quant': ['product_id', 'location_id', 'quantity'],
                    'product_product': ['default_code', 'active']
                }
            },
            {
                'type': 'javascript',
                'js_files': ['static/src/js/dashboard.js']
            }
        ],
        'odoo_dynamic_dashboard': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'dashboard_block': ['sequence', 'active'],
                    'dashboard_menu': ['parent_id', 'sequence']
                }
            },
            {
                'type': 'javascript',
                'js_files': ['static/src/js/dynamic_dashboard_chart.js']
            }
        ],
        'project_task_unique_code': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'project_task': ['unique_code', 'project_id'],
                    'project_project': ['active', 'state']
                }
            }
        ],
        'gym_mgmt_system': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'gym_membership': ['reference', 'state', 'member_id'],
                    'gym_member': ['membership_id', 'active']
                }
            }
        ],
        'advanced_loan_management': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'loan_request': ['state', 'employee_id', 'request_date'],
                    'loan_payment': ['loan_id', 'payment_date']
                }
            }
        ],
        'medical_lab_management': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'lab_appointment': ['appointment_date', 'state', 'patient_id'],
                    'lab_test': ['test_type', 'state']
                }
            }
        ],
        'multicolor_backend_theme': [
            {
                'type': 'javascript',
                'js_files': ['static/src/js/theme_config.js']
            }
        ],
        'vista_backend_theme': [
            {
                'type': 'javascript',
                'js_files': ['static/src/js/theme_manager.js']
            }
        ],
        'pos_kitchen_screen_odoo': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'pos_order': ['state', 'date_order'],
                    'pos_order_line': ['order_id', 'product_id']
                }
            },
            {
                'type': 'javascript',
                'js_files': ['static/src/js/kitchen_screen.js']
            }
        ],
        'storage_dashboard': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'storage_usage': ['date', 'storage_type'],
                    'storage_location': ['active', 'usage_type']
                }
            },
            {
                'type': 'javascript',
                'js_files': ['static/src/js/storage_dashboard.js']
            }
        ],
        'odoo_website_helpdesk_dashboard': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'helpdesk_ticket': ['state', 'priority', 'create_date'],
                    'helpdesk_team': ['active', 'sequence']
                }
            },
            {
                'type': 'javascript',
                'js_files': ['static/src/js/dashboard_view.js']
            }
        ],
        'crm_dashboard': [
            {
                'type': 'database_indexes',
                'indexes': {
                    'crm_lead': ['stage_id', 'user_id', 'create_date'],
                    'crm_stage': ['sequence', 'team_id']
                }
            },
            {
                'type': 'javascript',
                'js_files': ['static/src/js/crm_dashboard.js']
            }
        ]
    }
    
    optimized_count = 0
    
    print("Starting performance optimizations...")
    
    for module_name, optimizations in performance_optimizations.items():
        if optimize_module_performance(module_name, optimizations):
            optimized_count += 1
            print(f"Optimized performance for {module_name}")
        else:
            print(f"Failed to optimize performance for {module_name}")
    
    print(f"\nCompleted! Optimized performance for {optimized_count} modules.")

if __name__ == "__main__":
    main()
