#!/usr/bin/env python3
"""
Comprehensive Module Verification Script
Checks for incomplete features, placeholders, missing files, and manifest issues
"""
import os
import ast
import re
import json
from pathlib import Path

def check_manifest_file(module_path):
    """Check manifest file for completeness and issues"""
    manifest_path = os.path.join(module_path, '__manifest__.py')
    if not os.path.exists(manifest_path):
        return {"error": "No __manifest__.py file found"}
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the manifest
        tree = ast.parse(content)
        manifest_dict = ast.literal_eval(tree.body[0].value)
        
        issues = []
        
        # Check for placeholder values
        if manifest_dict.get('name', '').lower() in ['module name', 'todo', 'placeholder', '']:
            issues.append("Placeholder name")
        
        if manifest_dict.get('summary', '').lower() in ['todo', 'placeholder', '']:
            issues.append("Placeholder summary")
            
        if manifest_dict.get('description', '').lower() in ['todo', 'placeholder', '']:
            issues.append("Placeholder description")
            
        if manifest_dict.get('author', '').lower() in ['todo', 'placeholder', '']:
            issues.append("Placeholder author")
        
        # Check for missing required fields
        required_fields = ['name', 'version', 'depends', 'data']
        for field in required_fields:
            if field not in manifest_dict:
                issues.append(f"Missing {field}")
        
        # Check data files exist
        data_files = manifest_dict.get('data', [])
        missing_files = []
        for data_file in data_files:
            file_path = os.path.join(module_path, data_file)
            if not os.path.exists(file_path):
                missing_files.append(data_file)
        
        if missing_files:
            issues.append(f"Missing data files: {missing_files}")
        
        return {
            "manifest": manifest_dict,
            "issues": issues,
            "data_files": data_files,
            "missing_files": missing_files
        }
        
    except Exception as e:
        return {"error": f"Error parsing manifest: {str(e)}"}

def check_python_files(module_path):
    """Check Python files for placeholders and incomplete code"""
    issues = []
    
    # Check models directory
    models_path = os.path.join(module_path, 'models')
    if os.path.exists(models_path):
        for py_file in Path(models_path).glob('*.py'):
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for common placeholders
            placeholders = ['TODO', 'FIXME', 'XXX', 'PLACEHOLDER', 'pass  # TODO']
            for placeholder in placeholders:
                if placeholder.lower() in content.lower():
                    issues.append(f"{py_file.name}: Contains {placeholder}")
            
            # Check for incomplete class definitions
            if 'class ' in content and 'pass' in content:
                if content.count('pass') > content.count('def '):
                    issues.append(f"{py_file.name}: Possibly incomplete class definitions")
    
    return issues

def check_xml_files(module_path):
    """Check XML files for placeholders and incomplete definitions"""
    issues = []
    
    # Check views, data, security directories
    for subdir in ['views', 'data', 'security']:
        dir_path = os.path.join(module_path, subdir)
        if os.path.exists(dir_path):
            for xml_file in Path(dir_path).glob('*.xml'):
                with open(xml_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check for placeholders
                placeholders = ['TODO', 'FIXME', 'PLACEHOLDER', 'template_name']
                for placeholder in placeholders:
                    if placeholder.lower() in content.lower():
                        issues.append(f"{xml_file.name}: Contains {placeholder}")
                
                # Check for incomplete XML
                if '<record' in content and not '</record>' in content:
                    issues.append(f"{xml_file.name}: Incomplete XML records")
                
                # Check for empty fields
                if 'field name=""' in content or "field name=''" in content:
                    issues.append(f"{xml_file.name}: Empty field names")
    
    return issues

def verify_module(module_name):
    """Comprehensive verification of a single module"""
    module_path = os.path.join('.', module_name)
    
    if not os.path.isdir(module_path):
        return {"error": "Module directory not found"}
    
    verification_result = {
        "module": module_name,
        "manifest_check": check_manifest_file(module_path),
        "python_issues": check_python_files(module_path),
        "xml_issues": check_xml_files(module_path),
        "directory_structure": []
    }
    
    # Check directory structure
    expected_dirs = ['models', 'views', 'data', 'security', 'static']
    for dir_name in expected_dirs:
        dir_path = os.path.join(module_path, dir_name)
        if os.path.exists(dir_path):
            file_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
            verification_result["directory_structure"].append(f"{dir_name}: {file_count} files")
    
    return verification_result

def main():
    print("🔍 COMPREHENSIVE MODULE VERIFICATION")
    print("=" * 50)
    
    # Get all modules
    modules = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, '__manifest__.py'))]
    
    print(f"📊 Found {len(modules)} modules to verify")
    print("")
    
    issues_found = []
    modules_with_issues = 0
    
    # Sample verification - check first 20 modules for detailed analysis
    sample_modules = modules[:20]
    
    print(f"🔍 Detailed verification of first {len(sample_modules)} modules:")
    print("-" * 50)
    
    for module in sample_modules:
        result = verify_module(module)
        
        has_issues = False
        
        # Check manifest issues
        if result["manifest_check"].get("issues"):
            has_issues = True
            print(f"❌ {module}: Manifest issues - {result['manifest_check']['issues']}")
        
        # Check Python issues
        if result["python_issues"]:
            has_issues = True
            print(f"⚠️ {module}: Python issues - {result['python_issues']}")
        
        # Check XML issues
        if result["xml_issues"]:
            has_issues = True
            print(f"⚠️ {module}: XML issues - {result['xml_issues']}")
        
        if has_issues:
            modules_with_issues += 1
            issues_found.append(result)
        else:
            print(f"✅ {module}: No issues found")
    
    print("")
    print("=" * 50)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"📊 Modules checked: {len(sample_modules)}")
    print(f"✅ Modules without issues: {len(sample_modules) - modules_with_issues}")
    print(f"⚠️ Modules with issues: {modules_with_issues}")
    print(f"📈 Clean module rate: {((len(sample_modules) - modules_with_issues) / len(sample_modules) * 100):.1f}%")
    
    # Save detailed results
    with open('module_verification_results.json', 'w') as f:
        json.dump({
            "total_modules": len(modules),
            "verified_modules": len(sample_modules),
            "modules_with_issues": modules_with_issues,
            "clean_modules": len(sample_modules) - modules_with_issues,
            "detailed_results": issues_found
        }, f, indent=2)
    
    print(f"📄 Detailed results saved to module_verification_results.json")

if __name__ == "__main__":
    main()
