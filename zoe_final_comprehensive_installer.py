#!/usr/bin/env python3
"""
ZOE'S FINAL COMPREHENSIVE MODULE INSTALLER
100x Engineer approach to install ALL remaining modules to 100% completion
"""
import subprocess
import json
import time
import os
import re
from pathlib import Path

# Updated list of remaining failed modules (excluding auto_logout_idle_user_odoo which is now fixed)
REMAINING_FAILED_MODULES = [
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

def add_missing_action_methods_to_dashboard(module_name):
    """Add missing action methods to dashboard models"""
    print(f"  🔧 Adding missing action methods to {module_name}")
    
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
            
            # Add missing action_view_records method if referenced in views but not defined
            if 'action_view_records' not in content:
                # Check if there are views that reference this method
                views_path = module_path / 'views'
                if views_path.exists():
                    for view_file in views_path.glob('*dashboard*.xml'):
                        try:
                            with open(view_file, 'r', encoding='utf-8') as vf:
                                view_content = vf.read()
                            if 'action_view_records' in view_content:
                                # Add the missing method
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
                                break
                        except Exception:
                            continue
            
            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        except Exception as e:
            print(f"    ❌ Error fixing {py_file}: {e}")
    
    return fixed

def fix_missing_dependencies_comprehensive(module_name):
    """Comprehensive dependency fixing"""
    print(f"  🔧 Comprehensive dependency check for {module_name}")
    
    module_path = Path(module_name)
    manifest_file = module_path / '__manifest__.py'
    
    if not manifest_file.exists():
        return False
    
    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Common missing dependencies based on module patterns
        dependency_map = {
            'payroll': ['hr_payroll', 'hr_contract'],
            'survey': ['survey'],
            'lunch': ['lunch'],
            'event': ['event'],
            'hotel': ['event', 'point_of_sale'],
            'salon': ['point_of_sale'],
            'franchise': ['website_sale'],
            'batch_delivery': ['delivery', 'sale_stock'],
            'education': ['account'],
            'insurance': ['hr_contract'],
            'audit': ['base'],
            'theme': ['website'],
        }
        
        missing_deps = []
        
        for keyword, deps in dependency_map.items():
            if keyword in module_name.lower():
                for dep in deps:
                    if f"'{dep}'" not in content:
                        missing_deps.append(dep)
        
        if missing_deps:
            # Add missing dependencies
            deps_pattern = r"'depends'\s*:\s*\[(.*?)\]"
            match = re.search(deps_pattern, content, re.DOTALL)
            if match:
                current_deps = match.group(1).strip()
                for dep in missing_deps:
                    if f"'{dep}'" not in current_deps:
                        if current_deps and not current_deps.endswith(','):
                            current_deps += f", '{dep}'"
                        else:
                            current_deps += f"'{dep}'"
                
                new_deps = f"'depends': [{current_deps}]"
                content = re.sub(deps_pattern, new_deps, content, flags=re.DOTALL)
                
                print(f"    ✅ Added missing dependencies: {missing_deps}")
        
        if content != original_content:
            with open(manifest_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    
    except Exception as e:
        print(f"    ❌ Error fixing dependencies: {e}")
    
    return False

def install_module_with_comprehensive_fixes(module_name):
    """Install a module with comprehensive fixes"""
    print(f"\n{'='*70}")
    print(f"🔧 COMPREHENSIVE FIXING: {module_name}")
    print(f"{'='*70}")
    
    # Apply comprehensive fixes
    fixes_applied = 0
    
    if add_missing_action_methods_to_dashboard(module_name):
        fixes_applied += 1
    
    if fix_missing_dependencies_comprehensive(module_name):
        fixes_applied += 1
    
    print(f"  📊 Applied {fixes_applied} comprehensive fixes")
    
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
    print("🚀 ZOE'S FINAL COMPREHENSIVE MODULE INSTALLER")
    print("=" * 80)
    print("🎯 100x ENGINEER APPROACH TO 100% COMPLETION")
    print("=" * 80)
    print(f"📊 Installing {len(REMAINING_FAILED_MODULES)} remaining modules")
    print()
    
    successful_installs = []
    still_failed = []
    
    for i, module in enumerate(REMAINING_FAILED_MODULES, 1):
        print(f"[{i:2d}/{len(REMAINING_FAILED_MODULES)}] Processing {module}")
        
        success, error = install_module_with_comprehensive_fixes(module)
        
        if success:
            successful_installs.append(module)
        else:
            still_failed.append((module, error))
        
        time.sleep(2)  # Brief pause between modules
    
    # Final comprehensive summary
    print("\n" + "=" * 80)
    print("📋 ZOE'S FINAL COMPREHENSIVE RESULTS")
    print("=" * 80)
    
    total_modules = len(REMAINING_FAILED_MODULES)
    success_count = len(successful_installs)
    failed_count = len(still_failed)
    
    print(f"📊 Total modules processed: {total_modules}")
    print(f"✅ Successfully installed: {success_count} ({success_count/total_modules*100:.1f}%)")
    print(f"❌ Still failed: {failed_count} ({failed_count/total_modules*100:.1f}%)")
    print()
    
    if successful_installs:
        print("✅ NEWLY INSTALLED MODULES:")
        for module in successful_installs:
            print(f"  • {module}")
        print()
    
    if still_failed:
        print("❌ MODULES REQUIRING DEEPER ANALYSIS:")
        for module, error in still_failed:
            print(f"  • {module}: {error}")
        print()
    
    # Save comprehensive results
    results = {
        "comprehensive_fixes_applied": True,
        "total_processed": total_modules,
        "newly_successful": successful_installs,
        "still_failed": [{"module": m, "error": e} for m, e in still_failed],
        "success_rate": success_count/total_modules*100 if total_modules > 0 else 0
    }
    
    with open('zoe_final_comprehensive_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("📄 Results saved to zoe_final_comprehensive_results.json")
    print()
    
    # Calculate overall project statistics
    print("🎯 OVERALL PROJECT STATUS:")
    
    total_project_modules = 491  # Total modules in project
    previously_installed = 441   # Previously successfully installed (including attendance_regularization and auto_logout_idle_user_odoo)
    newly_installed = success_count
    total_installed = previously_installed + newly_installed
    
    print(f"  📊 Total project modules: {total_project_modules}")
    print(f"  ✅ Total successfully installed: {total_installed}")
    print(f"  📈 Overall project success rate: {total_installed/total_project_modules*100:.1f}%")
    
    if total_installed/total_project_modules >= 0.98:
        print(f"  🏆 PERFECT: 98%+ modules successfully installed!")
    elif total_installed/total_project_modules >= 0.95:
        print(f"  🏆 EXCELLENT: 95%+ modules successfully installed!")
    elif total_installed/total_project_modules >= 0.90:
        print(f"  👍 VERY GOOD: 90%+ modules successfully installed!")
    else:
        print(f"  ⚠️ CONTINUING: More work needed")
    
    print()
    print("🎉 ZOE'S FINAL COMPREHENSIVE MODULE INSTALLATION COMPLETE!")
    
    if success_count == total_modules:
        print("🏆 PERFECT 100x ENGINEER ACHIEVEMENT: ALL MODULES INSTALLED!")

if __name__ == "__main__":
    main()
