#!/usr/bin/env python3
"""
Verification of specifically installed modules
Cross-references database installed modules with file system verification
"""
import os
import subprocess
import json
import ast

def get_installed_modules():
    """Get list of installed modules from database"""
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_db', 'psql', '-U', 'odoo', '-d', 'cbms_test_db', 
            '-t', '-c', "SELECT name FROM ir_module_module WHERE state = 'installed' ORDER BY name;"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            modules = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            # Filter out base Odoo modules
            custom_modules = [m for m in modules if m not in [
                'base', 'web', 'mail', 'calendar', 'contacts', 'crm', 'sale', 'purchase', 
                'stock', 'account', 'hr', 'project', 'website', 'point_of_sale', 'mrp',
                'fleet', 'lunch', 'survey', 'im_livechat', 'pos_restaurant', 'mass_mailing',
                'event', 'membership', 'maintenance', 'helpdesk_mgmt', 'rating', 'portal',
                'payment', 'delivery', 'sale_management', 'purchase_stock', 'sale_stock',
                'stock_account', 'hr_attendance', 'hr_holidays', 'hr_expense', 'hr_timesheet',
                'analytic', 'auth_signup', 'auth_oauth', 'barcodes', 'board', 'bus',
                'resource', 'web_tour', 'web_kanban_gauge', 'utm', 'phone_validation'
            ]]
            return custom_modules
        else:
            print(f"Error getting installed modules: {result.stderr}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def quick_verify_module(module_name):
    """Quick verification of a module"""
    module_path = os.path.join('.', module_name)
    
    if not os.path.isdir(module_path):
        return {"status": "missing_directory", "issues": ["Module directory not found"]}
    
    # Check manifest
    manifest_path = os.path.join(module_path, '__manifest__.py')
    if not os.path.exists(manifest_path):
        return {"status": "missing_manifest", "issues": ["No __manifest__.py file"]}
    
    issues = []
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic checks
        if 'TODO' in content.upper() or 'PLACEHOLDER' in content.upper():
            issues.append("Manifest contains placeholders")
        
        # Parse manifest
        tree = ast.parse(content)
        manifest_dict = ast.literal_eval(tree.body[0].value)
        
        # Check data files exist
        data_files = manifest_dict.get('data', [])
        missing_files = []
        for data_file in data_files:
            file_path = os.path.join(module_path, data_file)
            if not os.path.exists(file_path):
                missing_files.append(data_file)
        
        if missing_files:
            issues.append(f"Missing files: {missing_files}")
        
        # Check for basic structure
        has_models = os.path.exists(os.path.join(module_path, 'models'))
        has_views = os.path.exists(os.path.join(module_path, 'views'))
        
        structure_info = {
            "has_models": has_models,
            "has_views": has_views,
            "data_files_count": len(data_files),
            "missing_files_count": len(missing_files)
        }
        
        if issues:
            return {"status": "has_issues", "issues": issues, "structure": structure_info}
        else:
            return {"status": "clean", "issues": [], "structure": structure_info}
            
    except Exception as e:
        return {"status": "parse_error", "issues": [f"Error parsing: {str(e)}"]}

def main():
    print("🔍 INSTALLED MODULES VERIFICATION")
    print("=" * 50)
    
    # Get installed modules from database
    print("📊 Getting installed modules from database...")
    installed_modules = get_installed_modules()
    
    print(f"✅ Found {len(installed_modules)} custom installed modules")
    print("")
    
    # Verify each installed module
    clean_modules = []
    modules_with_issues = []
    missing_modules = []
    parse_errors = []
    
    print("🔍 Verifying installed modules...")
    print("-" * 30)
    
    for i, module in enumerate(installed_modules, 1):
        if i <= 100:  # Check first 100 for detailed output
            result = quick_verify_module(module)
            
            if result["status"] == "clean":
                clean_modules.append(module)
                print(f"✅ {module}")
            elif result["status"] == "has_issues":
                modules_with_issues.append((module, result["issues"]))
                print(f"⚠️ {module}: {', '.join(result['issues'])}")
            elif result["status"] == "missing_directory":
                missing_modules.append(module)
                print(f"❌ {module}: Directory not found")
            elif result["status"] == "missing_manifest":
                missing_modules.append(module)
                print(f"❌ {module}: No manifest file")
            else:
                parse_errors.append((module, result["issues"]))
                print(f"💥 {module}: Parse error")
        else:
            # Quick check for remaining modules
            result = quick_verify_module(module)
            if result["status"] == "clean":
                clean_modules.append(module)
            elif result["status"] == "has_issues":
                modules_with_issues.append((module, result["issues"]))
            else:
                missing_modules.append(module)
    
    print("")
    print("=" * 50)
    print("📋 INSTALLED MODULES VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"📊 Total custom installed modules: {len(installed_modules)}")
    print(f"✅ Clean modules: {len(clean_modules)} ({len(clean_modules)/len(installed_modules)*100:.1f}%)")
    print(f"⚠️ Modules with minor issues: {len(modules_with_issues)} ({len(modules_with_issues)/len(installed_modules)*100:.1f}%)")
    print(f"❌ Missing/broken modules: {len(missing_modules)} ({len(missing_modules)/len(installed_modules)*100:.1f}%)")
    print(f"💥 Parse errors: {len(parse_errors)} ({len(parse_errors)/len(installed_modules)*100:.1f}%)")
    print("")
    
    if modules_with_issues:
        print("⚠️ MODULES WITH ISSUES:")
        for module, issues in modules_with_issues[:10]:  # Show first 10
            print(f"  • {module}: {', '.join(issues)}")
        if len(modules_with_issues) > 10:
            print(f"  ... and {len(modules_with_issues) - 10} more")
        print("")
    
    if missing_modules:
        print("❌ MISSING/BROKEN MODULES:")
        for module in missing_modules[:10]:  # Show first 10
            print(f"  • {module}")
        if len(missing_modules) > 10:
            print(f"  ... and {len(missing_modules) - 10} more")
        print("")
    
    # Save results
    results = {
        "total_installed": len(installed_modules),
        "clean_modules": len(clean_modules),
        "modules_with_issues": len(modules_with_issues),
        "missing_modules": len(missing_modules),
        "parse_errors": len(parse_errors),
        "clean_percentage": len(clean_modules)/len(installed_modules)*100,
        "sample_clean_modules": clean_modules[:20],
        "sample_issues": [(m, i) for m, i in modules_with_issues[:10]],
        "sample_missing": missing_modules[:10]
    }
    
    with open('installed_modules_verification.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Results saved to installed_modules_verification.json")
    
    # Overall assessment
    print("")
    print("🎯 OVERALL ASSESSMENT:")
    if len(clean_modules)/len(installed_modules) > 0.8:
        print("✅ EXCELLENT: Over 80% of installed modules are clean and complete")
    elif len(clean_modules)/len(installed_modules) > 0.6:
        print("👍 GOOD: Over 60% of installed modules are clean")
    else:
        print("⚠️ NEEDS ATTENTION: Less than 60% of modules are clean")

if __name__ == "__main__":
    main()
