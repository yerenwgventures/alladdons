#!/usr/bin/env python3
"""
Analyze Never Installed Modules
Determines which modules have never been successfully installed in any database
by analyzing all available installation logs and results.
"""

import json
import os
from datetime import datetime

def load_json_safe(filepath):
    """Safely load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}

def get_all_project_modules():
    """Get all modules in the project directory"""
    modules = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.') and not item.startswith('__'):
            if os.path.exists(os.path.join(item, '__manifest__.py')):
                modules.append(item)
    return sorted(modules)

def analyze_installation_history():
    """Analyze all installation logs to determine which modules were never installed"""
    
    all_modules = set(get_all_project_modules())
    
    # Track modules that were successfully installed at some point
    ever_installed = set()
    
    # Load all available result files
    result_files = [
        'installed_modules_verification.json',  # Pre-crash successful installations
        'zoe_final_100_percent_results.json',   # Final attempt results
        'zoe_systematic_installation_results.json',  # Systematic attempt
        'comprehensive_installation_results.json',   # Comprehensive attempt
        'COMPLETE_PRODUCTION_VALIDATION.json'       # Production validation
    ]
    
    print("🔍 ANALYZING INSTALLATION HISTORY")
    print("=" * 50)
    
    for result_file in result_files:
        if os.path.exists(result_file):
            print(f"📄 Analyzing: {result_file}")
            data = load_json_safe(result_file)
            
            # Extract successful modules from different file formats
            if 'sample_clean_modules' in data:
                # Pre-crash verification file
                ever_installed.update(data['sample_clean_modules'])
                print(f"  ✅ Found {len(data['sample_clean_modules'])} clean modules (sample)")
                if 'clean_modules' in data:
                    print(f"  📊 Total clean modules reported: {data['clean_modules']}")
            
            if 'newly_successful' in data:
                # Final results file
                ever_installed.update(data['newly_successful'])
                print(f"  ✅ Found {len(data['newly_successful'])} newly successful modules")
            
            if 'successful_modules' in data:
                # Systematic results
                ever_installed.update(data['successful_modules'])
                print(f"  ✅ Found {len(data['successful_modules'])} successful modules")
            
            if 'detailed_results' in data:
                # Production validation results
                production_ready = [r['module'] for r in data['detailed_results'] if r.get('production_ready', False)]
                ever_installed.update(production_ready)
                print(f"  ✅ Found {len(production_ready)} production ready modules")
        else:
            print(f"❌ File not found: {result_file}")
    
    # Calculate never installed modules
    never_installed = all_modules - ever_installed
    
    print(f"\n📊 INSTALLATION HISTORY ANALYSIS:")
    print(f"  📋 Total project modules: {len(all_modules)}")
    print(f"  ✅ Ever successfully installed: {len(ever_installed)}")
    print(f"  ❌ Never successfully installed: {len(never_installed)}")
    print(f"  📈 Success rate (ever installed): {(len(ever_installed)/len(all_modules)*100):.1f}%")
    
    # Analyze the 13 newly ready modules
    newly_ready_modules = {
        'cw_stock', 'franchise_management', 'gym_mgmt_system', 'hotel_management_odoo',
        'legal_case_management', 'medical_lab_management', 'portal_stock_check',
        'website_bargain', 'website_gdpr_odoo', 'website_maintenance_page',
        'website_pre_booking', 'website_warranty_management', 'theme_fasion'
    }
    
    newly_ready_never_installed = newly_ready_modules & never_installed
    newly_ready_ever_installed = newly_ready_modules & ever_installed
    
    print(f"\n🎯 13 NEWLY READY MODULES ANALYSIS:")
    print(f"  ✅ Were previously installed: {len(newly_ready_ever_installed)}")
    for module in sorted(newly_ready_ever_installed):
        print(f"    - {module}")
    print(f"  ❌ Never been installed: {len(newly_ready_never_installed)}")
    for module in sorted(newly_ready_never_installed):
        print(f"    - {module}")
    
    # Analyze remaining 15 modules that need fixes
    remaining_15_modules = {
        'base_accounting_kit', 'call_for_price_website', 'cw_account', 'cw_mrp', 
        'cw_purchase', 'cw_sale', 'customer_credit_payment_website',
        'education_fee', 'education_university_management', 
        'legal_case_management_dashboard', 'salon_management', 'theme_autofly', 
        'theme_boec', 'theme_coffee_shop', 'theme_shopping'
    }
    
    remaining_15_never_installed = remaining_15_modules & never_installed
    remaining_15_ever_installed = remaining_15_modules & ever_installed
    
    print(f"\n🔧 15 REMAINING MODULES ANALYSIS:")
    print(f"  ✅ Were previously installed: {len(remaining_15_ever_installed)}")
    for module in sorted(remaining_15_ever_installed):
        print(f"    - {module}")
    print(f"  ❌ Never been installed: {len(remaining_15_never_installed)}")
    for module in sorted(remaining_15_never_installed):
        print(f"    - {module}")
    
    # Create detailed report
    report = {
        'analysis_timestamp': datetime.now().isoformat(),
        'total_modules': len(all_modules),
        'ever_installed_count': len(ever_installed),
        'never_installed_count': len(never_installed),
        'success_rate_ever_installed': len(ever_installed)/len(all_modules)*100,
        'ever_installed_modules': sorted(list(ever_installed)),
        'never_installed_modules': sorted(list(never_installed)),
        'newly_ready_13_analysis': {
            'total': len(newly_ready_modules),
            'ever_installed': sorted(list(newly_ready_ever_installed)),
            'never_installed': sorted(list(newly_ready_never_installed))
        },
        'remaining_15_analysis': {
            'total': len(remaining_15_modules),
            'ever_installed': sorted(list(remaining_15_ever_installed)),
            'never_installed': sorted(list(remaining_15_never_installed))
        }
    }
    
    # Save detailed report
    with open('NEVER_INSTALLED_MODULES_ANALYSIS.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: NEVER_INSTALLED_MODULES_ANALYSIS.json")
    
    return report

def main():
    """Main analysis function"""
    report = analyze_installation_history()
    
    print(f"\n🎯 KEY INSIGHTS:")
    
    # Check if the 13 newly ready modules were ever installed
    newly_ready_never = report['newly_ready_13_analysis']['never_installed']
    if len(newly_ready_never) == 0:
        print("  ✅ All 13 newly ready modules were previously installed successfully!")
        print("  🎯 This confirms they are truly production ready")
    else:
        print(f"  ⚠️  {len(newly_ready_never)} of the 13 newly ready modules were never installed:")
        for module in newly_ready_never:
            print(f"    - {module}")
    
    # Check the remaining 15 modules
    remaining_never = report['remaining_15_analysis']['never_installed']
    remaining_ever = report['remaining_15_analysis']['ever_installed']
    
    print(f"\n🔧 REMAINING 15 MODULES PRIORITY:")
    if len(remaining_ever) > 0:
        print(f"  🏆 HIGH PRIORITY - Were previously installed ({len(remaining_ever)} modules):")
        for module in remaining_ever:
            print(f"    - {module} (just needs dependency fixes)")
    
    if len(remaining_never) > 0:
        print(f"  ⚠️  MEDIUM PRIORITY - Never been installed ({len(remaining_never)} modules):")
        for module in remaining_never:
            print(f"    - {module} (may need more complex fixes)")
    
    print(f"\n📊 OVERALL PROJECT STATUS:")
    print(f"  🎯 Modules that work: {report['ever_installed_count']}/{report['total_modules']} ({report['success_rate_ever_installed']:.1f}%)")
    print(f"  🔧 Modules never installed: {report['never_installed_count']}/{report['total_modules']} ({100-report['success_rate_ever_installed']:.1f}%)")
    
    return report

if __name__ == "__main__":
    main()
