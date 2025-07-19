#!/usr/bin/env python3
"""
Comprehensive Content Verification Script
Checks for placeholders, incomplete features, commented code, and missing files
"""
import os
import ast
import re
import json
import subprocess
from pathlib import Path

def get_installed_custom_modules():
    """Get custom modules that are actually installed in database"""
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_db', 'psql', '-U', 'odoo', '-d', 'cbms_test_db', 
            '-t', '-c', "SELECT name FROM ir_module_module WHERE state = 'installed' ORDER BY name;"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            all_modules = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            # Filter to only our custom modules (ones that exist in current directory)
            custom_modules = []
            for module in all_modules:
                if os.path.isdir(module) and os.path.exists(os.path.join(module, '__manifest__.py')):
                    custom_modules.append(module)
            return custom_modules
        return []
    except Exception as e:
        print(f"Error getting installed modules: {e}")
        return []

def check_for_placeholders_and_todos(file_path):
    """Check file for placeholders, TODOs, and incomplete content"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Check for common placeholders and incomplete markers
        placeholder_patterns = [
            r'TODO', r'FIXME', r'XXX', r'PLACEHOLDER', r'CHANGEME',
            r'template_name', r'your_.*_here', r'replace_.*_here',
            r'# TODO:', r'# FIXME:', r'# XXX:', r'# PLACEHOLDER:',
            r'pass\s*#.*TODO', r'pass\s*#.*FIXME'
        ]
        
        for i, line in enumerate(lines, 1):
            line_upper = line.upper()
            for pattern in placeholder_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(f"Line {i}: {pattern} found - {line.strip()[:100]}")
        
        # Check for commented out features
        commented_features = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#') and any(keyword in stripped.lower() for keyword in 
                ['def ', 'class ', 'field', 'model', 'view', 'record']):
                commented_features.append(f"Line {i}: Commented code - {stripped[:80]}")
        
        if commented_features:
            issues.extend(commented_features[:5])  # Limit to first 5
        
        return issues
    except Exception as e:
        return [f"Error reading file: {str(e)}"]

def verify_manifest_completeness(module_path):
    """Verify manifest file completeness and check for missing declared files"""
    manifest_path = os.path.join(module_path, '__manifest__.py')
    issues = []
    
    if not os.path.exists(manifest_path):
        return ["No __manifest__.py file found"]
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for placeholders in manifest
        placeholder_issues = check_for_placeholders_and_todos(manifest_path)
        issues.extend(placeholder_issues)
        
        # Parse manifest
        tree = ast.parse(content)
        manifest_dict = ast.literal_eval(tree.body[0].value)
        
        # Check for placeholder values in manifest fields
        placeholder_values = ['todo', 'placeholder', 'changeme', 'your_name_here', 'template']
        
        for field in ['name', 'summary', 'description', 'author', 'website']:
            value = manifest_dict.get(field, '').lower()
            if any(placeholder in value for placeholder in placeholder_values):
                issues.append(f"Placeholder in {field}: {manifest_dict.get(field, '')}")
        
        # Check all declared files exist
        missing_files = []
        for file_list_key in ['data', 'demo', 'qweb', 'css', 'js']:
            file_list = manifest_dict.get(file_list_key, [])
            for file_path in file_list:
                full_path = os.path.join(module_path, file_path)
                if not os.path.exists(full_path):
                    missing_files.append(file_path)
        
        if missing_files:
            issues.append(f"Missing declared files: {missing_files}")
        
        return issues, manifest_dict
        
    except Exception as e:
        return [f"Error parsing manifest: {str(e)}"], {}

def check_python_files_completeness(module_path):
    """Check Python files for incomplete implementations"""
    issues = []
    
    for py_file in Path(module_path).rglob('*.py'):
        if py_file.name == '__manifest__.py':
            continue
            
        file_issues = check_for_placeholders_and_todos(py_file)
        if file_issues:
            issues.append(f"{py_file.relative_to(module_path)}: {len(file_issues)} issues")
            issues.extend([f"  - {issue}" for issue in file_issues[:3]])  # Show first 3
        
        # Check for incomplete class/method definitions
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Count pass statements vs actual implementations
            pass_count = len(re.findall(r'\bpass\b', content))
            method_count = len(re.findall(r'def \w+', content))
            
            if pass_count > 0 and pass_count >= method_count * 0.5:
                issues.append(f"{py_file.relative_to(module_path)}: High ratio of 'pass' statements ({pass_count}/{method_count})")
                
        except Exception:
            pass
    
    return issues

def check_xml_files_completeness(module_path):
    """Check XML files for incomplete definitions"""
    issues = []
    
    for xml_file in Path(module_path).rglob('*.xml'):
        file_issues = check_for_placeholders_and_todos(xml_file)
        if file_issues:
            issues.append(f"{xml_file.relative_to(module_path)}: {len(file_issues)} issues")
            issues.extend([f"  - {issue}" for issue in file_issues[:3]])
        
        # Check for incomplete XML structures
        try:
            with open(xml_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for empty or placeholder field values
            empty_fields = re.findall(r'<field[^>]*name="[^"]*"[^>]*>\s*</field>', content)
            if empty_fields:
                issues.append(f"{xml_file.relative_to(module_path)}: {len(empty_fields)} empty field definitions")
            
            # Check for placeholder field names
            placeholder_fields = re.findall(r'field name="(template_|placeholder_|todo_|changeme_)[^"]*"', content)
            if placeholder_fields:
                issues.append(f"{xml_file.relative_to(module_path)}: Placeholder field names: {placeholder_fields}")
                
        except Exception:
            pass
    
    return issues

def comprehensive_module_verification(module_name):
    """Perform comprehensive verification of a single module"""
    module_path = Path(module_name)
    
    if not module_path.exists():
        return {"error": "Module directory not found"}
    
    print(f"🔍 Verifying {module_name}...")
    
    # Verify manifest
    manifest_issues, manifest_dict = verify_manifest_completeness(module_path)
    
    # Check Python files
    python_issues = check_python_files_completeness(module_path)
    
    # Check XML files
    xml_issues = check_xml_files_completeness(module_path)
    
    # Calculate severity
    total_issues = len(manifest_issues) + len(python_issues) + len(xml_issues)
    
    if total_issues == 0:
        status = "CLEAN"
    elif total_issues <= 3:
        status = "MINOR_ISSUES"
    elif total_issues <= 10:
        status = "MODERATE_ISSUES"
    else:
        status = "MAJOR_ISSUES"
    
    return {
        "module": module_name,
        "status": status,
        "total_issues": total_issues,
        "manifest_issues": manifest_issues,
        "python_issues": python_issues,
        "xml_issues": xml_issues,
        "manifest_data": {
            "name": manifest_dict.get('name', ''),
            "version": manifest_dict.get('version', ''),
            "author": manifest_dict.get('author', ''),
            "data_files_count": len(manifest_dict.get('data', []))
        }
    }

def main():
    print("🔍 COMPREHENSIVE CONTENT VERIFICATION")
    print("=" * 60)
    
    # Get installed custom modules
    print("📊 Getting installed custom modules from database...")
    installed_modules = get_installed_custom_modules()
    
    print(f"✅ Found {len(installed_modules)} installed custom modules")
    print("")
    
    # Verify modules
    results = {
        "CLEAN": [],
        "MINOR_ISSUES": [],
        "MODERATE_ISSUES": [],
        "MAJOR_ISSUES": []
    }
    
    detailed_results = []
    
    print("🔍 Performing comprehensive verification...")
    print("-" * 40)
    
    for i, module in enumerate(installed_modules[:50], 1):  # Check first 50 for detailed output
        result = comprehensive_module_verification(module)
        
        if "error" not in result:
            status = result["status"]
            results[status].append(module)
            detailed_results.append(result)
            
            if result["total_issues"] == 0:
                print(f"✅ {module}")
            elif result["total_issues"] <= 3:
                print(f"⚠️ {module} - {result['total_issues']} minor issues")
            else:
                print(f"❌ {module} - {result['total_issues']} issues")
    
    # Quick check remaining modules
    for module in installed_modules[50:]:
        result = comprehensive_module_verification(module)
        if "error" not in result:
            results[result["status"]].append(module)
    
    print("")
    print("=" * 60)
    print("📋 COMPREHENSIVE VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"📊 Total verified modules: {len(installed_modules)}")
    print(f"✅ Clean modules: {len(results['CLEAN'])} ({len(results['CLEAN'])/len(installed_modules)*100:.1f}%)")
    print(f"⚠️ Minor issues: {len(results['MINOR_ISSUES'])} ({len(results['MINOR_ISSUES'])/len(installed_modules)*100:.1f}%)")
    print(f"🔧 Moderate issues: {len(results['MODERATE_ISSUES'])} ({len(results['MODERATE_ISSUES'])/len(installed_modules)*100:.1f}%)")
    print(f"❌ Major issues: {len(results['MAJOR_ISSUES'])} ({len(results['MAJOR_ISSUES'])/len(installed_modules)*100:.1f}%)")
    
    # Save detailed results
    summary = {
        "total_modules": len(installed_modules),
        "verification_summary": {
            "clean": len(results['CLEAN']),
            "minor_issues": len(results['MINOR_ISSUES']),
            "moderate_issues": len(results['MODERATE_ISSUES']),
            "major_issues": len(results['MAJOR_ISSUES'])
        },
        "clean_percentage": len(results['CLEAN'])/len(installed_modules)*100,
        "detailed_results": detailed_results[:20]  # Save first 20 detailed results
    }
    
    with open('comprehensive_verification_results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Detailed results saved to comprehensive_verification_results.json")
    
    # Overall assessment
    clean_rate = len(results['CLEAN'])/len(installed_modules)*100
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if clean_rate >= 80:
        print("🏆 EXCELLENT: 80%+ modules are clean and complete")
    elif clean_rate >= 60:
        print("👍 GOOD: 60%+ modules are clean")
    elif clean_rate >= 40:
        print("⚠️ FAIR: 40%+ modules are clean, some issues found")
    else:
        print("❌ NEEDS ATTENTION: Less than 40% modules are clean")

if __name__ == "__main__":
    main()
