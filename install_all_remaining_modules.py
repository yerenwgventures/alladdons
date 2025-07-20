#!/usr/bin/env python3
"""
Install All Remaining Modules
Systematically installs all previously failed modules after fixes
"""
import subprocess
import json
import time

def load_uninstalled_modules():
    """Load the list of uninstalled modules"""
    try:
        with open('uninstalled_modules_list.json', 'r') as f:
            data = json.load(f)
            return data['uninstalled_module_list']
    except FileNotFoundError:
        print("❌ Uninstalled modules list not found")
        return []

def install_module(module_name):
    """Install a single module and return result"""
    print(f"  📦 Installing {module_name}...")
    
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_instance', 
            'odoo', '-d', 'cbms_test_db', '-i', module_name, '--stop-after-init'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"  ✅ {module_name} - SUCCESS")
            return True, "SUCCESS"
        else:
            # Extract key error information
            error_lines = result.stderr.split('\n')
            key_error = "Unknown error"
            
            for line in error_lines:
                if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed']):
                    key_error = line.strip()[:100]
                    break
            
            print(f"  ❌ {module_name} - FAILED: {key_error}")
            return False, key_error
            
    except subprocess.TimeoutExpired:
        print(f"  ⏰ {module_name} - TIMEOUT")
        return False, "TIMEOUT"
    except Exception as e:
        print(f"  💥 {module_name} - ERROR: {str(e)}")
        return False, str(e)

def main():
    print("🚀 INSTALLING ALL REMAINING MODULES")
    print("=" * 60)
    
    # Load uninstalled modules
    uninstalled_modules = load_uninstalled_modules()
    
    if not uninstalled_modules:
        print("❌ No uninstalled modules found")
        return
    
    print(f"📊 Found {len(uninstalled_modules)} modules to install")
    print()
    
    # Install each module
    successful_installs = []
    failed_installs = []
    
    for i, module in enumerate(uninstalled_modules, 1):
        print(f"[{i:2d}/{len(uninstalled_modules)}] Processing {module}")
        
        success, error = install_module(module)
        
        if success:
            successful_installs.append(module)
        else:
            failed_installs.append((module, error))
        
        # Brief pause between installations
        time.sleep(2)
        print()
    
    # Final summary
    print("=" * 60)
    print("📋 INSTALLATION RESULTS SUMMARY")
    print("=" * 60)
    
    total_modules = len(uninstalled_modules)
    success_count = len(successful_installs)
    failed_count = len(failed_installs)
    
    print(f"📊 Total modules processed: {total_modules}")
    print(f"✅ Successfully installed: {success_count} ({success_count/total_modules*100:.1f}%)")
    print(f"❌ Failed to install: {failed_count} ({failed_count/total_modules*100:.1f}%)")
    print()
    
    if successful_installs:
        print("✅ NEWLY INSTALLED MODULES:")
        for module in successful_installs:
            print(f"  • {module}")
        print()
    
    if failed_installs:
        print("❌ STILL FAILED MODULES:")
        for module, error in failed_installs:
            print(f"  • {module}: {error}")
        print()
    
    # Save results
    results = {
        "total_processed": total_modules,
        "newly_successful": successful_installs,
        "still_failed": [{"module": m, "error": e} for m, e in failed_installs],
        "success_rate": success_count/total_modules*100 if total_modules > 0 else 0
    }
    
    with open('final_installation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("📄 Results saved to final_installation_results.json")
    
    # Overall assessment
    print()
    print("🎯 OVERALL PROJECT STATUS:")
    
    # Calculate total project statistics
    total_project_modules = 491  # Total modules in project
    previously_installed = 440   # Previously successfully installed
    newly_installed = success_count
    total_installed = previously_installed + newly_installed
    
    print(f"  📊 Total project modules: {total_project_modules}")
    print(f"  ✅ Total successfully installed: {total_installed}")
    print(f"  📈 Overall project success rate: {total_installed/total_project_modules*100:.1f}%")
    
    if total_installed/total_project_modules >= 0.95:
        print(f"  🏆 EXCELLENT: 95%+ modules successfully installed!")
    elif total_installed/total_project_modules >= 0.90:
        print(f"  👍 VERY GOOD: 90%+ modules successfully installed!")
    elif total_installed/total_project_modules >= 0.85:
        print(f"  ✅ GOOD: 85%+ modules successfully installed!")
    else:
        print(f"  ⚠️ MORE WORK NEEDED: Less than 85% success rate")

if __name__ == "__main__":
    main()
