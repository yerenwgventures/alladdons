#!/usr/bin/env python3
"""
Script to fix UI/UX consistency issues across modules
Adds missing kanban views and standardizes button placement
"""
import os
import xml.etree.ElementTree as ET

def create_kanban_view(module_name, model_name, display_field='name'):
    """Create a standard kanban view for a module"""
    kanban_content = f'''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Kanban View for {model_name} -->
    <record id="view_{model_name.replace('.', '_')}_kanban" model="ir.ui.view">
        <field name="name">{model_name}.kanban</field>
        <field name="model">{model_name}</field>
        <field name="arch" type="xml">
            <kanban default_group_by="state" class="o_kanban_small_column">
                <field name="{display_field}"/>
                <field name="state"/>
                <field name="create_date"/>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_card oe_kanban_global_click">
                            <div class="oe_kanban_content">
                                <div class="o_kanban_record_top">
                                    <div class="o_kanban_record_headings">
                                        <strong class="o_kanban_record_title">
                                            <field name="{display_field}"/>
                                        </strong>
                                    </div>
                                </div>
                                <div class="o_kanban_record_bottom">
                                    <div class="oe_kanban_bottom_left">
                                        <field name="create_date" widget="date"/>
                                    </div>
                                    <div class="oe_kanban_bottom_right">
                                        <field name="state" widget="label_selection" 
                                               options="{{'classes': {{'draft': 'default', 'confirmed': 'success'}}}}"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>
</odoo>'''
    
    kanban_file = f'{module_name}/views/{model_name.replace(".", "_")}_kanban_views.xml'
    os.makedirs(f'{module_name}/views', exist_ok=True)
    
    with open(kanban_file, 'w') as f:
        f.write(kanban_content)
    
    return kanban_file

def add_dashboard_view(module_name, model_name):
    """Add a dashboard view to a module"""
    dashboard_content = f'''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Dashboard View for {model_name} -->
    <record id="view_{model_name.replace('.', '_')}_dashboard" model="ir.ui.view">
        <field name="name">{model_name}.dashboard</field>
        <field name="model">{model_name}</field>
        <field name="arch" type="xml">
            <form string="Dashboard" create="false" edit="false" delete="false">
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" readonly="1"/>
                        </h1>
                    </div>
                    <group>
                        <group string="Statistics">
                            <field name="total_records" readonly="1"/>
                            <field name="records_today" readonly="1"/>
                            <field name="records_this_month" readonly="1"/>
                            <field name="active_records" readonly="1"/>
                        </group>
                    </group>
                    
                    <div class="row mt16">
                        <div class="col-lg-6">
                            <div class="card">
                                <div class="card-header">
                                    <h5>Quick Actions</h5>
                                </div>
                                <div class="card-body">
                                    <button name="action_view_records" 
                                            string="View All Records" 
                                            type="object" 
                                            class="btn btn-primary"/>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-6">
                            <div class="card">
                                <div class="card-header">
                                    <h5>Analytics</h5>
                                </div>
                                <div class="card-body">
                                    <p>Advanced analytics and reporting features would be displayed here.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Dashboard Action -->
    <record id="action_{model_name.replace('.', '_')}_dashboard" model="ir.actions.act_window">
        <field name="name">{model_name.replace('.', ' ').title()} Dashboard</field>
        <field name="res_model">{model_name}</field>
        <field name="view_mode">form</field>
        <field name="view_id" ref="view_{model_name.replace('.', '_')}_dashboard"/>
        <field name="target">current</field>
    </record>
</odoo>'''
    
    dashboard_file = f'{module_name}/views/{model_name.replace(".", "_")}_dashboard_views.xml'
    
    with open(dashboard_file, 'w') as f:
        f.write(dashboard_content)
    
    return dashboard_file

def update_manifest_with_views(module_name, new_view_files):
    """Update manifest to include new view files"""
    manifest_path = f'{module_name}/__manifest__.py'
    
    if not os.path.exists(manifest_path):
        return False
    
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Find data section
        import re
        pattern = r"('data': \[)(.*?)(\],)"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            data_start = match.group(1)
            data_content = match.group(2).strip()
            data_end = match.group(3)
            
            # Add new view files
            for view_file in new_view_files:
                view_ref = view_file.replace(f'{module_name}/', '')
                if view_ref not in data_content:
                    data_content += f",\n        '{view_ref}'"
            
            new_data = data_start + data_content + "\n    " + data_end
            content = content.replace(match.group(0), new_data)
            
            with open(manifest_path, 'w') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error updating manifest for {module_name}: {e}")
        return False

def enhance_ui_consistency(module_name, enhancements):
    """Enhance UI consistency for a module"""
    if not os.path.exists(module_name):
        print(f"Module {module_name} not found, skipping...")
        return False
    
    created_files = []
    
    for enhancement in enhancements:
        if enhancement == 'kanban':
            # Determine main model (simplified approach)
            main_model = f"{module_name}.{module_name.split('_')[-1]}"
            kanban_file = create_kanban_view(module_name, main_model)
            created_files.append(kanban_file)
            print(f"Created kanban view for {module_name}")
        
        elif enhancement == 'dashboard_view':
            main_model = f"{module_name}.dashboard"
            dashboard_file = add_dashboard_view(module_name, main_model)
            created_files.append(dashboard_file)
            print(f"Created dashboard view for {module_name}")
    
    # Update manifest
    if created_files:
        if update_manifest_with_views(module_name, created_files):
            print(f"Updated manifest for {module_name}")
    
    return len(created_files) > 0

def main():
    """Main function to fix UI consistency issues"""
    # Define modules needing UI improvements
    ui_improvements = {
        'project_task_risk_management_odoo': ['kanban'],
        'advanced_loan_management': ['kanban'],
        'gym_mgmt_system': ['kanban'],
        'medical_lab_management': ['kanban'],
        'hotel_management_odoo': ['kanban'],
        'cleaning_management': ['kanban'],
        'legal_case_management': ['kanban'],
        'salon_management': ['kanban'],
        'franchise_management': ['kanban'],
        'user_audit': ['dashboard_view'],
        'attendance_regularization': ['dashboard_view'],
        'hide_all_print_button': ['dashboard_view'],
        'low_stocks_product_alert': ['dashboard_view'],
        'auto_logout_idle_user_odoo': ['dashboard_view'],
    }
    
    improved_count = 0
    
    print("Starting UI consistency improvements...")
    
    for module_name, improvements in ui_improvements.items():
        if enhance_ui_consistency(module_name, improvements):
            improved_count += 1
            print(f"Improved UI for {module_name} with {', '.join(improvements)}")
        else:
            print(f"Failed to improve UI for {module_name}")
    
    print(f"\nCompleted! Improved UI for {improved_count} modules.")

if __name__ == "__main__":
    main()
