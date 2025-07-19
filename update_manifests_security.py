#!/usr/bin/env python3
"""
Script to update manifest files to include security files
"""
import os
import re

modules = [
    'magic_note', 'user_audit', 'customized_barcode_generator', 
    'product_to_invoice', 'product_multi_uom', 'survey_upload_file', 
    'storage_dashboard', 'cw_stock', 'project_task_unique_code', 
    'attendance_regularization', 'employee_stages', 'partner_related_user'
]

def update_manifest_security(manifest_path):
    """Add security file to manifest data section"""
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Check if security is already included
        if 'security/ir.model.access.csv' in content:
            return False
        
        # Find data section and add security file
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

updated_count = 0
for module in modules:
    manifest_path = f'./{module}/__manifest__.py'
    if os.path.exists(manifest_path):
        if update_manifest_security(manifest_path):
            print(f"Updated manifest for {module}")
            updated_count += 1
        else:
            print(f"Manifest already has security or couldn't update: {module}")
    else:
        print(f"Manifest not found: {module}")

print(f"\nUpdated {updated_count} manifest files with security references.")
