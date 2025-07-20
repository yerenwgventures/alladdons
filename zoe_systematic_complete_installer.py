#!/usr/bin/env python3
"""
ZOE 100x ENGINEER - SYSTEMATIC COMPLETE MODULE INSTALLER
Systematic approach to install ALL modules to 100% completion
"""
import subprocess
import json
import time
import os
import re
from pathlib import Path

def get_installed_modules():
    """Get list of currently installed modules"""
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_instance', 
            'bash', '-c', 'PGPASSWORD=odoo psql -h odoo_test_db -U odoo -d cbms_test_db -t -c "SELECT name FROM ir_module_module WHERE state=\'installed\' ORDER BY name;"'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            installed = []
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line and not line.startswith('-') and line != 'name' and not line.startswith('perl:'):
                    installed.append(line)
            return installed
        return []
    except:
        return []

def get_all_modules():
    """Get all modules in the workspace"""
    modules = []
    for item in Path('.').iterdir():
        if item.is_dir() and (item / '__manifest__.py').exists():
            modules.append(item.name)
    return sorted(modules)

def install_single_module_with_error_analysis(module_name):
    """Install a single module with detailed error analysis and fixes"""
    print(f"\n{'='*80}")
    print(f"🔧 ZOE 100x ENGINEER - INSTALLING: {module_name}")
    print(f"{'='*80}")
    
    # Try to install with detailed error logging
    print(f"  📦 Installing {module_name}...")
    
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_instance', 
            'odoo', '-d', 'cbms_test_db', '--db_host=odoo_test_db', 
            '--db_user=odoo', '--db_password=odoo', 
            '-i', module_name, '--stop-after-init', '--log-level=error'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"  ✅ {module_name} - SUCCESS")
            return True, "SUCCESS"
        else:
            print(f"  ❌ {module_name} - FAILED")
            
            # Analyze the error in detail
            error_output = result.stderr
            
            # Extract key error information
            key_errors = []
            error_lines = error_output.split('\n')
            
            for i, line in enumerate(error_lines):
                if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed', 'traceback']):
                    # Get context around the error
                    context_start = max(0, i-2)
                    context_end = min(len(error_lines), i+3)
                    context = error_lines[context_start:context_end]
                    key_errors.extend(context)
            
            # Print detailed error analysis
            if key_errors:
                print(f"  📋 DETAILED ERROR ANALYSIS:")
                for error in key_errors[-10:]:  # Show last 10 relevant lines
                    if error.strip():
                        print(f"    • {error.strip()[:150]}")
            
            # Return the most relevant error
            relevant_error = "Unknown error"
            for line in error_lines:
                if any(keyword in line.lower() for keyword in ['error:', 'exception:', 'failed']):
                    relevant_error = line.strip()[:200]
                    break
            
            return False, relevant_error
            
    except subprocess.TimeoutExpired:
        print(f"  ⏰ {module_name} - TIMEOUT")
        return False, "TIMEOUT"
    except Exception as e:
        print(f"  💥 {module_name} - ERROR: {str(e)}")
        return False, str(e)

