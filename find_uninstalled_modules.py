#!/usr/bin/env python3
"""
Find Uninstalled Modules
Identifies which modules from the directory are not installed
"""
import os
import subprocess

def get_all_directory_modules():
    """Get all modules in the current directory"""
    modules = []
    for item in sorted(os.listdir('.')):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, '__manifest__.py')):
            modules.append(item)
    return modules

def get_installed_modules():
    """Get modules that are installed in database"""
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_db', 'psql', '-U', 'odoo', '-d', 'cbms_test_db', 
            '-t', '-c', "SELECT name FROM ir_module_module WHERE state = 'installed' ORDER BY name;"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            installed = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return installed
        return []
    except Exception as e:
        print(f"Error getting installed modules: {e}")
        return []

def get_uninstallable_modules():
    """Get modules marked as uninstallable"""
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_db', 'psql', '-U', 'odoo', '-d', 'cbms_test_db', 
            '-t', '-c', "SELECT name FROM ir_module_module WHERE state = 'uninstallable' ORDER BY name;"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            uninstallable = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return uninstallable
        return []
    except Exception as e:
        print(f"Error getting uninstallable modules: {e}")
        return []

def main():
    print("🔍 FINDING UNINSTALLED MODULES")
    print("=" * 50)
    
    # Get all modules
    all_modules = get_all_directory_modules()
    installed_modules = get_installed_modules()
    uninstallable_modules = get_uninstallable_modules()
    
    print(f"📊 Total modules in directory: {len(all_modules)}")
    print(f"✅ Installed modules: {len(installed_modules)}")
    print(f"❌ Uninstallable modules: {len(uninstallable_modules)}")
    print()
    
    # Find modules that exist in directory but are not installed
    directory_modules_set = set(all_modules)
    installed_modules_set = set(installed_modules)
    uninstallable_modules_set = set(uninstallable_modules)
    
    # Modules in directory that are installed
    installed_from_directory = directory_modules_set.intersection(installed_modules_set)
    
    # Modules in directory that are uninstallable
    uninstallable_from_directory = directory_modules_set.intersection(uninstallable_modules_set)
    
    # Modules in directory that are neither installed nor uninstallable
    uninstalled_modules = directory_modules_set - installed_modules_set - uninstallable_modules_set
    
    print(f"✅ Directory modules successfully installed: {len(installed_from_directory)}")
    print(f"❌ Directory modules marked uninstallable: {len(uninstallable_from_directory)}")
    print(f"🔧 Directory modules not installed: {len(uninstalled_modules)}")
    print()
    
    if uninstalled_modules:
        print("🔧 MODULES NOT INSTALLED:")
        print("-" * 30)
        for i, module in enumerate(sorted(uninstalled_modules), 1):
            print(f"{i:3d}. {module}")
        print()
    
    if uninstallable_from_directory:
        print("❌ MODULES MARKED UNINSTALLABLE:")
        print("-" * 30)
        for i, module in enumerate(sorted(uninstallable_from_directory), 1):
            print(f"{i:3d}. {module}")
        print()
    
    # Save results
    results = {
        "total_directory_modules": len(all_modules),
        "installed_from_directory": len(installed_from_directory),
        "uninstallable_from_directory": len(uninstallable_from_directory),
        "uninstalled_modules": len(uninstalled_modules),
        "uninstalled_module_list": sorted(list(uninstalled_modules)),
        "uninstallable_module_list": sorted(list(uninstallable_from_directory))
    }
    
    import json
    with open('uninstalled_modules_list.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("📄 Results saved to uninstalled_modules_list.json")
    
    # Summary
    success_rate = len(installed_from_directory) / len(all_modules) * 100
    print()
    print("📊 SUMMARY:")
    print(f"  Success Rate: {success_rate:.1f}% of directory modules installed")
    print(f"  {len(uninstalled_modules)} modules need investigation")

if __name__ == "__main__":
    main()
