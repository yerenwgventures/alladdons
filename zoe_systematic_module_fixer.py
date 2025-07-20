#!/usr/bin/env python3
"""
ZOE'S SYSTEMATIC MODULE FIXER
100x Engineer approach to fix ALL remaining modules to 100% completion
"""
import subprocess
import json
import time
import os
import re
from pathlib import Path

# List of remaining failed modules to fix
FAILED_MODULES = [
    'auto_logout_idle_user_odoo',
    'automatic_payroll', 
    'batch_delivery_tracking',
    'bill_digitization',
    'cleaning_management',
    'detect_unauthorized_login',
    'education_fee',
    'employee_bonus_manager',
    'employee_ideas',
    'employee_late_check_in',
    'event_management',
    'franchise_management',
    'hide_all_print_button',
    'hotel_management_odoo',
    'hr_hourly_payslip',
    'hr_insurance',
    'laundry_management',
    'low_stocks_product_alert',
    'lunch_order_pdf',
    'mobile_service_shop',
    'pantry_payroll',
    'print_subscription_id_card',
    'product_multi_document',
    'project_task_risk_management_odoo',
    'salon_management',
    'survey_upload_file',
    'theme_blast',
    'theme_shopping',
    'user_audit',
    'website_sign_sending_by_priority'
]

def get_detailed_error_log(module_name):
    """Get detailed error log for a specific module"""
    print(f"🔍 ANALYZING MODULE: {module_name}")
    
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_instance', 
            'odoo', '-d', 'cbms_test_db', '--db_host=odoo_test_db', 
            '--db_user=odoo', '--db_password=odoo', 
            '-i', module_name, '--stop-after-init', '--log-level=debug'
        ], capture_output=True, text=True, timeout=300)
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -2, "", str(e)

def fix_dashboard_model_issues(module_name):
    """Fix dashboard model issues (missing tables, _auto=False, etc.)"""
    print(f"  🔧 Fixing dashboard model issues for {module_name}")
    
    # Find dashboard model files
    module_path = Path(module_name)
    if not module_path.exists():
        return False
    
    models_path = module_path / 'models'
    if not models_path.exists():
        return False
    
    fixed = False
    
    # Look for dashboard models
    for py_file in models_path.glob('*dashboard*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix _auto = False issues
            if '_auto = False' in content:
                content = content.replace('_auto = False', '# _auto = False  # Fixed: Create table')
                print(f"    ✅ Fixed _auto=False in {py_file}")
                fixed = True
            
            # Add missing action methods
            if 'def action_view_records(self):' not in content and 'action_view_records' in content:
                # Find the class definition
                class_match = re.search(r'class\s+(\w+)\(models\.Model\):', content)
                if class_match:
                    # Add the missing method before the last line of the class
                    method_code = '''
    def action_view_records(self):
        """Action to view all records"""
        return {
            'name': 'Records',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'list,form',
            'target': 'current',
        }
'''
                    # Insert before the last method or at the end of class
                    content = content.rstrip() + method_code
                    print(f"    ✅ Added missing action_view_records method in {py_file}")
                    fixed = True
            
            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        except Exception as e:
            print(f"    ❌ Error fixing {py_file}: {e}")
    
    return fixed

def fix_analytics_model_issues(module_name):
    """Fix analytics model issues"""
    print(f"  🔧 Fixing analytics model issues for {module_name}")
    
    module_path = Path(module_name)
    if not module_path.exists():
        return False
    
    models_path = module_path / 'models'
    if not models_path.exists():
        return False
    
    fixed = False
    
    # Look for analytics models
    for py_file in models_path.glob('*analytics*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix _auto = False issues
            if '_auto = False' in content:
                content = content.replace('_auto = False', '# _auto = False  # Fixed: Create table')
                print(f"    ✅ Fixed _auto=False in {py_file}")
                fixed = True
            
            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        except Exception as e:
            print(f"    ❌ Error fixing {py_file}: {e}")
    
    return fixed

def fix_deprecated_field_parameters(module_name):
    """Fix deprecated field parameters like track_visibility"""
    print(f"  🔧 Fixing deprecated field parameters for {module_name}")
    
    module_path = Path(module_name)
    if not module_path.exists():
        return False
    
    models_path = module_path / 'models'
    if not models_path.exists():
        return False
    
    fixed = False
    
    for py_file in models_path.glob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix track_visibility parameter
            content = re.sub(r"track_visibility='onchange'", "tracking=True", content)
            content = re.sub(r'track_visibility="onchange"', "tracking=True", content)
            
            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"    ✅ Fixed deprecated parameters in {py_file}")
                fixed = True
        
        except Exception as e:
            print(f"    ❌ Error fixing {py_file}: {e}")
    
    return fixed

def fix_missing_dependencies(module_name):
    """Fix missing dependencies in manifest"""
    print(f"  🔧 Checking dependencies for {module_name}")
    
    module_path = Path(module_name)
    manifest_file = module_path / '__manifest__.py'
    
    if not manifest_file.exists():
        return False
    
    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Common missing dependencies based on error patterns
        missing_deps = []
        
        if 'survey' in content.lower() and "'survey'" not in content:
            missing_deps.append('survey')
        if 'hr_contract' in content.lower() and "'hr_contract'" not in content:
            missing_deps.append('hr_contract')
        if 'hr_payroll' in content.lower() and "'hr_payroll'" not in content:
            missing_deps.append('hr_payroll')
        
        if missing_deps:
            # Add missing dependencies
            deps_pattern = r"'depends'\s*:\s*\[(.*?)\]"
            match = re.search(deps_pattern, content, re.DOTALL)
            if match:
                current_deps = match.group(1)
                for dep in missing_deps:
                    if f"'{dep}'" not in current_deps:
                        current_deps += f", '{dep}'"
                
                new_deps = f"'depends': [{current_deps}]"
                content = re.sub(deps_pattern, new_deps, content, flags=re.DOTALL)
                
                with open(manifest_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"    ✅ Added missing dependencies: {missing_deps}")
                return True
    
    except Exception as e:
        print(f"    ❌ Error fixing dependencies: {e}")
    
    return False

def install_module_with_fixes(module_name):
    """Install a module with systematic fixes"""
    print(f"\n{'='*60}")
    print(f"🔧 FIXING MODULE: {module_name}")
    print(f"{'='*60}")
    
    # Apply fixes
    fixes_applied = 0
    
    if fix_dashboard_model_issues(module_name):
        fixes_applied += 1
    
    if fix_analytics_model_issues(module_name):
        fixes_applied += 1
    
    if fix_deprecated_field_parameters(module_name):
        fixes_applied += 1
    
    if fix_missing_dependencies(module_name):
        fixes_applied += 1
    
    print(f"  📊 Applied {fixes_applied} fixes")
    
    # Try to install
    print(f"  📦 Installing {module_name}...")
    
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_instance', 
            'odoo', '-d', 'cbms_test_db', '--db_host=odoo_test_db', 
            '--db_user=odoo', '--db_password=odoo', 
            '-i', module_name, '--stop-after-init'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"  ✅ {module_name} - SUCCESS")
            return True, "SUCCESS"
        else:
            print(f"  ❌ {module_name} - FAILED")
            # Get detailed error for further analysis
            error_lines = result.stderr.split('\n')
            key_error = "Unknown error"
            
            for line in error_lines:
                if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed', 'traceback']):
                    key_error = line.strip()[:200]
                    break
            
            print(f"  📋 Error: {key_error}")
            return False, key_error
            
    except subprocess.TimeoutExpired:
        print(f"  ⏰ {module_name} - TIMEOUT")
        return False, "TIMEOUT"
    except Exception as e:
        print(f"  💥 {module_name} - ERROR: {str(e)}")
        return False, str(e)

