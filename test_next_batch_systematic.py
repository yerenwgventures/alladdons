#!/usr/bin/env python3
"""
Systematic Module Testing - Next Batch
Tests modules in alphabetical order and reports results
"""
import os
import subprocess
import time
from pathlib import Path

def get_next_modules_to_test(start_from=None, batch_size=10):
    """Get next batch of modules to test"""
    modules = []
    for item in sorted(os.listdir('.')):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, '__manifest__.py')):
            modules.append(item)
    
    if start_from:
        try:
            start_index = modules.index(start_from)
            return modules[start_index:start_index + batch_size]
        except ValueError:
            pass
    
    return modules[:batch_size]

def test_module(module_name):
    """Test a single module installation"""
    print(f"  📦 Testing {module_name}...")
    
    try:
        result = subprocess.run([
            'docker', 'exec', 'odoo_test_instance', 
            'odoo', '-d', 'cbms_test_db', '-i', module_name, '--stop-after-init'
        ], capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            print(f"  ✅ {module_name} - SUCCESS")
            return True, "SUCCESS"
        else:
            error_msg = result.stderr.split('\n')[-10:]  # Last 10 lines
            print(f"  ❌ {module_name} - FAILED")
            return False, '\n'.join(error_msg)
            
    except subprocess.TimeoutExpired:
        print(f"  ⏰ {module_name} - TIMEOUT")
        return False, "TIMEOUT"
    except Exception as e:
        print(f"  💥 {module_name} - ERROR: {str(e)}")
        return False, str(e)

def main():
    """Main testing function"""
    print("🚀 SYSTEMATIC MODULE TESTING - NEXT BATCH")
    print("=" * 50)
    
    # Get modules that haven't been tested yet (starting from 'a')
    tested_modules = [
        'access_restriction_by_ip', 'account_bank_statement_import_csv',
        'account_bank_statement_import_txt', 'account_invoice_report_xlsx',
        'account_move_line_report_xlsx', 'account_payment_report_xlsx',
        'account_report_send_by_mail', 'account_trial_balance_report_xlsx',
        'advance_hr_attendance_dashboard', 'advanced_loan_management',
        'all_in_one_html_notes', 'all_in_one_inventory_kit',
        'all_in_one_pos_kit', 'all_in_one_purchase_kit',
        'all_in_one_sales_kit', 'all_in_one_website_kit',
        'amazon_s3_storage', 'analytical_account_report_xlsx',
        'analytical_report_xlsx', 'api_rest_base',
        'api_rest_partner', 'api_rest_product',
        'approval_connector', 'hr_timesheet_description',
        'print_subscription_id_card', 'product_multi_document',
        'website_sign_sending_by_priority',
        # Batch 2 - All successful
        'account_interest_on_overdue_invoice', 'account_journal_discount',
        'account_line_view', 'account_move_multi_cancel',
        'account_payment_approval', 'account_restrict_journal',
        'activity_dashboard_mngmnt', 'activity_reminder',
        'advance_cash_flow_statements', 'advance_signup_page',
        'advanced_chatter_view', 'advanced_excel_reports',
        'advanced_pos_reports', 'advanced_vat_invoice',
        'age_restricted_product_pos',
        # Batch 3 - Mixed results, all fixed
        'age_verification_odoo', 'all_in_one_dynamic_custom_fields',
        'amount_in_words_invoice', 'analytic_accounts_on_stock_picking',
        'artify_backend_theme', 'attendance_regularization',
        'attendance_view_calendar', 'auto_daily_weekly_report',
        'auto_database_backup', 'auto_fill',
        'auto_logout_idle_user_odoo', 'auto_save_restrict',
        'automatic_invoice_and_post', 'automatic_payroll',
        'automatic_project_task_timer'
    ]
    
    # Get all modules
    all_modules = []
    for item in sorted(os.listdir('.')):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, '__manifest__.py')):
            all_modules.append(item)
    
    # Find untested modules
    untested_modules = [m for m in all_modules if m not in tested_modules]
    
    print(f"📊 Found {len(untested_modules)} untested modules")
    print(f"🎯 Testing next batch of 15 modules...")
    print()
    
    # Test next batch
    batch = untested_modules[:15]
    results = []
    
    for i, module in enumerate(batch, 1):
        print(f"[{i:2d}/15] Testing {module}")
        success, details = test_module(module)
        results.append({
            'module': module,
            'success': success,
            'details': details
        })
        time.sleep(2)  # Brief pause between tests
        print()
    
    # Summary
    print("📋 BATCH TESTING RESULTS")
    print("=" * 30)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"📊 Success Rate: {len(successful)/len(results)*100:.1f}%")
    print()
    
    if successful:
        print("✅ SUCCESSFUL MODULES:")
        for result in successful:
            print(f"  • {result['module']}")
        print()
    
    if failed:
        print("❌ FAILED MODULES:")
        for result in failed:
            print(f"  • {result['module']}: {result['details'][:100]}...")
        print()
    
    # Save detailed results
    with open('batch_test_results.txt', 'w') as f:
        f.write("SYSTEMATIC MODULE TESTING RESULTS\n")
        f.write("=" * 40 + "\n\n")
        
        for result in results:
            f.write(f"MODULE: {result['module']}\n")
            f.write(f"STATUS: {'SUCCESS' if result['success'] else 'FAILED'}\n")
            if not result['success']:
                f.write(f"DETAILS: {result['details']}\n")
            f.write("-" * 40 + "\n")
    
    print(f"📄 Detailed results saved to batch_test_results.txt")
    print(f"🎯 Next batch will start from: {untested_modules[15] if len(untested_modules) > 15 else 'END'}")

if __name__ == "__main__":
    main()
