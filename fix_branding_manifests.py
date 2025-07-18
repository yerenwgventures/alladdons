#!/usr/bin/env python3
"""
Script to update branding in all __manifest__.py files
Replaces Cybrosys branding with CBMS TECHNOLOGIES LTD branding
"""
import os
import re
import sys

def update_manifest_branding(file_path):
    """Update branding in a single manifest file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update copyright header
        content = re.sub(
            r'Cybrosys Technologies Pvt\. Ltd\.',
            'CBMS TECHNOLOGIES LTD',
            content
        )
        
        content = re.sub(
            r'Copyright \(C\) \d{4}-TODAY Cybrosys Technologies\(<https://www\.cybrosys\.com>\)\.',
            'Copyright (C) 2025-TODAY CBMS TECHNOLOGIES LTD (<https://www.mycbms.com>).',
            content
        )
        
        # Update author email
        content = re.sub(
            r'Author: [^(]+\(odoo@cybrosys\.com\)',
            'Author: Development Team (info@mycbms.com)',
            content
        )
        
        # Update manifest fields
        content = re.sub(
            r"'author': 'Cybrosys Techno Solutions'",
            "'author': 'CBMS TECHNOLOGIES LTD'",
            content
        )
        
        content = re.sub(
            r"'company': 'Cybrosys Techno Solutions'",
            "'company': 'CBMS TECHNOLOGIES LTD'",
            content
        )
        
        content = re.sub(
            r"'maintainer': 'Cybrosys Techno Solutions'",
            "'maintainer': 'CBMS TECHNOLOGIES LTD'",
            content
        )
        
        content = re.sub(
            r"'website': 'https://www\.cybrosys\.com'",
            "'website': 'https://www.mycbms.com'",
            content
        )
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all manifest files"""
    updated_count = 0
    total_count = 0
    
    print("Starting manifest branding update...")
    
    # Find all __manifest__.py files
    for root, dirs, files in os.walk('.'):
        if '__manifest__.py' in files:
            manifest_path = os.path.join(root, '__manifest__.py')
            total_count += 1
            
            if update_manifest_branding(manifest_path):
                updated_count += 1
                print(f"Updated: {manifest_path}")
            
            # Progress indicator
            if total_count % 50 == 0:
                print(f"Processed {total_count} files...")
    
    print(f"\nCompleted! Updated {updated_count} out of {total_count} manifest files.")

if __name__ == "__main__":
    main()