def main():
    print("🚀 ZOE'S SYSTEMATIC MODULE FIXER - 100x ENGINEER APPROACH")
    print("=" * 80)
    print(f"📊 Fixing {len(FAILED_MODULES)} remaining modules")
    print()
    
    successful_fixes = []
    still_failed = []
    
    for i, module in enumerate(FAILED_MODULES, 1):
        print(f"[{i:2d}/{len(FAILED_MODULES)}] Processing {module}")
        
        success, error = install_module_with_fixes(module)
        
        if success:
            successful_fixes.append(module)
        else:
            still_failed.append((module, error))
        
        time.sleep(2)  # Brief pause between modules
    
    # Final summary
    print("\n" + "=" * 80)
    print("📋 ZOE'S SYSTEMATIC FIXING RESULTS")
    print("=" * 80)
    
    total_modules = len(FAILED_MODULES)
    success_count = len(successful_fixes)
    failed_count = len(still_failed)
    
    print(f"📊 Total modules processed: {total_modules}")
    print(f"✅ Successfully fixed and installed: {success_count} ({success_count/total_modules*100:.1f}%)")
    print(f"❌ Still failed: {failed_count} ({failed_count/total_modules*100:.1f}%)")
    print()
    
    if successful_fixes:
        print("✅ NEWLY FIXED MODULES:")
        for module in successful_fixes:
            print(f"  • {module}")
        print()
    
    if still_failed:
        print("❌ STILL FAILED MODULES (need deeper analysis):")
        for module, error in still_failed:
            print(f"  • {module}: {error}")
        print()
    
    # Save results
    results = {
        "systematic_fixes_applied": True,
        "total_processed": total_modules,
        "newly_successful": successful_fixes,
        "still_failed": [{"module": m, "error": e} for m, e in still_failed],
        "success_rate": success_count/total_modules*100 if total_modules > 0 else 0
    }
    
    with open('zoe_systematic_fixing_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("📄 Results saved to zoe_systematic_fixing_results.json")
    print()
    print("🎯 ZOE'S 100x ENGINEER STATUS:")
    
    if success_count == total_modules:
        print("  🏆 PERFECT: 100% modules fixed!")
    elif success_count >= total_modules * 0.8:
        print("  👍 EXCELLENT: 80%+ modules fixed!")
    else:
        print("  ⚠️ CONTINUING: More deep fixes needed")
    
    print("\n🎉 ZOE'S SYSTEMATIC MODULE FIXING COMPLETE!")

if __name__ == "__main__":
    main()
