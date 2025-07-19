#!/usr/bin/env python3
"""
Analyze Uninstalled Module Issues
Tests installation and captures detailed error logs for uninstalled modules
"""
import os
import subprocess
import json
import ast
from pathlib import Path

def load_uninstalled_modules():
    """Load the list of uninstalled modules"""
    try:
        with open('uninstalled_modules_list.json', 'r') as f:
            data = json.load(f)
            return data['uninstalled_module_list']
    except FileNotFoundError:
        print("❌ Uninstalled modules list not found")
        return []

def analyze_manifest_issues(module_name):
    """Analyze manifest file for potential issues"""
    manifest_path = Path(module_name) / '__manifest__.py'
    
    if not manifest_path.exists():
        return ["Missing __manifest__.py file"]
    
    issues = []
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse manifest
        tree = ast.parse(content)
        manifest_dict = ast.literal_eval(tree.body[0].value)
        
        # Check for enterprise dependencies
        enterprise_modules = [
            'account_accountant', 'account_asset', 'account_budget', 'account_consolidation',
            'account_invoice_extract', 'account_reports', 'account_sepa', 'account_taxcloud',
            'approvals', 'documents', 'documents_hr', 'documents_project', 'documents_spreadsheet',
            'helpdesk', 'hr_payroll', 'hr_payroll_account', 'industry_fsm', 'iot',
            'knowledge', 'l10n_be_hr_payroll', 'marketing_automation', 'mrp_plm', 'mrp_workorder',
            'planning', 'project_enterprise', 'quality', 'sale_subscription', 'sign', 'social',
            'stock_barcode', 'studio', 'timesheet_grid', 'voip', 'web_studio'
        ]
        
        depends = manifest_dict.get('depends', [])
        enterprise_deps = [dep for dep in depends if dep in enterprise_modules]
        
        if enterprise_deps:
            issues.append(f"Enterprise dependencies: {enterprise_deps}")
        
        # Check for external dependencies
        external_deps = manifest_dict.get('external_dependencies', {})
        python_deps = external_deps.get('python', [])
        
        if python_deps:
            issues.append(f"External Python dependencies: {python_deps}")
        
        # Check installable flag
        if not manifest_dict.get('installable', True):
            issues.append("Module marked as not installable")
        
        # Check for missing data files
        data_files = manifest_dict.get('data', [])
        missing_files = []
        for data_file in data_files:
            if not (Path(module_name) / data_file).exists():
                missing_files.append(data_file)
        
        if missing_files:
            issues.append(f"Missing data files: {missing_files}")
        
        return issues
        
    except Exception as e:
        return [f"Manifest parsing error: {str(e)}"]

def test_module_installation(module_name):
    """Test module installation and capture detailed error log"""
    print(f"  🧪 Testing installation of {module_name}...")
    
    try:
        # Try to install the module
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_instance', 
            'odoo', '-d', 'cbms_test_db', '-i', module_name, '--stop-after-init'
        ], capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            return {
                "status": "SUCCESS",
                "error_log": "",
                "summary": "Module installed successfully"
            }
        else:
            # Parse error log
            error_lines = result.stderr.split('\n')
            
            # Extract key error information
            key_errors = []
            traceback_started = False
            
            for line in error_lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for specific error patterns
                if any(pattern in line.lower() for pattern in [
                    'modulenotfounderror', 'importerror', 'no module named',
                    'missing dependency', 'depends on', 'not found',
                    'traceback', 'exception', 'error', 'failed'
                ]):
                    key_errors.append(line)
                    if 'traceback' in line.lower():
                        traceback_started = True
                elif traceback_started and line.startswith('  '):
                    key_errors.append(line)
                elif traceback_started and not line.startswith('  '):
                    traceback_started = False
            
            # Summarize the error
            error_summary = "Unknown error"
            full_log = '\n'.join(key_errors[-15:])  # Last 15 relevant lines
            
            if 'modulenotfounderror' in full_log.lower():
                missing_module = ""
                for line in key_errors:
                    if 'no module named' in line.lower():
                        missing_module = line.split("'")[-2] if "'" in line else "unknown"
                        break
                error_summary = f"Missing Python module: {missing_module}"
            elif 'depends on' in full_log.lower():
                error_summary = "Missing Odoo module dependency"
            elif 'not found' in full_log.lower():
                error_summary = "Missing file or resource"
            elif 'importerror' in full_log.lower():
                error_summary = "Import error - missing dependency"
            
            return {
                "status": "FAILED",
                "error_log": full_log,
                "summary": error_summary
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "error_log": "Installation timed out after 180 seconds",
            "summary": "Installation timeout"
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "error_log": str(e),
            "summary": f"Test error: {str(e)}"
        }

