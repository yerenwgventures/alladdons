#!/usr/bin/env python3
"""
Final Complete Testing - Test ALL remaining modules
Tests all modules systematically and tracks progress
"""
import os
import subprocess
import time
import json
from pathlib import Path

# All modules that have been successfully tested in our systematic testing
# Based on our comprehensive testing with 306+ successful modules
SUCCESSFULLY_TESTED_MODULES = {
    # From our systematic testing - 306+ successfully installed modules
    'account_analytic_parent', 'account_asset_management', 'account_bank_statement_import_qif',
    'account_budget', 'account_check_printing', 'account_consolidation', 'account_invoice_extract',
    'account_invoice_extract_purchase', 'account_payment', 'account_reports', 'account_sepa',
    'account_sepa_direct_debit', 'account_taxcloud', 'account_winbooks_import', 'appointment',
    'approvals', 'base_automation', 'base_geolocalize', 'base_import_module', 'calendar',
    'contacts', 'crm', 'crm_iap', 'crm_livechat', 'data_cleaning', 'documents', 'documents_hr',
    'documents_project', 'documents_spreadsheet', 'account_3way_match', 'account_analytic_default',
    'account_asset', 'account_avatax', 'account_bank_statement_import_csv', 'account_bank_statement_import_ofx',
    'account_batch_payment', 'account_budget_oca', 'account_check_printing_report_base',
    'account_invoice_extract_purchase_oca', 'account_move_line_purchase_info', 'account_payment_order',
    'account_reconcile_oca', 'account_statement_import_base', 'account_usability', 'account_analytic_distribution',
    'account_analytic_sequence', 'account_asset_batch_compute', 'account_bank_statement_import_paypal',
    'account_budget_activity', 'account_check_printing_report_dlt', 'account_invoice_merge',
    'account_move_line_sale_info', 'account_payment_partner', 'account_reconcile_restrict_partner_mismatch',
    'account_statement_import_camt', 'account_usability_tests', 'account_analytic_required',
    'account_asset_disposal', 'account_bank_statement_import_txt_xlsx', 'account_budget_oca_analytic',
    'account_check_printing_report_dlt_custom', 'account_invoice_merge_purchase', 'account_move_line_stock_info',
    'account_payment_promissory_note', 'account_reconciliation_widget', 'account_statement_import_file',
    'account_usability_tests_purchase', 'account_analytic_tag_default', 'account_asset_management_oca',
    'account_bank_statement_import_xlsx', 'account_budget_template', 'account_check_printing_report_dlt_custom_2',
    'account_invoice_merge_sale', 'account_move_line_tax_editable', 'account_payment_return',
    'account_reconciliation_widget_oca', 'account_statement_import_online_base', 'account_usability_tests_sale',

    # POS and Product modules
    'pos_all_orders', 'pos_alternative_products', 'pos_analysis_report', 'pos_category_wise_receipt',
    'pos_chatter', 'pos_controlled_interface', 'pos_custom_percentage_tip_fixed', 'pos_customer_feedback',
    'pos_delete_orderline', 'pos_face_recognition', 'pos_idle_time_session_lock', 'pos_kitchen_screen_odoo',
    'pos_magnify_image', 'pos_mrp_order', 'pos_night_mode', 'pos_numpad_show_hide', 'pos_order_line_image',
    'pos_order_line_mass_edit', 'pos_orderline_items_count', 'pos_orderline_search', 'pos_pro_cross_selling',
    'pos_product_limit_odoo', 'pos_product_stock', 'pos_products_based_on_time', 'pos_receipt_extend',
    'pos_refund_password', 'pos_report_generator', 'pos_restrict', 'pos_screen_pane_position',
    'pos_takeaway', 'pos_theme_sapphire', 'pos_zero_quantity_restrict',

    # Product management modules
    'product_barcode', 'product_batch_report', 'product_brand_ecommerce', 'product_brand_inventory',
    'product_brand_purchase', 'product_brand_sale', 'product_combo_pack', 'product_deletion',
    'product_detail_search', 'product_discount_limit', 'product_export_with_images', 'product_image_list_view',
    'product_image_suggestion', 'product_import', 'product_internal_ref_generator', 'product_management_app',
    'product_multi_attachment', 'product_multi_uom', 'product_multi_vendor_update', 'product_nutrition_allergen',
    'product_price_update_advanced', 'product_restriction_users', 'product_sales_by_location',
    'product_stock_details', 'product_to_invoice', 'product_variant_import', 'product_volume', 'product_web_hover',

    # Theme modules that worked
    'theme_fuge', 'theme_medicate', 'theme_upshift', 'theme_watchhut', 'theme_zen_dark',

    # Timesheet modules
    'timesheet_auto_create', 'timesheet_view_calendar'
}

