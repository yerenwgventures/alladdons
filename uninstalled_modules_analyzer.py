#!/usr/bin/env python3
"""
Uninstalled Modules Analyzer
Identifies modules that failed to install and analyzes their issues
"""
import os
import subprocess
import json
import ast
from pathlib import Path

def get_all_modules_in_directory():
    """Get all modules in the current directory"""
    modules = []
    for item in sorted(os.listdir('.')):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, '__manifest__.py')):
            modules.append(item)
    return modules

def get_installed_modules():
    """Get modules that are successfully installed in database"""
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
    """Get modules marked as uninstallable (usually enterprise-only)"""
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

def analyze_module_issues(module_name):
    """Analyze why a module failed to install"""
    module_path = Path(module_name)
    
    if not module_path.exists():
        return {"error": "Module directory not found"}
    
    issues = []
    
    # Check manifest file
    manifest_path = module_path / '__manifest__.py'
    if not manifest_path.exists():
        issues.append("Missing __manifest__.py file")
        return {"issues": issues, "category": "MISSING_MANIFEST"}
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse manifest
        tree = ast.parse(content)
        manifest_dict = ast.literal_eval(tree.body[0].value)
        
        # Check dependencies
        depends = manifest_dict.get('depends', [])
        missing_deps = []
        
        # Check for enterprise dependencies
        enterprise_deps = [
            'account_accountant', 'account_asset', 'account_budget', 'account_consolidation',
            'account_invoice_extract', 'account_reports', 'account_sepa', 'account_taxcloud',
            'approvals', 'documents', 'documents_hr', 'documents_project', 'documents_spreadsheet',
            'helpdesk', 'hr_payroll', 'hr_payroll_account', 'industry_fsm', 'iot',
            'knowledge', 'l10n_be_hr_payroll', 'l10n_us_hr_payroll', 'marketing_automation',
            'mrp_plm', 'mrp_workorder', 'planning', 'project_enterprise', 'quality',
            'quality_control', 'quality_mrp', 'sale_subscription', 'sign', 'social',
            'stock_barcode', 'studio', 'timesheet_grid', 'voip', 'web_studio'
        ]
        
        for dep in depends:
            if dep in enterprise_deps:
                missing_deps.append(f"{dep} (Enterprise only)")
        
        if missing_deps:
            issues.append(f"Enterprise dependencies: {missing_deps}")
        
        # Check for missing data files
        data_files = manifest_dict.get('data', [])
        missing_files = []
        for data_file in data_files:
            if not (module_path / data_file).exists():
                missing_files.append(data_file)
        
        if missing_files:
            issues.append(f"Missing data files: {missing_files}")
        
        # Check for external dependencies
        external_depends = manifest_dict.get('external_dependencies', {})
        python_deps = external_depends.get('python', [])
        
        if python_deps:
            issues.append(f"External Python dependencies: {python_deps}")
        
        # Check installable flag
        if not manifest_dict.get('installable', True):
            issues.append("Module marked as not installable")
        
        # Check auto_install
        if manifest_dict.get('auto_install', False):
            issues.append("Auto-install module (may have dependency conflicts)")
        
        # Categorize the issue
        if missing_deps and any('Enterprise only' in dep for dep in missing_deps):
            category = "ENTERPRISE_DEPENDENCY"
        elif python_deps:
            category = "EXTERNAL_DEPENDENCY"
        elif missing_files:
            category = "MISSING_FILES"
        elif not manifest_dict.get('installable', True):
            category = "NOT_INSTALLABLE"
        else:
            category = "OTHER"
        
        return {
            "issues": issues,
            "category": category,
            "manifest_data": {
                "name": manifest_dict.get('name', ''),
                "version": manifest_dict.get('version', ''),
                "depends": depends,
                "installable": manifest_dict.get('installable', True),
                "auto_install": manifest_dict.get('auto_install', False)
            }
        }
        
    except Exception as e:
        issues.append(f"Manifest parsing error: {str(e)}")
        return {"issues": issues, "category": "PARSE_ERROR"}

def test_module_installation(module_name):
    """Test if a module can be installed and capture error log"""
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_instance', 
            'odoo', '-d', 'cbms_test_db', '-i', module_name, '--stop-after-init', '--log-level=error'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            return {"status": "SUCCESS", "log": ""}
        else:
            # Extract relevant error information
            error_lines = result.stderr.split('\n')
            relevant_errors = []
            
            for line in error_lines:
                if any(keyword in line.lower() for keyword in 
                      ['error', 'exception', 'traceback', 'failed', 'missing']):
                    relevant_errors.append(line.strip())
            
            return {
                "status": "FAILED", 
                "log": '\n'.join(relevant_errors[-10:])  # Last 10 relevant error lines
            }
            
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "log": "Installation timed out"}
    except Exception as e:
        return {"status": "ERROR", "log": str(e)}

