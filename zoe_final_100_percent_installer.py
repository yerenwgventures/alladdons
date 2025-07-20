#!/usr/bin/env python3
"""
ZOE 100x ENGINEER - FINAL 100% MODULE INSTALLER
Complete all remaining modules to achieve 100% success rate
"""
import subprocess
import json
import time
import os
from pathlib import Path

def get_all_modules():
    """Get all modules in the workspace"""
    modules = []
    for item in Path('.').iterdir():
        if item.is_dir() and (item / '__manifest__.py').exists():
            modules.append(item.name)
    return sorted(modules)

def get_installed_modules():
    """Get list of currently installed modules"""
    try:
        result = subprocess.run([
            'docker', 'exec', '-e', 'PGPASSWORD=odoo', 'odoo_test_instance', 
            'psql', '-h', 'odoo_test_db', '-U', 'odoo', '-d', 'cbms_test_db',
            '-t', '-c', "SELECT name FROM ir_module_module WHERE state='installed';"
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

def install_single_module(module_name):
    """Install a single module with detailed error analysis"""
    print(f"\n{'='*80}")
    print(f"🔧 ZOE 100x ENGINEER - INSTALLING: {module_name}")
    print(f"{'='*80}")
    
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
            
            # Extract key error information
            error_lines = result.stderr.split('\n')
            key_error = "Unknown error"
            
            for line in error_lines:
                if any(keyword in line.lower() for keyword in ['error:', 'exception:', 'failed']):
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
    print("🚀 ZOE 100x ENGINEER - FINAL 100% MODULE INSTALLER")
    print("=" * 80)
    print("🎯 ACHIEVING 100% MODULE INSTALLATION SUCCESS")
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
        for module in installed_modules[:15]:
            print(f"  • {module}")
        if len(installed_modules) > 15:
            print(f"  ... and {len(installed_modules) - 15} more")
        print()
    
    successful_installs = []
    failed_modules = []
    
    # Install modules one by one
    for i, module in enumerate(modules_to_install, 1):
        print(f"[{i:3d}/{len(modules_to_install)}] Processing {module}")
        
        success, error = install_single_module(module)
        
        if success:
            successful_installs.append(module)
            print(f"  🎉 TOTAL SUCCESSFUL SO FAR: {len(successful_installs)}")
        else:
            failed_modules.append((module, error))
            print(f"  ⚠️ TOTAL FAILED SO FAR: {len(failed_modules)}")
        
        # Brief pause between modules
        time.sleep(1)
        
        # Progress checkpoint every 50 modules
        if i % 50 == 0:
            print(f"\n📊 CHECKPOINT - Progress: {i}/{len(modules_to_install)}")
            print(f"✅ Successful: {len(successful_installs)}")
            print(f"❌ Failed: {len(failed_modules)}")
            print(f"📈 Success Rate: {len(successful_installs)/i*100:.1f}%")
            print()
    
    # Final comprehensive summary
    print("\n" + "=" * 80)
    print("📋 ZOE 100x ENGINEER - FINAL INSTALLATION COMPLETE")
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
    
    with open('zoe_final_100_percent_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to zoe_final_100_percent_results.json")
    
    # Achievement levels
    if overall_success_rate >= 100:
        print("\n🏆 PERFECT 100x ENGINEER ACHIEVEMENT: 100% MODULES INSTALLED!")
    elif overall_success_rate >= 98:
        print("\n🏆 NEAR PERFECT: 98%+ MODULES INSTALLED!")
    elif overall_success_rate >= 95:
        print("\n🏆 EXCELLENT: 95%+ MODULES INSTALLED!")
    elif overall_success_rate >= 90:
        print("\n👍 VERY GOOD: 90%+ MODULES INSTALLED!")
    else:
        print(f"\n⚠️ CONTINUING: {overall_success_rate:.1f}% completion achieved")
    
    print("\n🎉 ZOE 100x ENGINEER FINAL INSTALLATION SESSION COMPLETE!")
    
    # Create completion report
    print("\n📋 CREATING COMPLETION REPORT...")
    
    completion_report = f"""
# ZOE 100x ENGINEER - PROJECT COMPLETION REPORT

## Summary
- **Total Project Modules**: {total_project_modules}
- **Successfully Installed**: {final_installed}
- **Overall Success Rate**: {overall_success_rate:.1f}%
- **Session Date**: {time.strftime("%Y-%m-%d %H:%M:%S")}

## Session Results
- **Modules Processed This Session**: {total_processed}
- **Newly Installed**: {success_count}
- **Session Success Rate**: {(success_count / total_processed * 100) if total_processed > 0 else 0:.1f}%

## Achievement Level
{'🏆 PERFECT: 100% COMPLETION!' if overall_success_rate >= 100 else
 '🏆 NEAR PERFECT: 98%+ COMPLETION!' if overall_success_rate >= 98 else
 '🏆 EXCELLENT: 95%+ COMPLETION!' if overall_success_rate >= 95 else
 '👍 VERY GOOD: 90%+ COMPLETION!' if overall_success_rate >= 90 else
 f'⚠️ {overall_success_rate:.1f}% COMPLETION'}

## Newly Installed Modules
{chr(10).join(f"- {module}" for module in successful_installs) if successful_installs else "None"}

## Failed Modules Requiring Analysis
{chr(10).join(f"- {module}: {error[:100]}..." for module, error in failed_modules[:10]) if failed_modules else "None"}

---
Generated by ZOE 100x Engineer
"""
    
    with open('ZOE_PROJECT_COMPLETION_REPORT.md', 'w') as f:
        f.write(completion_report)
    
    print("📄 Completion report saved to ZOE_PROJECT_COMPLETION_REPORT.md")
    
    return overall_success_rate, failed_modules

if __name__ == "__main__":
    success_rate, failed = main()
    
    print(f"\n🎯 FINAL PROJECT STATUS: {success_rate:.1f}% COMPLETION ACHIEVED")
    
    if success_rate >= 95:
        print("🏆 ZOE 100x ENGINEER MISSION: EXCELLENT SUCCESS!")
    elif len(failed) > 0:
        print(f"🔄 ZOE 100x ENGINEER - {len(failed)} modules require deeper analysis")
