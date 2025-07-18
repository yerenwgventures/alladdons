#!/usr/bin/env python3
"""
Script to fix syntax errors in manifest files
Removes double commas and fixes formatting issues
"""
import os
import re

def fix_manifest_syntax(file_path):
    """Fix syntax errors in a manifest file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix double commas
        content = re.sub(r',,+', ',', content)
        
        # Fix trailing commas before closing brackets
        content = re.sub(r',\s*\]', '\n    ]', content)
        
        # Fix spacing around commas in data arrays
        content = re.sub(r"'([^']+)',\s*'", r"'\1',\n        '", content)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all manifest syntax errors"""
    # Files with known syntax errors
    files_with_errors = [
        './advanced_loan_management/__manifest__.py',
        './attendance_regularization/__manifest__.py',
        './cleaning_management/__manifest__.py',
        './franchise_management/__manifest__.py',
        './gym_mgmt_system/__manifest__.py',
        './hide_all_print_button/__manifest__.py',
        './hotel_management_odoo/__manifest__.py',
        './laundry_management/__manifest__.py',
        './legal_case_management/__manifest__.py',
        './medical_lab_management/__manifest__.py',
        './project_task_risk_management_odoo/__manifest__.py',
        './salon_management/__manifest__.py',
    ]
    
    fixed_count = 0
    
    print("Fixing manifest syntax errors...")
    
    for file_path in files_with_errors:
        if os.path.exists(file_path):
            if fix_manifest_syntax(file_path):
                print(f"Fixed syntax errors in {file_path}")
                fixed_count += 1
            else:
                print(f"No changes needed in {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nCompleted! Fixed syntax errors in {fixed_count} manifest files.")

if __name__ == "__main__":
    main()
