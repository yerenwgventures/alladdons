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
        'automatic_project_task_timer',
        # Batch 4 - All successful after fixes
        'autosuggestion_in_discuss', 'backend_theme_odoo12',
        'barcode_capturing_sale_purchase', 'barcode_scanning_sale_purchase',
        'base_account_budget', 'base_accounting_kit',
        'batch_delivery_tracking', 'bill_digitization',
        'bom_comparison_report', 'bom_structure_in_excel_odoo',
        'bom_total_cost', 'bulk_create_mo_so_po',
        'call_for_price_website', 'cancel_landed_cost_odoo',
        'cancel_mo',
        # Batch 5 - All successful after fixes
        'cancel_quotation_expiry', 'chatter_activity_delay',
        'chatter_attachments_as_zip', 'chatter_attachments_manager',
        'chatter_camera', 'cleaning_management',
        'code_backend_theme', 'code_backend_theme_enterprise',
        'company_scrap_management', 'contact_documents',
        'contacts_birthday_greetings', 'cost_per_employee_manufacturing',
        'countrybased_terms_and_condition', 'create_expense_from_task_odoo',
        'crm_check_approve_limiter',
        # Batch 6 - All successful after fixes
        'crm_dashboard', 'crm_dynamic_fields',
        'cron_failure_notification', 'cts_theme_rozz',
        'custom_pivot_report', 'custom_receipts_for_pos',
        'custom_robots_txt', 'customer_credit_payment_website',
        'customer_image_and_tags_in_pos', 'customer_product_qrcode',
        'customer_sequence', 'customer_supplier_approval',
        'customers_dealers_quantity', 'customize_signup',
        'customized_barcode_generator',
        # Batch 7 - All successful after fixes
        'cw_account', 'cw_mrp', 'cw_purchase', 'cw_sale', 'cw_stock',
        'dark_mode_backend', 'dashboard_pos', 'database_delete_protection',
        'delivery_date_ecommerce', 'delivery_date_sale_order_line',
        'delivery_date_scheduler_odoo', 'delivery_split',
        'detect_unauthorized_login', 'developer_mode',
        'direct_send_email_template',
        # Batch 8 - 14/15 successful (dynamic_product_label_print has DB schema issue)
        'document_approval', 'dodger_blue', 'done_quantity_auto_fill',
        'dragable_and_resizable_wizard', 'duplicate_contact_details_alert',
        'duplicate_product_bom', 'dynamic_accounts_report',
        'dynamic_hover_on_related_fields', 'dynamic_image_hotspot',
        'dynamic_link_snippet', 'dynamic_product_pricelist',
        'dynamic_sale_order_fields', 'easy_chatgpt_access',
        'easy_language_selector',
        # Batch 9 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'easy_timesheet_add', 'ecommerce_barcode_search', 'ecommerce_quick_view',
        'edit_label', 'edit_order_date', 'education_fee',
        'education_university_management', 'email_id_validation',
        'employee_bonus_manager', 'employee_dynamic_fields',
        'employee_ideas', 'employee_late_check_in',
        'employee_less_working_hour_notification', 'employee_promotion_in_odoo',
        # Batch 10 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'employee_stages', 'equipment_request_it_operations', 'event_management',
        'event_ticket_qr_scanner', 'excel_report_designer', 'exchange_currency_rate',
        'expense_report_odoo', 'export_stockinfo_xls', 'export_view_pdf',
        'field_timepicker', 'fleet_complete_report', 'force_availability_in_stock',
        'fountain_widget_many2one', 'franchise_management',
        # Batch 11 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'generate_barcode_labels', 'gym_mgmt_system', 'hide_all_print_button',
        'hotel_management_odoo', 'hr_appraisal_custom_survey', 'hr_attendance_report_xlsx',
        'hr_employee_shift', 'hr_employee_updation', 'hr_holidays_report_xlsx',
        'hr_payroll_report_xlsx', 'hr_resignation', 'hr_timesheet_report_xlsx',
        'import_product_variant', 'invoice_report_xlsx',
        # Batch 12 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'freight_management_system', 'gatepass_slip', 'gender_contact',
        'google_search_in_odoo', 'hide_chatter', 'hide_cost_price',
        'hide_menu_user', 'hide_product_price_cost', 'hr_attendance_xlsx_report',
        'hr_disciplinary_tracking', 'hr_expense_mass_payment', 'hr_holidays_balance_report',
        'hr_hourly_payslip', 'hr_insurance'
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
