#!/usr/bin/env python3
"""
Script to fix XML view type issues in Odoo modules.
Removes incorrect <field name="type">...</field> lines from view definitions.
"""

import os
import re
import sys

def fix_xml_file(filepath):
    """Fix XML type issues in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match incorrect view type definitions
        # This matches lines like:    <field name="type">list</field>
        # But NOT lines like:        <field name="type" invisible="1"/>
        pattern = r'^\s*<field name="type">[^<]*</field>\s*$'
        
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Check if this line matches the incorrect pattern
            if re.match(pattern, line):
                # Check context - if it's in a view definition, remove it
                # Look for nearby <record model="ir.ui.view"> or similar
                context_start = max(0, i - 10)
                context_end = min(len(lines), i + 5)
                context = '\n'.join(lines[context_start:context_end])
                
                if 'ir.ui.view' in context and ('model' in line or 'arch' in context):
                    print(f"  Removing line {i+1}: {line.strip()}")
                    continue  # Skip this line
            
            fixed_lines.append(line)
        
        fixed_content = '\n'.join(fixed_lines)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix all XML files in base_accounting_kit."""
    module_path = 'base_accounting_kit'
    
    if not os.path.exists(module_path):
        print(f"Module path {module_path} not found!")
        return 1
    
    # Find all XML files with type issues
    xml_files = []
    for root, dirs, files in os.walk(module_path):
        for file in files:
            if file.endswith('.xml'):
                filepath = os.path.join(root, file)
                # Check if file contains type field definitions
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if 'field name="type"' in content:
                        xml_files.append(filepath)
                except:
                    continue
    
    print(f"Found {len(xml_files)} XML files with potential type issues")
    
    fixed_count = 0
    for filepath in xml_files:
        print(f"Processing: {filepath}")
        if fix_xml_file(filepath):
            fixed_count += 1
            print(f"  ✓ Fixed")
        else:
            print(f"  - No changes needed")
    
    print(f"\nFixed {fixed_count} files out of {len(xml_files)} total")
    return 0

if __name__ == '__main__':
    sys.exit(main())
