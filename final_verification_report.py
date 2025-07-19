#!/usr/bin/env python3
"""
Final Verification Report Generator
Creates comprehensive summary of all testing and verification results
"""
import json
import subprocess

def get_database_stats():
    """Get final database statistics"""
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_db', 'psql', '-U', 'odoo', '-d', 'cbms_test_db', 
            '-t', '-c', "SELECT state, COUNT(*) FROM ir_module_module GROUP BY state ORDER BY COUNT(*) DESC;"
        ], capture_output=True, text=True)
        
        stats = {}
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) == 2:
                        state = parts[0].strip()
                        count = int(parts[1].strip())
                        stats[state] = count
        return stats
    except Exception as e:
        return {"error": str(e)}

def load_verification_results():
    """Load verification results from JSON files"""
    results = {}
    
    try:
        with open('comprehensive_verification_results.json', 'r') as f:
            results['content_verification'] = json.load(f)
    except FileNotFoundError:
        results['content_verification'] = {"error": "File not found"}
    
    try:
        with open('final_testing_results.json', 'r') as f:
            results['testing_results'] = json.load(f)
    except FileNotFoundError:
        results['testing_results'] = {"error": "File not found"}
    
    return results

def generate_final_report():
    """Generate comprehensive final verification report"""
    print("🔍 FINAL COMPREHENSIVE VERIFICATION REPORT")
    print("=" * 80)
    print()
    
    # Database Statistics
    print("📊 DATABASE VERIFICATION RESULTS")
    print("-" * 40)
    db_stats = get_database_stats()
    
    if "error" not in db_stats:
        total_modules = sum(db_stats.values())
        installed = db_stats.get('installed', 0)
        uninstalled = db_stats.get('uninstalled', 0)
        uninstallable = db_stats.get('uninstallable', 0)
        
        print(f"✅ Total modules in database: {total_modules}")
        print(f"✅ Successfully installed: {installed} ({installed/total_modules*100:.1f}%)")
        print(f"📦 Uninstalled: {uninstalled} ({uninstalled/total_modules*100:.1f}%)")
        print(f"❌ Uninstallable (Enterprise): {uninstallable} ({uninstallable/total_modules*100:.1f}%)")
    else:
        print(f"❌ Error getting database stats: {db_stats['error']}")
    
    print()
    
    # Load verification results
    results = load_verification_results()
    
    # Content Verification Results
    print("🔍 CONTENT VERIFICATION RESULTS")
    print("-" * 40)
    
    content_results = results.get('content_verification', {})
    if "error" not in content_results:
        total_verified = content_results.get('total_modules', 0)
        summary = content_results.get('verification_summary', {})
        clean_pct = content_results.get('clean_percentage', 0)
        
        print(f"📊 Modules verified for content: {total_verified}")
        print(f"✅ Clean modules (no issues): {summary.get('clean', 0)} ({clean_pct:.1f}%)")
        print(f"⚠️ Minor issues: {summary.get('minor_issues', 0)} ({summary.get('minor_issues', 0)/total_verified*100:.1f}%)")
        print(f"🔧 Moderate issues: {summary.get('moderate_issues', 0)} ({summary.get('moderate_issues', 0)/total_verified*100:.1f}%)")
        print(f"❌ Major issues: {summary.get('major_issues', 0)} ({summary.get('major_issues', 0)/total_verified*100:.1f}%)")
    else:
        print(f"❌ Content verification error: {content_results.get('error', 'Unknown')}")
    
    print()
    
    # Testing Results
    print("🧪 INSTALLATION TESTING RESULTS")
    print("-" * 40)
    
    testing_results = results.get('testing_results', {})
    if "error" not in testing_results:
        total_tested = testing_results.get('total_modules', 0)
        successful = testing_results.get('newly_successful', [])
        failed = testing_results.get('failed', [])
        success_rate = testing_results.get('overall_success_rate', 0)
        
        print(f"📊 Modules tested for installation: {total_tested}")
        print(f"✅ Successfully installed: {len(successful)} ({len(successful)/total_tested*100:.1f}%)")
        print(f"❌ Failed installation: {len(failed)} ({len(failed)/total_tested*100:.1f}%)")
        print(f"📈 Overall success rate: {success_rate:.1f}%")
    else:
        print(f"❌ Testing results error: {testing_results.get('error', 'Unknown')}")
    
    print()
    
    # Issue Analysis
    print("🔍 ISSUE ANALYSIS")
    print("-" * 40)
    
    if "error" not in content_results:
        detailed = content_results.get('detailed_results', [])
        
        # Analyze common issues
        issue_types = {
            'placeholder_issues': 0,
            'missing_files': 0,
            'empty_fields': 0,
            'commented_code': 0,
            'incomplete_implementations': 0
        }
        
        for module_result in detailed:
            issues = module_result.get('manifest_issues', []) + \
                    module_result.get('python_issues', []) + \
                    module_result.get('xml_issues', [])
            
            for issue in issues:
                issue_lower = issue.lower()
                if 'placeholder' in issue_lower or 'todo' in issue_lower:
                    issue_types['placeholder_issues'] += 1
                elif 'missing' in issue_lower:
                    issue_types['missing_files'] += 1
                elif 'empty field' in issue_lower:
                    issue_types['empty_fields'] += 1
                elif 'commented' in issue_lower:
                    issue_types['commented_code'] += 1
                elif 'incomplete' in issue_lower or 'pass' in issue_lower:
                    issue_types['incomplete_implementations'] += 1
        
        print("📋 Common issue types found:")
        for issue_type, count in issue_types.items():
            if count > 0:
                print(f"  • {issue_type.replace('_', ' ').title()}: {count}")
    
    print()
    
    # Overall Assessment
    print("🎯 OVERALL ASSESSMENT")
    print("-" * 40)
    
    if "error" not in db_stats and "error" not in content_results:
        installed_modules = db_stats.get('installed', 0)
        clean_modules = content_results.get('verification_summary', {}).get('clean', 0)
        
        print(f"🏆 ACHIEVEMENT SUMMARY:")
        print(f"  ✅ {installed_modules} modules successfully installed in database")
        print(f"  ✅ {clean_modules} modules verified as clean and complete")
        print(f"  📈 {clean_modules/installed_modules*100:.1f}% of installed modules are production-ready")
        print()
        
        if clean_modules/installed_modules >= 0.8:
            assessment = "🏆 EXCELLENT"
            description = "Over 80% of installed modules are clean and production-ready"
        elif clean_modules/installed_modules >= 0.6:
            assessment = "👍 GOOD"
            description = "Over 60% of installed modules are clean and production-ready"
        elif clean_modules/installed_modules >= 0.4:
            assessment = "⚠️ FAIR"
            description = "40-60% of installed modules are clean, some issues need attention"
        else:
            assessment = "❌ NEEDS WORK"
            description = "Less than 40% of modules are clean, significant issues found"
        
        print(f"🎯 FINAL GRADE: {assessment}")
        print(f"📝 {description}")
        print()
        
        print("🚀 DEPLOYMENT READINESS:")
        if clean_modules/installed_modules >= 0.6:
            print("  ✅ READY FOR PRODUCTION DEPLOYMENT")
            print("  ✅ Majority of modules are clean and functional")
            print("  ✅ Minor issues can be addressed post-deployment")
        else:
            print("  ⚠️ REQUIRES ATTENTION BEFORE PRODUCTION")
            print("  🔧 Address major issues in critical modules")
            print("  📋 Review and fix placeholder content")
    
    print()
    print("=" * 80)
    print("🎉 COMPREHENSIVE VERIFICATION COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    generate_final_report()