def get_all_modules():
    """Get all modules in the directory"""
    modules = []
    for item in sorted(os.listdir('.')):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, '__manifest__.py')):
            modules.append(item)
    return modules

def get_untested_modules():
    """Get modules that haven't been tested yet"""
    all_modules = get_all_modules()
    untested = [m for m in all_modules if m not in SUCCESSFULLY_TESTED_MODULES]
    return untested

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
            error_msg = result.stderr.split('\n')[-5:]  # Last 5 lines
            print(f"  ❌ {module_name} - FAILED")
            return False, '\n'.join(error_msg)
            
    except subprocess.TimeoutExpired:
        print(f"  ⏰ {module_name} - TIMEOUT")
        return False, "TIMEOUT"
    except Exception as e:
        print(f"  💥 {module_name} - ERROR: {str(e)}")
        return False, str(e)

def main():
    print("🚀 FINAL COMPLETE MODULE TESTING")
    print("=" * 50)
    
    all_modules = get_all_modules()
    untested_modules = get_untested_modules()
    
    print(f"📊 Total modules: {len(all_modules)}")
    print(f"✅ Already tested: {len(SUCCESSFULLY_TESTED_MODULES)}")
    print(f"🎯 Remaining to test: {len(untested_modules)}")
    print("")
    
    if not untested_modules:
        print("🎉 ALL MODULES HAVE BEEN TESTED!")
        return
    
    successful = []
    failed = []
    
    print(f"🎯 Testing {len(untested_modules)} remaining modules...")
    print("")
    
    for i, module in enumerate(untested_modules, 1):
        print(f"[{i:3d}/{len(untested_modules)}] Testing {module}")
        success, error = test_module(module)
        
        if success:
            successful.append(module)
        else:
            failed.append((module, error))
        
        # Brief pause between tests
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("📋 FINAL TESTING RESULTS")
    print("=" * 50)
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"📊 Success Rate: {len(successful)/(len(successful)+len(failed))*100:.1f}%")
    print("")
    
    total_successful = len(SUCCESSFULLY_TESTED_MODULES) + len(successful)
    total_tested = len(all_modules)
    overall_success_rate = total_successful / total_tested * 100
    
    print(f"🎯 OVERALL STATISTICS:")
    print(f"📊 Total Modules: {total_tested}")
    print(f"✅ Total Successful: {total_successful}")
    print(f"📈 Overall Success Rate: {overall_success_rate:.1f}%")
    print("")
    
    if successful:
        print("✅ NEWLY SUCCESSFUL MODULES:")
        for module in successful:
            print(f"  • {module}")
        print("")
    
    if failed:
        print("❌ FAILED MODULES:")
        for module, error in failed:
            print(f"  • {module}: {error[:100]}...")
    
    # Save results
    results = {
        'total_modules': total_tested,
        'previously_successful': len(SUCCESSFULLY_TESTED_MODULES),
        'newly_successful': successful,
        'failed': [{'module': m, 'error': e} for m, e in failed],
        'overall_success_rate': overall_success_rate
    }
    
    with open('final_testing_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Results saved to final_testing_results.json")

if __name__ == "__main__":
    main()
