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
        'hr_hourly_payslip', 'hr_insurance',
        # Batch 13 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'hr_leave_dashboard', 'hue_backend_theme', 'image_capture_upload_widget',
        'import_lots', 'import_partner_employee_image', 'import_template_download',
        'import_user_excel', 'index_and_follow', 'inventory_barcode_scanning',
        'inventory_forecast_analysis_report', 'inventory_move_mini_dashboard',
        'inventory_report_generator', 'hr_zk_attendance', 'import_bill_of_materials_in_mrp',
        # Batch 14 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'inventory_stock_dashboard_odoo', 'inventory_turnover_report_analysis',
        'invoice_bill_select_orderlines', 'invoice_design', 'invoice_format_editor',
        'invoice_multi_approval', 'invoice_stock_move', 'jazzy_backend_theme',
        'lang_switch_pos', 'list_tree_pin_records', 'listview_change_background_color',
        'laundry_management', 'legal_case_management', 'legal_case_management_dashboard',
        # Batch 15 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'login_as_any_user', 'login_pos_direct', 'login_to_checkout',
        'login_user_detail', 'low_sale_report', 'low_stocks_product_alert',
        'lunch_order_pdf', 'magic_note', 'mail_message_access',
        'mail_to_child_contact', 'mandatory_field_highlight', 'manufacturing_timesheet',
        'mass_price_update', 'master_search',
        # Batch 16 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'master_search_systray', 'membership_card_odoo', 'merge_picking_orders',
        'merge_rfq', 'model_viewer_widget', 'monday_odoo_connector',
        'mrp_order_from_multiple_sale_order', 'mrp_product_kanban', 'mrp_work_order_print',
        'multi_barcode_for_products', 'multi_image_in_pos', 'multi_pricelist',
        'medical_lab_management', 'mobile_service_shop',
        # Batch 17 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'multicolor_backend_theme', 'multiple_reference_per_product', 'odoo_accounting_dashboard',
        'odoo_calculator_tool', 'odoo_chatgpt_connector', 'odoo_contact_approval',
        'odoo_dynamic_dashboard', 'odoo_google_contact_integration', 'odoo_google_meet_integration',
        'odoo_health_report', 'odoo_parking_management', 'odoo_picking_order_line_views',
        'odoo_product_tags', 'odoo_read_messages',
        # Batch 18 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'odoo_readonly_user', 'odoo_rental_sales', 'odoo_sale_order_line_views',
        'odoo_selection_field_configurator', 'odoo_twilio_sms', 'odoo_website_helpdesk',
        'odoo_website_helpdesk_dashboard', 'ohrms_service_request', 'one2many_duplicate_record_widget',
        'one2many_excel_report', 'one2many_mass_select_delete', 'openai_odoo_base',
        'openai_product_images', 'openai_product_tag_descrption',
        # Batch 19 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'openai_website_product_media', 'orange_theme_odoo12', 'order_invoice_manual_link',
        'order_line_sequences', 'pantry_payroll', 'partner_emails_history',
        'partner_related_user', 'partner_search_by_number', 'password_hint',
        'password_reset_manager', 'payment_proof_attachment', 'payment_status_in_sale',
        'pdf_report_action', 'pdf_report_password_protection',
        # Batch 20 - 14/15 successful (dynamic_product_label_print still has DB schema issue)
        'pdf_report_with_sign', 'pdf_report_with_watermark', 'personal_organiser',
        'pip_installer', 'point_of_sale_logo', 'portal_stock_check',
        'pos_all_orders', 'pos_alternative_products', 'pos_analysis_report',
        'pos_category_wise_receipt', 'pos_chatter', 'pos_controlled_interface',
        'pos_custom_percentage_tip_fixed', 'pos_customer_feedback',
        # Batch 21 - 14/15 successful (dynamic_product_label_print still has DB schema issue)
        'pos_delete_orderline', 'pos_face_recognition', 'pos_idle_time_session_lock',
        'pos_kitchen_screen_odoo', 'pos_magnify_image', 'pos_mrp_order',
        'pos_night_mode', 'pos_numpad_show_hide', 'pos_order_line_image',
        'pos_order_line_mass_edit', 'pos_orderline_items_count', 'pos_orderline_search',
        'pos_pro_cross_selling', 'pos_product_limit_odoo',
        # Batch 22 - 14/15 successful (dynamic_product_label_print still has DB schema issue)
        'pos_product_stock', 'pos_products_based_on_time', 'pos_receipt_extend',
        'pos_refund_password', 'pos_report_generator', 'pos_restrict',
        'pos_screen_pane_position', 'pos_takeaway', 'pos_theme_sapphire',
        'pos_zero_quantity_restrict', 'pricelist_price_on_product', 'print_minutes_of_meeting',
        'product_360_degree_view_in_website', 'product_approval_management',
        # Batch 23 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'product_barcode', 'product_batch_report', 'product_brand_ecommerce',
        'product_brand_inventory', 'product_brand_purchase', 'product_brand_sale',
        'product_combo_pack', 'product_deletion', 'product_detail_search',
        'product_discount_limit', 'product_export_with_images', 'product_image_list_view',
        'product_image_suggestion', 'product_import',
        # Batch 24 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'product_internal_ref_generator', 'product_management_app', 'product_multi_attachment',
        'product_multi_uom', 'product_multi_vendor_update', 'product_nutrition_allergen',
        'product_price_update_advanced', 'product_restriction_users', 'product_sales_by_location',
        'product_stock_details', 'product_to_invoice', 'product_variant_import',
        'product_volume', 'product_web_hover',
        # Batch 25 - 14/15 successful after fixes (dynamic_product_label_print still has DB schema issue)
        'product_wise_shipping_method', 'products_to_transfer', 'profit_and_loss_pdf_report',
        'progress_billing', 'project_by_phases', 'project_dashboard_odoo',
        'project_dynamic_fields', 'project_progress_bar', 'project_report_pdf',
        'project_task_access', 'project_task_attachments', 'project_task_risk_management_odoo',
        'project_task_unique_code', 'project_website_kanban_view',
        # Batch 26 - 12/15 successful (3 modules need fixes)
        'projects_task_checklists', 'psql_query_execute', 'purchase_down_payment',
        'purchase_line_views', 'purchase_order_delivery_status', 'purchase_product_configurator',
        'purchase_product_history', 'purchase_recurring_orders', 'purchase_requisition_project_task',
        'quick_rfq', 'quotation_customer_followup', 'recurring_of_activities',
        # Batch 27 - 12/15 successful (3 modules need fixes - same failed modules)
        'remove_studio_field', 'report_attachment_preview', 'reset_journal_entries',
        'rest_api_odoo', 'restrict_delivery_method', 'restrict_pricelist_user',
        'restrict_web_debug', 'return_invoice_bill', 'sale_customer_product_history',
        'sale_delivery_address', 'sale_discount_total', 'sale_invoice_detail',
        # Batch 28 - 11/15 successful (4 modules need fixes)
        'sale_invoice_due_date_reminder', 'sale_mini_dashboard', 'sale_order_line_multi_warehouse',
        'sale_product_image', 'sale_purchase_automated', 'sale_purchase_from_product',
        'sale_purchase_previous_product_cost', 'sale_recurring', 'sale_report_advanced',
        'sale_report_format_editor', 'sale_report_generator',
        # Batch 29 - 9/15 successful (6 modules need fixes)
        'sale_stock_restrict', 'sales_person_signature', 'sales_product_performance_report',
        'sales_target_vs_achievement', 'sales_team_access_controls', 'salesperson_pos_order_line',
        'schedule_activity_to_multiple_users', 'schedule_survey', 'scheduled_action_shortcut',
        # Batch 30 - 9/15 successful (6 modules need fixes - same failed modules)
        'section_wise_subtotal', 'separate_quotation_number_odoo', 'sequence_opportunity_crm',
        'serial_no_from_mo', 'shopping_through_agent', 'signup_with_twilio',
        'simple_mrp_order', 'size_restriction_for_attachments', 'smart_alert_warning',
        # Batch 31 - 9/15 successful (6 modules need fixes - same failed modules)
        'so_bom_selection', 'special_product_snippet', 'split_mrp_order',
        'statement_report', 'sticky_pivot_view', 'stock_intercompany_transfer',
        'stock_last_purchase_price', 'stock_move_invoice', 'stock_transfer_in_pos',
        # Batch 32 - 7/15 successful (8 modules need fixes - 2 new failures)
        'subscription_package', 'substitute_product_in_mrp', 'survey_question_duplicator',
        'systray_menu_favourites', 'table_reservation_in_pos', 'task_deadline_reminder',
        'task_overdue_email_odoo'
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
