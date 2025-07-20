#!/usr/bin/env python3
"""
Analyze Remaining 28 Modules
Detailed analysis of the 28 modules that need review to determine:
1. Exact dependencies required
2. Whether dependencies are standard Odoo modules
3. What actions are needed to make them production ready
4. Priority order for fixing
"""

import os
import json
import ast
from datetime import datetime

# List of 28 modules that need review
MODULES_TO_ANALYZE = [
    'base_accounting_kit', 'call_for_price_website', 'cw_account', 'cw_mrp', 
    'cw_purchase', 'cw_sale', 'cw_stock', 'customer_credit_payment_website',
    'education_fee', 'education_university_management', 'franchise_management',
    'gym_mgmt_system', 'hotel_management_odoo', 'legal_case_management',
    'legal_case_management_dashboard', 'medical_lab_management', 'portal_stock_check',
    'salon_management', 'theme_autofly', 'theme_boec', 'theme_coffee_shop',
    'theme_fasion', 'theme_shopping', 'website_bargain', 'website_gdpr_odoo',
    'website_maintenance_page', 'website_pre_booking', 'website_warranty_management'
]

# Standard Odoo modules (safe to depend on)
STANDARD_MODULES = {
    'base', 'web', 'mail', 'account', 'sale', 'purchase', 'stock', 'hr', 
    'project', 'crm', 'calendar', 'contacts', 'uom', 'product', 'portal',
    'website', 'website_sale', 'point_of_sale', 'mrp', 'fleet', 'event',
    'survey', 'lunch', 'membership', 'hr_attendance', 'hr_payroll', 'hr_contract',
    'hr_timesheet', 'stock_account', 'sale_management', 'purchase_stock',
    'website_blog', 'website_mass_mailing', 'auth_oauth', 'payment'
}

def analyze_module_dependencies(module_name):
    """Analyze a single module's dependencies"""
    module_path = os.path.join('.', module_name)
    manifest_path = os.path.join(module_path, '__manifest__.py')
    
    if not os.path.exists(manifest_path):
        return {
            'module': module_name,
            'status': 'missing_manifest',
            'dependencies': [],
            'issues': ['Missing __manifest__.py file']
        }
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
        
        manifest_dict = ast.literal_eval(manifest_content.strip())
        depends = manifest_dict.get('depends', [])
        
        # Categorize dependencies
        standard_deps = []
        custom_deps = []
        missing_deps = []
        
        for dep in depends:
            if dep in STANDARD_MODULES:
                standard_deps.append(dep)
            else:
                # Check if custom dependency exists in project
                if os.path.exists(os.path.join('.', dep)):
                    custom_deps.append(dep)
                else:
                    missing_deps.append(dep)
        
        # Determine action needed
        action_needed = "ready"
        issues = []
        
        if missing_deps:
            action_needed = "install_missing_deps"
            issues.append(f"Missing dependencies: {missing_deps}")
        elif custom_deps:
            action_needed = "install_custom_deps"
            issues.append(f"Custom dependencies: {custom_deps}")
        
        # Check if installable
        if not manifest_dict.get('installable', True):
            issues.append("Module marked as not installable")
            action_needed = "fix_installable"
        
        return {
            'module': module_name,
            'name': manifest_dict.get('name', module_name),
            'version': manifest_dict.get('version', 'Unknown'),
            'category': manifest_dict.get('category', 'Unknown'),
            'status': action_needed,
            'dependencies': {
                'all': depends,
                'standard': standard_deps,
                'custom': custom_deps,
                'missing': missing_deps
            },
            'issues': issues,
            'installable': manifest_dict.get('installable', True),
            'priority': determine_priority(module_name, manifest_dict.get('category', ''))
        }
        
    except Exception as e:
        return {
            'module': module_name,
            'status': 'manifest_error',
            'dependencies': [],
            'issues': [f'Manifest parsing error: {str(e)}']
        }

def determine_priority(module_name, category):
    """Determine priority based on module name and category"""
    if module_name.startswith('cw_'):
        return 'HIGH'  # Catch Weight modules are business critical
    elif 'accounting' in module_name.lower() or category == 'Accounting':
        return 'HIGH'
    elif module_name.startswith('theme_'):
        return 'LOW'  # Themes are less critical
    elif 'website' in module_name:
        return 'MEDIUM'
    elif any(word in module_name for word in ['hotel', 'gym', 'salon', 'medical', 'legal']):
        return 'MEDIUM'  # Specialized industry modules
    else:
        return 'MEDIUM'

def main():
    """Main analysis function"""
    print("🔍 ANALYZING REMAINING 28 MODULES")
    print("=" * 50)
    
    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'total_modules': len(MODULES_TO_ANALYZE),
        'modules_analyzed': [],
        'summary': {
            'ready': 0,
            'install_missing_deps': 0,
            'install_custom_deps': 0,
            'manifest_error': 0,
            'missing_manifest': 0
        },
        'by_priority': {
            'HIGH': [],
            'MEDIUM': [],
            'LOW': []
        }
    }
    
    print(f"📊 Analyzing {len(MODULES_TO_ANALYZE)} modules...")
    
    for module in MODULES_TO_ANALYZE:
        print(f"🔍 Analyzing: {module}")
        analysis = analyze_module_dependencies(module)
        results['modules_analyzed'].append(analysis)
        
        # Update summary
        status = analysis['status']
        results['summary'][status] = results['summary'].get(status, 0) + 1
        
        # Group by priority
        priority = analysis.get('priority', 'MEDIUM')
        results['by_priority'][priority].append(analysis)
        
        # Print status
        if analysis['status'] == 'ready':
            print(f"  ✅ Ready - Standard dependencies only")
        elif analysis['status'] == 'install_missing_deps':
            print(f"  ❌ Missing: {analysis['dependencies']['missing']}")
        elif analysis['status'] == 'install_custom_deps':
            print(f"  ⚠️  Custom deps: {analysis['dependencies']['custom']}")
        else:
            print(f"  🔧 Issues: {analysis['issues']}")
    
    # Save detailed results
    with open('REMAINING_28_MODULES_ANALYSIS.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n📊 ANALYSIS SUMMARY:")
    print(f"  ✅ Ready to install: {results['summary'].get('ready', 0)}")
    print(f"  ❌ Missing dependencies: {results['summary'].get('install_missing_deps', 0)}")
    print(f"  ⚠️  Custom dependencies: {results['summary'].get('install_custom_deps', 0)}")
    print(f"  🔧 Manifest errors: {results['summary'].get('manifest_error', 0)}")
    
    print(f"\n🎯 BY PRIORITY:")
    for priority in ['HIGH', 'MEDIUM', 'LOW']:
        modules = results['by_priority'][priority]
        print(f"  {priority}: {len(modules)} modules")
        for module in modules[:3]:  # Show first 3
            print(f"    - {module['module']} ({module['status']})")
        if len(modules) > 3:
            print(f"    ... and {len(modules) - 3} more")
    
    print(f"\n📄 Detailed analysis saved to: REMAINING_28_MODULES_ANALYSIS.json")
    
    return results

if __name__ == "__main__":
    main()
