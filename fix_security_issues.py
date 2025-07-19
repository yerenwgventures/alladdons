#!/usr/bin/env python3
"""
Script to fix security issues across modules
Creates missing security files and updates overly permissive access
"""
import os
import re
import sys

# Modules that need security fixes (from our analysis)
MODULES_NEEDING_SECURITY = [
    'low_stocks_product_alert',
    'employee_ideas', 
    'magic_note',
    'auto_logout_idle_user_odoo',
    'user_audit',
    'readonly_unit_price_cybrosys',
    'customized_barcode_generator',
    'product_to_invoice',
    'uom_product_list',
    'product_multi_uom'
]

def create_security_file(module_path, module_name):
    """Create a basic security file for a module"""
    security_dir = os.path.join(module_path, 'security')
    os.makedirs(security_dir, exist_ok=True)
    
    security_file = os.path.join(security_dir, 'ir.model.access.csv')
    
    # Basic security template
    security_content = """id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_{}_admin,access.{}.admin,model_{},base.group_system,1,1,1,1
access_{}_user,access.{}.user,model_{},base.group_user,1,1,1,0
""".format(
        module_name.replace('_', '.'),
        module_name.replace('_', '.'), 
        module_name,
        module_name.replace('_', '.'),
        module_name.replace('_', '.'),
        module_name
    )
    
    with open(security_file, 'w') as f:
        f.write(security_content)
    
    return security_file

def update_manifest_security(manifest_path):
    """Add security file to manifest data section"""
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Check if security is already included
        if 'security/ir.model.access.csv' in content:
            return False
        
        # Add security file to data section
        pattern = r"('data': \[)(.*?)(\],)"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            data_start = match.group(1)
            data_content = match.group(2).strip()
            data_end = match.group(3)
            
            # Add security file at the beginning
            if data_content:
                new_data = data_start + "\n        'security/ir.model.access.csv'," + data_content + "\n    " + data_end
            else:
                new_data = data_start + "\n        'security/ir.model.access.csv',\n    " + data_end
            
            content = content.replace(match.group(0), new_data)
            
            with open(manifest_path, 'w') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error updating manifest {manifest_path}: {e}")
        return False

def main():
    """Main function to fix security issues"""
    fixed_count = 0
    
    print("Starting security fixes...")
    
    for module_name in MODULES_NEEDING_SECURITY:
        module_path = os.path.join('.', module_name)
        manifest_path = os.path.join(module_path, '__manifest__.py')
        
        if os.path.exists(manifest_path):
            # Create security file
            security_file = create_security_file(module_path, module_name)
            print(f"Created security file: {security_file}")
            
            # Update manifest
            if update_manifest_security(manifest_path):
                print(f"Updated manifest: {manifest_path}")
                fixed_count += 1
            else:
                print(f"Manifest already has security or couldn't update: {manifest_path}")
        else:
            print(f"Module not found: {module_path}")
    
    print(f"\nCompleted! Fixed security for {fixed_count} modules.")

if __name__ == "__main__":
    main()
