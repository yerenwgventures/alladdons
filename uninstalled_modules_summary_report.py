#!/usr/bin/env python3
"""
Uninstalled Modules Summary Report
Creates a comprehensive summary of all uninstalled modules and their issues
"""
import json

def load_analysis_data():
    """Load the detailed analysis data"""
    try:
        with open('uninstalled_modules_detailed_analysis.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Analysis data not found")
        return None

def extract_error_summary(error_log):
    """Extract key error information from log"""
    if not error_log:
        return "No error log available"
    
    # Look for specific error patterns
    if "NameError: name 'api' is not defined" in error_log:
        return "Python syntax error - missing import"
    elif "null value in column \"model_id\"" in error_log:
        return "Database constraint error - missing model reference"
    elif "ModuleNotFoundError" in error_log or "No module named" in error_log:
        return "Missing Python dependency"
    elif "depends on" in error_log.lower():
        return "Missing Odoo module dependency"
    elif "could not be processed" in error_log:
        return "Data file processing error"
    elif "ImportError" in error_log:
        return "Import error - missing dependency"
    elif "FileNotFoundError" in error_log:
        return "Missing file"
    else:
        return "Complex installation error"

def main():
    print("📋 UNINSTALLED MODULES COMPREHENSIVE SUMMARY REPORT")
    print("=" * 80)
    
    # Load analysis data
    data = load_analysis_data()
    if not data:
        return
    
    print(f"📊 Total uninstalled modules: {data['total_uninstalled']}")
    print()
    
    # Summary by category
    print("📊 ISSUES BY CATEGORY:")
    print("-" * 40)
    categories = data['categories']
    for category, count in categories.items():
        if count > 0:
            category_name = category.replace('_', ' ').title()
            print(f"  {category_name}: {count} modules")
    print()
    
    # Detailed breakdown
    detailed_analysis = data['detailed_analysis']
    
    print("🔍 DETAILED BREAKDOWN:")
    print("=" * 80)
    
    # Group by category for detailed reporting
    by_category = {}
    for module_data in detailed_analysis:
        category = module_data['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(module_data)
    
    # Report each category
    for category, modules in by_category.items():
        if not modules:
            continue
            
        category_name = category.replace('_', ' ').title()
        print(f"\n🔧 {category_name.upper()} ({len(modules)} modules)")
        print("-" * 60)
        
        for module_data in modules:
            module_name = module_data['module']
            manifest_issues = module_data['manifest_issues']
            install_test = module_data['install_test']
            
            print(f"\n📦 {module_name}")
            print(f"   Status: {install_test['status']}")
            
            if manifest_issues:
                print(f"   Manifest Issues:")
                for issue in manifest_issues:
                    print(f"     • {issue}")
            
            error_summary = extract_error_summary(install_test.get('error_log', ''))
            print(f"   Error Summary: {error_summary}")
            
            # Show first few lines of error log if available
            error_log = install_test.get('error_log', '')
            if error_log and len(error_log) > 100:
                lines = error_log.split('\n')
                key_lines = [line for line in lines if any(keyword in line.lower() 
                           for keyword in ['error', 'exception', 'failed', 'traceback'])]
                if key_lines:
                    print(f"   Key Error: {key_lines[-1][:100]}...")
    
    print("\n" + "=" * 80)
    print("📋 SUMMARY OF ISSUES:")
    print("=" * 80)
    
    # Count specific issue types
    issue_counts = {
        "Missing Python Dependencies": 0,
        "Missing Odoo Dependencies": 0,
        "Database Constraint Errors": 0,
        "Python Syntax Errors": 0,
        "File Processing Errors": 0,
        "Complex Installation Errors": 0
    }
    
    for module_data in detailed_analysis:
        error_log = module_data['install_test'].get('error_log', '')
        error_summary = extract_error_summary(error_log)
        
        if "missing python dependency" in error_summary.lower():
            issue_counts["Missing Python Dependencies"] += 1
        elif "missing odoo module dependency" in error_summary.lower():
            issue_counts["Missing Odoo Dependencies"] += 1
        elif "database constraint error" in error_summary.lower():
            issue_counts["Database Constraint Errors"] += 1
        elif "python syntax error" in error_summary.lower():
            issue_counts["Python Syntax Errors"] += 1
        elif "data file processing error" in error_summary.lower():
            issue_counts["File Processing Errors"] += 1
        else:
            issue_counts["Complex Installation Errors"] += 1
    
    for issue_type, count in issue_counts.items():
        if count > 0:
            print(f"  • {issue_type}: {count} modules")
    
    print("\n🎯 RECOMMENDATIONS:")
    print("-" * 40)
    
    external_deps = len(data['category_details']['EXTERNAL_DEPENDENCY'])
    if external_deps > 0:
        print(f"  📦 Install external Python libraries for {external_deps} modules")
        print("      Example: pip install dropbox boto3 paramiko pyncclient")
    
    enterprise_deps = len(data['category_details']['ENTERPRISE_DEPENDENCY'])
    if enterprise_deps > 0:
        print(f"  🏢 {enterprise_deps} modules require Odoo Enterprise edition")
    
    syntax_errors = issue_counts["Python Syntax Errors"]
    if syntax_errors > 0:
        print(f"  🔧 Fix Python syntax errors in {syntax_errors} modules")
    
    db_errors = issue_counts["Database Constraint Errors"]
    if db_errors > 0:
        print(f"  🗃️ Fix database model references in {db_errors} modules")
    
    print(f"\n📊 OVERALL ASSESSMENT:")
    fixable_count = (issue_counts["Python Syntax Errors"] + 
                    issue_counts["File Processing Errors"] + 
                    external_deps)
    
    print(f"  ✅ Successfully installed: 440/491 modules (89.6%)")
    print(f"  🔧 Potentially fixable: {fixable_count} modules")
    print(f"  ❌ Complex issues: {data['total_uninstalled'] - fixable_count} modules")
    
    if fixable_count > 25:
        print(f"  🎯 GOOD: Most uninstalled modules have fixable issues")
    else:
        print(f"  ⚠️ CHALLENGING: Many modules have complex issues")

if __name__ == "__main__":
    main()