def main():
    print("🔍 ANALYZING UNINSTALLED MODULE ISSUES")
    print("=" * 60)
    
    # Load uninstalled modules
    uninstalled_modules = load_uninstalled_modules()
    
    if not uninstalled_modules:
        print("❌ No uninstalled modules found")
        return
    
    print(f"📊 Analyzing {len(uninstalled_modules)} uninstalled modules...")
    print()
    
    # Analyze each module
    analysis_results = []
    issue_categories = {
        "ENTERPRISE_DEPENDENCY": [],
        "EXTERNAL_DEPENDENCY": [],
        "MISSING_FILES": [],
        "IMPORT_ERROR": [],
        "TIMEOUT": [],
        "OTHER": []
    }
    
    for i, module in enumerate(uninstalled_modules, 1):
        print(f"[{i:2d}/{len(uninstalled_modules)}] Analyzing {module}")
        
        # Check manifest issues
        manifest_issues = analyze_manifest_issues(module)
        
        # Test installation
        install_result = test_module_installation(module)
        
        # Categorize the issue
        category = "OTHER"
        if any("Enterprise dependencies" in issue for issue in manifest_issues):
            category = "ENTERPRISE_DEPENDENCY"
        elif any("External Python dependencies" in issue for issue in manifest_issues):
            category = "EXTERNAL_DEPENDENCY"
        elif any("Missing data files" in issue for issue in manifest_issues):
            category = "MISSING_FILES"
        elif install_result["status"] == "TIMEOUT":
            category = "TIMEOUT"
        elif "Missing Python module" in install_result["summary"]:
            category = "EXTERNAL_DEPENDENCY"
        elif "Import error" in install_result["summary"]:
            category = "IMPORT_ERROR"
        
        issue_categories[category].append(module)
        
        # Store detailed results
        analysis_results.append({
            "module": module,
            "category": category,
            "manifest_issues": manifest_issues,
            "install_test": install_result
        })
        
        # Print summary
        if install_result["status"] == "SUCCESS":
            print(f"    ✅ {install_result['summary']}")
        else:
            print(f"    ❌ {install_result['summary']}")
            if manifest_issues:
                print(f"    📋 Manifest issues: {len(manifest_issues)}")
        print()
    
    # Print summary
    print("=" * 60)
    print("📋 UNINSTALLED MODULES ANALYSIS SUMMARY")
    print("=" * 60)
    
    for category, modules in issue_categories.items():
        if modules:
            category_name = category.replace('_', ' ').title()
            print(f"🔧 {category_name}: {len(modules)} modules")
            for module in modules[:3]:  # Show first 3
                print(f"  • {module}")
            if len(modules) > 3:
                print(f"  ... and {len(modules) - 3} more")
            print()
    
    # Save detailed results
    summary = {
        "total_uninstalled": len(uninstalled_modules),
        "categories": {k: len(v) for k, v in issue_categories.items()},
        "category_details": issue_categories,
        "detailed_analysis": analysis_results
    }
    
    with open('uninstalled_modules_detailed_analysis.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("📄 Detailed analysis saved to uninstalled_modules_detailed_analysis.json")
    
    # Recommendations
    print()
    print("🎯 RECOMMENDATIONS:")
    enterprise_count = len(issue_categories["ENTERPRISE_DEPENDENCY"])
    external_count = len(issue_categories["EXTERNAL_DEPENDENCY"])
    missing_files_count = len(issue_categories["MISSING_FILES"])
    
    if enterprise_count > 0:
        print(f"  🏢 {enterprise_count} modules require Odoo Enterprise edition")
    if external_count > 0:
        print(f"  📦 {external_count} modules need external Python libraries")
    if missing_files_count > 0:
        print(f"  📁 {missing_files_count} modules have missing files (fixable)")
    
    fixable_count = missing_files_count + len(issue_categories["OTHER"])
    if fixable_count > 0:
        print(f"  🔧 {fixable_count} modules potentially fixable")

if __name__ == "__main__":
    main()
