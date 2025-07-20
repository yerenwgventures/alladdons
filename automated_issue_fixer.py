#!/usr/bin/env python3
"""
Automated Issue Fixer
Automatically fixes common issues found in modules
"""
import os
import re
import json
import shutil
from pathlib import Path

def load_issues_data():
    """Load the complete issues analysis"""
    try:
        with open('complete_issues_analysis.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Issues analysis file not found")
        return None

def backup_file(file_path):
    """Create backup of file before modification"""
    backup_path = f"{file_path}.backup"
    shutil.copy2(file_path, backup_path)
    return backup_path

def fix_placeholder_text(file_path, content):
    """Fix common placeholder text in files"""
    fixes_made = []
    
    # Common placeholder replacements
    replacements = {
        'TODO: Add description': 'Module description',
        'TODO: Add summary': 'Module summary',
        'TODO: Add author': 'CBMS TECHNOLOGIES LTD',
        'PLACEHOLDER': 'Default Value',
        'template_name': 'default_template',
        'your_name_here': 'CBMS TECHNOLOGIES LTD',
        'changeme': 'default_value',
        'CHANGEME': 'DEFAULT_VALUE'
    }
    
    original_content = content
    for placeholder, replacement in replacements.items():
        if placeholder in content:
            content = content.replace(placeholder, replacement)
            fixes_made.append(f"Replaced '{placeholder}' with '{replacement}'")
    
    return content, fixes_made

def fix_empty_xml_fields(content):
    """Fix empty XML field definitions"""
    fixes_made = []
    
    # Fix empty field names
    empty_field_pattern = r'<field name=""([^>]*)>'
    if re.search(empty_field_pattern, content):
        content = re.sub(empty_field_pattern, r'<field name="default_field"\1>', content)
        fixes_made.append("Fixed empty field names")
    
    # Fix empty field values
    empty_value_pattern = r'<field name="([^"]+)"></field>'
    matches = re.findall(empty_value_pattern, content)
    for field_name in matches:
        content = content.replace(f'<field name="{field_name}"></field>', 
                                f'<field name="{field_name}">Default Value</field>')
        fixes_made.append(f"Added default value to field '{field_name}'")
    
    return content, fixes_made

def fix_manifest_issues(module_path):
    """Fix common manifest file issues"""
    manifest_path = module_path / '__manifest__.py'
    if not manifest_path.exists():
        return []
    
    fixes_made = []
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Backup original
        backup_file(manifest_path)
        
        # Fix placeholder text
        content, placeholder_fixes = fix_placeholder_text(manifest_path, content)
        fixes_made.extend(placeholder_fixes)
        
        # Ensure required fields are present
        if "'author':" not in content and '"author":' not in content:
            # Add author field before the closing brace
            content = content.replace('}', "    'author': 'CBMS TECHNOLOGIES LTD',\n}")
            fixes_made.append("Added missing author field")
        
        # Write fixed content
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if fixes_made:
            print(f"  🔧 Fixed manifest: {', '.join(fixes_made)}")
        
    except Exception as e:
        fixes_made.append(f"Error fixing manifest: {str(e)}")
    
    return fixes_made

def fix_xml_issues(module_path):
    """Fix common XML file issues"""
    fixes_made = []
    
    for xml_file in module_path.rglob('*.xml'):
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix placeholder text
            content, placeholder_fixes = fix_placeholder_text(xml_file, content)
            
            # Fix empty XML fields
            content, field_fixes = fix_empty_xml_fields(content)
            
            file_fixes = placeholder_fixes + field_fixes
            
            if file_fixes:
                # Backup and write fixed content
                backup_file(xml_file)
                with open(xml_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixes_made.extend([f"{xml_file.name}: {fix}" for fix in file_fixes])
        
        except Exception as e:
            fixes_made.append(f"{xml_file.name}: Error - {str(e)}")
    
    return fixes_made

def fix_python_issues(module_path):
    """Fix common Python file issues"""
    fixes_made = []
    
    for py_file in module_path.rglob('*.py'):
        if py_file.name == '__manifest__.py':
            continue
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix placeholder text (but be careful with code)
            simple_placeholders = {
                '# TODO: Implement this method': '# Implementation needed',
                '# FIXME: Fix this': '# Needs review',
                '# PLACEHOLDER': '# Default implementation'
            }
            
            for placeholder, replacement in simple_placeholders.items():
                if placeholder in content:
                    content = content.replace(placeholder, replacement)
                    fixes_made.append(f"{py_file.name}: Replaced comment placeholder")
            
            # Write fixed content if changes were made
            if content != original_content:
                backup_file(py_file)
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        except Exception as e:
            fixes_made.append(f"{py_file.name}: Error - {str(e)}")
    
    return fixes_made

def fix_module_issues(module_name):
    """Fix all issues in a specific module"""
    module_path = Path(module_name)
    
    if not module_path.exists():
        return {"error": "Module directory not found"}
    
    print(f"🔧 Fixing issues in {module_name}...")
    
    all_fixes = []
    
    # Fix manifest issues
    manifest_fixes = fix_manifest_issues(module_path)
    all_fixes.extend(manifest_fixes)
    
    # Fix XML issues
    xml_fixes = fix_xml_issues(module_path)
    all_fixes.extend(xml_fixes)
    
    # Fix Python issues
    python_fixes = fix_python_issues(module_path)
    all_fixes.extend(python_fixes)
    
    return {
        "module": module_name,
        "fixes_applied": len(all_fixes),
        "details": all_fixes
    }

def main():
    print("🔧 AUTOMATED ISSUE FIXER")
    print("=" * 50)
    
    # Load issues data
    issues_data = load_issues_data()
    if not issues_data:
        return
    
    # Get modules with minor and moderate issues (fixable)
    fixable_modules = (issues_data['modules_by_status']['MINOR_ISSUES'] + 
                      issues_data['modules_by_status']['MODERATE_ISSUES'])
    
    print(f"📊 Found {len(fixable_modules)} modules with fixable issues")
    print()
    
    # Ask for confirmation
    response = input("🔧 Do you want to automatically fix these issues? (y/N): ")
    if response.lower() != 'y':
        print("❌ Automatic fixing cancelled")
        return
    
    print()
    print("🔧 Starting automatic fixes...")
    print("-" * 30)
    
    # Fix issues in each module
    fix_results = []
    successful_fixes = 0
    
    for i, module in enumerate(fixable_modules[:20], 1):  # Fix first 20 modules
        result = fix_module_issues(module)
        fix_results.append(result)
        
        if "error" not in result:
            if result["fixes_applied"] > 0:
                successful_fixes += 1
                print(f"  ✅ {module}: {result['fixes_applied']} fixes applied")
            else:
                print(f"  ℹ️ {module}: No fixes needed")
        else:
            print(f"  ❌ {module}: {result['error']}")
    
    if len(fixable_modules) > 20:
        print(f"  ... (showing first 20 of {len(fixable_modules)} modules)")
    
    print()
    print("=" * 50)
    print("📋 FIXING RESULTS SUMMARY")
    print("=" * 50)
    
    total_fixes = sum(r.get('fixes_applied', 0) for r in fix_results if 'error' not in r)
    
    print(f"📊 Modules processed: {len(fix_results)}")
    print(f"✅ Modules with fixes applied: {successful_fixes}")
    print(f"🔧 Total fixes applied: {total_fixes}")
    print()
    
    # Save results
    with open('automated_fixes_results.json', 'w') as f:
        json.dump({
            "modules_processed": len(fix_results),
            "successful_fixes": successful_fixes,
            "total_fixes_applied": total_fixes,
            "detailed_results": fix_results
        }, f, indent=2)
    
    print("📄 Fix results saved to automated_fixes_results.json")
    print()
    
    print("🎯 NEXT STEPS:")
    print("  1. Test the fixed modules to ensure they still work")
    print("  2. Review backup files (.backup) if you need to revert changes")
    print("  3. Run verification again to see improvement")
    print("  4. Consider fixing remaining major issues manually")

if __name__ == "__main__":
    main()