def main():
    print("🚀 ZOE 100x ENGINEER - SYSTEMATIC COMPLETE MODULE INSTALLER")
    print("=" * 80)
    print("🎯 SYSTEMATIC APPROACH TO 100% MODULE COMPLETION")
    print("=" * 80)
    
    # Get current status
    all_modules = get_all_modules()
    installed_modules = get_installed_modules()
    
    # Filter out stub modules and already installed modules
    modules_to_install = [m for m in all_modules if not m.startswith('stub_') and m not in installed_modules]
    
    print(f"📊 Total modules found: {len(all_modules)}")
    print(f"📊 Currently installed: {len(installed_modules)}")
    print(f"📊 Modules to install: {len(modules_to_install)}")
    print()
    
    # Show some currently installed modules for verification
    if installed_modules:
        print("✅ SAMPLE OF CURRENTLY INSTALLED MODULES:")
        for module in installed_modules[:10]:
            print(f"  • {module}")
        if len(installed_modules) > 10:
            print(f"  ... and {len(installed_modules) - 10} more")
        print()
    
    successful_installs = []
    failed_modules = []
    
    # Install modules one by one with detailed analysis
    for i, module in enumerate(modules_to_install, 1):
        print(f"[{i:3d}/{len(modules_to_install)}] Processing {module}")
        
        success, error = install_single_module_with_error_analysis(module)
        
        if success:
            successful_installs.append(module)
            print(f"  🎉 TOTAL SUCCESSFUL SO FAR: {len(successful_installs)}")
        else:
            failed_modules.append((module, error))
            print(f"  ⚠️ TOTAL FAILED SO FAR: {len(failed_modules)}")
        
        # Brief pause between modules
        time.sleep(2)
        
        # Progress checkpoint every 50 modules
        if i % 50 == 0:
            print(f"\n📊 CHECKPOINT - Progress: {i}/{len(modules_to_install)}")
            print(f"✅ Successful: {len(successful_installs)}")
            print(f"❌ Failed: {len(failed_modules)}")
            print(f"📈 Success Rate: {len(successful_installs)/i*100:.1f}%")
            print()
    
    # Final comprehensive summary
    print("\n" + "=" * 80)
    print("📋 ZOE 100x ENGINEER - SYSTEMATIC INSTALLATION COMPLETE")
    print("=" * 80)
    
    total_processed = len(modules_to_install)
    success_count = len(successful_installs)
    failed_count = len(failed_modules)
    
    print(f"📊 Total modules processed: {total_processed}")
    print(f"✅ Successfully installed: {success_count}")
    print(f"❌ Failed modules: {failed_count}")
    
    if total_processed > 0:
        session_success_rate = (success_count / total_processed) * 100
        print(f"📈 Session success rate: {session_success_rate:.1f}%")
    
    # Calculate overall project statistics
    final_installed = len(installed_modules) + success_count
    total_project_modules = len(all_modules) - len([m for m in all_modules if m.startswith('stub_')])
    overall_success_rate = (final_installed / total_project_modules) * 100
    
    print(f"\n🎯 OVERALL PROJECT STATUS:")
    print(f"  📊 Total project modules: {total_project_modules}")
    print(f"  ✅ Total successfully installed: {final_installed}")
    print(f"  📈 Overall project success rate: {overall_success_rate:.1f}%")
    
    if successful_installs:
        print(f"\n✅ NEWLY INSTALLED MODULES ({len(successful_installs)}):")
        for module in successful_installs:
            print(f"  • {module}")
    
    if failed_modules:
        print(f"\n❌ MODULES REQUIRING FURTHER ANALYSIS ({len(failed_modules)}):")
        for module, error in failed_modules[:20]:  # Show first 20 failed modules
            print(f"  • {module}: {error[:100]}...")
        if len(failed_modules) > 20:
            print(f"  ... and {len(failed_modules) - 20} more failed modules")
    
    # Save comprehensive results
    results = {
        "session_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_processed": total_processed,
        "newly_successful": successful_installs,
        "failed_modules": [{"module": m, "error": e} for m, e in failed_modules],
        "session_success_rate": (success_count / total_processed * 100) if total_processed > 0 else 0,
        "overall_project_success_rate": overall_success_rate,
        "total_project_modules": total_project_modules,
        "total_installed": final_installed,
        "previously_installed": len(installed_modules)
    }
    
    with open('zoe_systematic_installation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to zoe_systematic_installation_results.json")
    
    if overall_success_rate >= 100:
        print("\n🏆 PERFECT 100x ENGINEER ACHIEVEMENT: 100% MODULES INSTALLED!")
    elif overall_success_rate >= 95:
        print("\n🏆 EXCELLENT 100x ENGINEER ACHIEVEMENT: 95%+ MODULES INSTALLED!")
    elif overall_success_rate >= 90:
        print("\n👍 VERY GOOD: 90%+ MODULES INSTALLED!")
    else:
        print(f"\n⚠️ CONTINUING: {overall_success_rate:.1f}% completion achieved")
    
    print("\n🎉 ZOE 100x ENGINEER SYSTEMATIC INSTALLATION SESSION COMPLETE!")
    
    return failed_modules, overall_success_rate

if __name__ == "__main__":
    failed, success_rate = main()
    
    print(f"\n📊 FINAL STATUS: {success_rate:.1f}% completion achieved")
    
    if success_rate < 100 and failed:
        print(f"🔄 ZOE 100x ENGINEER - {len(failed)} modules require deeper analysis")
        print("💡 Next steps: Analyze failed modules and apply targeted fixes")
