#!/usr/bin/env python3
"""
Complete Issues Analyzer
Re-runs verification on all modules to get complete issue list
"""
import os
import subprocess
import json
import ast
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

def quick_issue_check(module_name):
    """Quick check for issues in a module"""
    module_path = Path(module_name)
    
    if not module_path.exists():
        return {"status": "missing", "issues": 0}
    
    issues = 0
    issue_details = []
    
    # Check manifest
    manifest_path = module_path / '__manifest__.py'
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for placeholders
            placeholders = ['TODO', 'PLACEHOLDER', 'CHANGEME', 'template_name', 'your_name_here']
            for placeholder in placeholders:
                if placeholder.lower() in content.lower():
                    issues += 1
                    issue_details.append(f"Manifest: {placeholder} found")
            
            # Check for missing data files
            try:
                tree = ast.parse(content)
                manifest_dict = ast.literal_eval(tree.body[0].value)
                
                for data_file in manifest_dict.get('data', []):
                    if not (module_path / data_file).exists():
                        issues += 1
                        issue_details.append(f"Missing file: {data_file}")
            except:
                pass
                
        except Exception as e:
            issues += 1
            issue_details.append(f"Manifest error: {str(e)}")
    
    # Check Python files
    for py_file in module_path.rglob('*.py'):
        if py_file.name == '__manifest__.py':
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for placeholders
            if any(placeholder in content.upper() for placeholder in ['TODO', 'FIXME', 'PLACEHOLDER']):
                issues += 1
                issue_details.append(f"{py_file.name}: Contains placeholders")
            
            # Check for high ratio of pass statements
            pass_count = content.count('pass')
            method_count = content.count('def ')
            
            if method_count > 0 and pass_count > method_count * 0.6:
                issues += 1
                issue_details.append(f"{py_file.name}: High pass/method ratio ({pass_count}/{method_count})")
                
        except Exception:
            pass
    
    # Check XML files
    for xml_file in module_path.rglob('*.xml'):
        try:
            with open(xml_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for placeholders
            if any(placeholder in content.upper() for placeholder in ['TODO', 'PLACEHOLDER', 'TEMPLATE_']):
                issues += 1
                issue_details.append(f"{xml_file.name}: Contains placeholders")
            
            # Check for empty fields
            if 'field name=""' in content or "field name=''" in content:
                issues += 1
                issue_details.append(f"{xml_file.name}: Empty field names")
                
        except Exception:
            pass
    
    # Categorize by severity
    if issues == 0:
        status = "CLEAN"
    elif issues <= 2:
        status = "MINOR_ISSUES"
    elif issues <= 5:
        status = "MODERATE_ISSUES"
    else:
        status = "MAJOR_ISSUES"
    
    return {
        "status": status,
        "issues": issues,
        "details": issue_details[:5]  # Limit to first 5 details
    }

def main():
    print("🔍 COMPLETE ISSUES ANALYZER")
    print("=" * 50)
    
    # Get all installed custom modules
    print("📊 Getting installed custom modules...")
    installed_modules = get_installed_custom_modules()
    
    print(f"✅ Found {len(installed_modules)} installed custom modules")
    print()
    
    # Analyze all modules
    results = {
        "CLEAN": [],
        "MINOR_ISSUES": [],
        "MODERATE_ISSUES": [],
        "MAJOR_ISSUES": []
    }
    
    detailed_issues = []
    
    print("🔍 Analyzing all modules for issues...")
    print("-" * 40)
    
    for i, module in enumerate(installed_modules, 1):
        if i <= 50:  # Show progress for first 50
            print(f"[{i:3d}/{len(installed_modules)}] {module}", end="")
        
        result = quick_issue_check(module)
        
        if result["status"] != "missing":
            status = result["status"]
            results[status].append(module)
            
            if result["issues"] > 0:
                detailed_issues.append({
                    "module": module,
                    "status": status,
                    "issue_count": result["issues"],
                    "details": result["details"]
                })
            
            if i <= 50:
                if result["issues"] == 0:
                    print(" ✅")
                elif result["issues"] <= 2:
                    print(f" ⚠️ ({result['issues']} issues)")
                else:
                    print(f" ❌ ({result['issues']} issues)")
        else:
            if i <= 50:
                print(" 💥 (missing)")
    
    if len(installed_modules) > 50:
        print(f"... and {len(installed_modules) - 50} more modules analyzed")
    
    print()
    print("=" * 50)
    print("📋 COMPLETE ANALYSIS RESULTS")
    print("=" * 50)
    
    total = len(installed_modules)
    print(f"📊 Total modules analyzed: {total}")
    print(f"✅ Clean modules: {len(results['CLEAN'])} ({len(results['CLEAN'])/total*100:.1f}%)")
    print(f"⚠️ Minor issues: {len(results['MINOR_ISSUES'])} ({len(results['MINOR_ISSUES'])/total*100:.1f}%)")
    print(f"🔧 Moderate issues: {len(results['MODERATE_ISSUES'])} ({len(results['MODERATE_ISSUES'])/total*100:.1f}%)")
    print(f"❌ Major issues: {len(results['MAJOR_ISSUES'])} ({len(results['MAJOR_ISSUES'])/total*100:.1f}%)")
    print()
    
    # Show modules with major issues
    if results['MAJOR_ISSUES']:
        print("❌ MODULES WITH MAJOR ISSUES:")
        for module in results['MAJOR_ISSUES'][:10]:  # Show first 10
            module_details = next((d for d in detailed_issues if d['module'] == module), None)
            if module_details:
                print(f"  • {module} ({module_details['issue_count']} issues)")
                for detail in module_details['details'][:2]:  # Show first 2 details
                    print(f"    - {detail}")
        if len(results['MAJOR_ISSUES']) > 10:
            print(f"  ... and {len(results['MAJOR_ISSUES']) - 10} more")
        print()
    
    # Show modules with moderate issues
    if results['MODERATE_ISSUES']:
        print("🔧 MODULES WITH MODERATE ISSUES (sample):")
        for module in results['MODERATE_ISSUES'][:5]:  # Show first 5
            module_details = next((d for d in detailed_issues if d['module'] == module), None)
            if module_details:
                print(f"  • {module} ({module_details['issue_count']} issues)")
        if len(results['MODERATE_ISSUES']) > 5:
            print(f"  ... and {len(results['MODERATE_ISSUES']) - 5} more")
        print()
    
    # Save complete results
    complete_results = {
        "total_modules": total,
        "summary": {
            "clean": len(results['CLEAN']),
            "minor_issues": len(results['MINOR_ISSUES']),
            "moderate_issues": len(results['MODERATE_ISSUES']),
            "major_issues": len(results['MAJOR_ISSUES'])
        },
        "modules_by_status": results,
        "detailed_issues": detailed_issues
    }
    
    with open('complete_issues_analysis.json', 'w') as f:
        json.dump(complete_results, f, indent=2)
    
    print("📄 Complete analysis saved to complete_issues_analysis.json")
    
    # Final recommendations
    print()
    print("🎯 DEPLOYMENT RECOMMENDATIONS:")
    clean_rate = len(results['CLEAN']) / total
    
    if clean_rate >= 0.7:
        print("  🏆 EXCELLENT: Deploy clean modules immediately")
    elif clean_rate >= 0.5:
        print("  👍 GOOD: Deploy clean modules, fix minor issues")
    else:
        print("  ⚠️ NEEDS WORK: Address issues before deployment")
    
    print(f"  ✅ {len(results['CLEAN'])} modules ready for immediate deployment")
    print(f"  🔧 {len(results['MINOR_ISSUES']) + len(results['MODERATE_ISSUES'])} modules need fixes")
    print(f"  ❌ {len(results['MAJOR_ISSUES'])} modules need significant work")

if __name__ == "__main__":
    main()
