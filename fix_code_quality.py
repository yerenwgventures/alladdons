#!/usr/bin/env python3
"""
Script to improve code quality across modules
Adds missing docstrings and improves method documentation
"""
import os
import re
import sys

def add_docstring_to_method(file_path, method_name, docstring):
    """Add docstring to a method if it's missing"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to find method without docstring
        pattern = rf'(def {method_name}\([^)]*\):\s*\n)(\s*)((?!"""|\'\'\'|\s*"""|\s*\'\'\')[^\n])'
        
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            indent = match.group(2)
            # Add docstring with proper indentation
            new_content = content.replace(
                match.group(0),
                f'{match.group(1)}{indent}"""{docstring}"""\n{indent}{match.group(3)}'
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def improve_module_documentation(module_path):
    """Improve documentation for a specific module"""
    models_path = os.path.join(module_path, 'models')
    if not os.path.exists(models_path):
        return 0
    
    improved_count = 0
    
    for file_name in os.listdir(models_path):
        if file_name.endswith('.py') and file_name != '__init__.py':
            file_path = os.path.join(models_path, file_name)
            
            # Common method patterns that need docstrings
            methods_to_document = [
                ('create', 'Create a new record with the given values.'),
                ('write', 'Update the record with the given values.'),
                ('unlink', 'Delete the current record.'),
                ('name_get', 'Return the display name for the record.'),
                ('_compute_', 'Compute field value based on other fields.'),
                ('_onchange_', 'Handle field change event.'),
                ('action_', 'Execute action method.'),
            ]
            
            for method_pattern, default_docstring in methods_to_document:
                if add_docstring_to_method(file_path, method_pattern, default_docstring):
                    improved_count += 1
                    print(f"Added docstring to {method_pattern} in {file_path}")
    
    return improved_count

def main():
    """Main function to improve code quality"""
    # Focus on modules identified as needing improvement
    modules_to_improve = [
        'hide_all_print_button',
        'readonly_unit_price_cybrosys', 
        'magic_note',
        'user_audit',
        'auto_logout_idle_user_odoo',
        'customized_barcode_generator',
        'product_multi_uom',
        'survey_upload_file',
        'storage_dashboard',
        'cw_stock'
    ]
    
    total_improved = 0
    
    print("Starting code quality improvements...")
    
    for module_name in modules_to_improve:
        module_path = os.path.join('.', module_name)
        if os.path.exists(module_path):
            improved = improve_module_documentation(module_path)
            total_improved += improved
            print(f"Improved {improved} methods in {module_name}")
        else:
            print(f"Module not found: {module_name}")
    
    print(f"\nCompleted! Improved documentation for {total_improved} methods.")

if __name__ == "__main__":
    main()