def main():
    print("🔍 UNINSTALLED MODULES ANALYZER")
    print("=" * 60)
    
    # Get all modules and installed modules
    print("📊 Analyzing module installation status...")
    all_modules = get_all_modules_in_directory()
    installed_modules = get_installed_modules()
    uninstallable_modules = get_uninstallable_modules()
    
    # Find uninstalled modules
    uninstalled_modules = []
    for module in all_modules:
        if module not in installed_modules:
            uninstalled_modules.append(module)
    
    print(f"📊 Total modules in directory: {len(all_modules)}")
    print(f"✅ Successfully installed: {len(installed_modules)}")
    print(f"❌ Uninstallable (Enterprise): {len(uninstallable_modules)}")
    print(f"🔧 Not installed: {len(uninstalled_modules)}")
    print()
    
    if not uninstalled_modules:
        print("🎉 All modules are successfully installed!")
        return
    
    # Analyze uninstalled modules
    print(f"🔍 Analyzing {len(uninstalled_modules)} uninstalled modules...")
    print("-" * 50)
    
    analysis_results = []
    categories = {
        "ENTERPRISE_DEPENDENCY": [],
        "EXTERNAL_DEPENDENCY": [],
        "MISSING_FILES": [],
        "NOT_INSTALLABLE": [],
        "PARSE_ERROR": [],
        "OTHER": []
    }
    
    for i, module in enumerate(uninstalled_modules[:30], 1):  # Analyze first 30
        print(f"[{i:2d}/{min(30, len(uninstalled_modules))}] Analyzing {module}...")
        
        # Analyze issues
        analysis = analyze_module_issues(module)
        
        if "error" not in analysis:
            category = analysis["category"]
            categories[category].append(module)
            
            # Test installation to get error log
            print(f"    🧪 Testing installation...")
            install_test = test_module_installation(module)
            
            analysis["install_test"] = install_test
            analysis_results.append({
                "module": module,
                **analysis
            })
            
            if analysis["issues"]:
                print(f"    ❌ Issues: {len(analysis['issues'])}")
                for issue in analysis["issues"][:2]:  # Show first 2 issues
                    print(f"      • {issue}")
            else:
                print(f"    ✅ No obvious issues found")
        else:
            print(f"    💥 Error: {analysis['error']}")
    
    if len(uninstalled_modules) > 30:
        print(f"... (analyzed first 30 of {len(uninstalled_modules)} uninstalled modules)")
    
    print()
    print("=" * 60)
    print("📋 UNINSTALLED MODULES ANALYSIS SUMMARY")
    print("=" * 60)
    
    # Summary by category
    for category, modules in categories.items():
        if modules:
            category_name = category.replace('_', ' ').title()
            print(f"🔧 {category_name}: {len(modules)} modules")
            for module in modules[:5]:  # Show first 5
                print(f"  • {module}")
            if len(modules) > 5:
                print(f"  ... and {len(modules) - 5} more")
            print()
    
    # Save detailed results
    summary = {
        "total_modules": len(all_modules),
        "installed_modules": len(installed_modules),
        "uninstalled_modules": len(uninstalled_modules),
        "uninstallable_modules": len(uninstallable_modules),
        "categories": {k: len(v) for k, v in categories.items()},
        "detailed_analysis": analysis_results,
        "uninstalled_module_list": uninstalled_modules
    }
    
    with open('uninstalled_modules_analysis.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("📄 Detailed analysis saved to uninstalled_modules_analysis.json")
    
    # Recommendations
    print()
    print("🎯 RECOMMENDATIONS:")
    enterprise_count = len(categories["ENTERPRISE_DEPENDENCY"])
    external_count = len(categories["EXTERNAL_DEPENDENCY"])
    
    if enterprise_count > 0:
        print(f"  🏢 {enterprise_count} modules require Odoo Enterprise edition")
    if external_count > 0:
        print(f"  📦 {external_count} modules need external Python libraries")
    
    fixable_count = len(categories["MISSING_FILES"]) + len(categories["OTHER"])
    if fixable_count > 0:
        print(f"  🔧 {fixable_count} modules have fixable issues")

if __name__ == "__main__":
    main()
