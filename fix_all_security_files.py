#!/usr/bin/env python3
"""
Fix All Security Files with Model Reference Issues
Systematically fixes all security files with missing model references
"""
import os
import csv
from pathlib import Path

def find_model_name_in_module(module_path):
    """Find the actual model name defined in the module"""
    models_path = module_path / 'models'
    if not models_path.exists():
        return None
    
    model_names = []
    
    # Check all Python files in models directory
    for py_file in models_path.glob('*.py'):
        if py_file.name == '__init__.py':
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for _name = 'model.name' patterns
            import re
            name_patterns = re.findall(r"_name\s*=\s*['\"]([^'\"]+)['\"]", content)
            model_names.extend(name_patterns)
            
        except Exception as e:
            print(f"Error reading {py_file}: {e}")
    
    return model_names

def fix_security_file(security_file_path, module_name):
    """Fix a security file with correct model references"""
    if not security_file_path.exists():
        return False
    
    module_path = security_file_path.parent.parent
    model_names = find_model_name_in_module(module_path)
    
    if not model_names:
        print(f"  ⚠️ No model names found for {module_name}")
        return False
    
    try:
        # Read the CSV file
        with open(security_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Backup original
        backup_path = f"{security_file_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Parse CSV
        lines = content.strip().split('\n')
        if len(lines) < 2:
            return False
        
        header = lines[0]
        data_lines = lines[1:]
        
        fixed_lines = [header]
        fixes_made = []
        
        for line in data_lines:
            if not line.strip():
                continue
                
            parts = line.split(',')
            if len(parts) < 3:
                continue
            
            # Check if model_id needs fixing
            model_id = parts[2]
            
            # If it's a placeholder or incorrect reference
            if 'model_' + module_name.replace('_', '_') in model_id or 'model_' + module_name in model_id:
                # Use the first model name found
                primary_model = model_names[0]
                correct_model_id = f"model_{primary_model.replace('.', '_')}"
                parts[2] = correct_model_id
                fixes_made.append(f"Fixed model reference: {model_id} -> {correct_model_id}")
            
            fixed_lines.append(','.join(parts))
        
        if fixes_made:
            # Write fixed content
            with open(security_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(fixed_lines) + '\n')
            
            print(f"  ✅ Fixed {len(fixes_made)} model references")
            for fix in fixes_made:
                print(f"    • {fix}")
            return True
        else:
            print(f"  ℹ️ No fixes needed")
            return False
            
    except Exception as e:
        print(f"  ❌ Error fixing security file: {e}")
        return False

def main():
    print("🔧 FIXING ALL SECURITY FILES WITH MODEL REFERENCE ISSUES")
    print("=" * 70)
    
    # List of modules with known security file issues
    modules_with_security_issues = [
        'attendance_regularization',
        'readonly_unit_price_cybrosys', 
        'storage_dashboard',
        'survey_upload_file',
        'uom_product_list'
    ]
    
    fixed_count = 0
    
    for module_name in modules_with_security_issues:
        module_path = Path(module_name)
        
        if not module_path.exists():
            print(f"❌ Module {module_name} not found")
            continue
        
        print(f"\n🔍 Fixing {module_name}...")
        
        # Check for security files
        security_path = module_path / 'security'
        if not security_path.exists():
            print(f"  ⚠️ No security directory found")
            continue
        
        # Look for ir.model.access.csv
        access_file = security_path / 'ir.model.access.csv'
        if access_file.exists():
            if fix_security_file(access_file, module_name):
                fixed_count += 1
        else:
            print(f"  ⚠️ No ir.model.access.csv found")
    
    print(f"\n" + "=" * 70)
    print(f"📋 SECURITY FILES FIXING SUMMARY")
    print(f"=" * 70)
    print(f"✅ Fixed security files: {fixed_count}")
    print(f"📊 Modules processed: {len(modules_with_security_issues)}")
    
    if fixed_count > 0:
        print(f"\n🎯 NEXT STEPS:")
        print(f"  1. Test the fixed modules to ensure they install correctly")
        print(f"  2. Backup files (.backup) are available for rollback if needed")

if __name__ == "__main__":
    main()
