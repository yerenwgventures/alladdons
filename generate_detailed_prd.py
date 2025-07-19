#!/usr/bin/env python3
import json
import re

def create_detailed_module_description(module_data):
    """Create detailed, business-focused module description"""
    
    module_name = module_data['module_name']
    display_name = module_data['display_name']
    category = module_data['category']
    summary = module_data.get('summary', '')
    business_value = module_data.get('business_value', '')
    key_features = module_data.get('key_features', [])
    technical_scope = module_data.get('technical_scope', {})
    
    # Create comprehensive description based on module analysis
    descriptions = {
        'access_restriction_by_ip': 'Implements enterprise-grade security by restricting user login access to specific IP addresses. Administrators can define multiple allowed IP addresses per user, preventing unauthorized access from unknown locations. Features IP validation during login, security alerts for blocked attempts, and comprehensive audit trails.',

        'advanced_loan_management': 'Complete loan lifecycle management system covering loan applications, approval workflows, disbursement tracking, and repayment scheduling. Supports multiple loan types, interest calculations, amortization schedules, automated payment reminders, and comprehensive financial reporting for lending operations.',

        'pos_kitchen_screen_odoo': 'Digital kitchen display system for restaurants that shows real-time order information to kitchen staff. Orders are automatically displayed with preparation times, special instructions, and order priorities. Includes order status tracking, completion notifications, and integration with POS order flow.',

        'website_bargain': 'E-commerce negotiation platform allowing customers to propose alternative prices for products. Sellers can accept, reject, or counter-offer through automated workflows. Features price negotiation history, approval limits, notification systems, and integration with standard e-commerce checkout.',

        'dynamic_accounts_report': 'Advanced financial reporting engine with customizable report generation. Users can create dynamic profit & loss statements, balance sheets, cash flow reports, and trial balances with flexible date ranges, comparison periods, and drill-down capabilities for detailed analysis.',

        'hr_attendance_xlsx_report': 'Comprehensive attendance reporting system generating detailed Excel reports with employee attendance patterns, overtime calculations, late arrivals, early departures, and absence summaries. Includes graphical analysis and customizable report templates.',

        'inventory_barcode_scanning': 'Mobile-optimized barcode scanning solution for inventory operations. Supports product receiving, stock transfers, cycle counting, and inventory adjustments using smartphone cameras or dedicated scanners. Real-time stock updates with offline capability.',

        'project_task_risk_management_odoo': 'Project risk assessment and mitigation framework with risk identification, probability scoring, impact analysis, and mitigation planning. Includes risk registers, escalation procedures, and automated risk monitoring with dashboard reporting.',

        'website_product_customization': 'Product personalization platform allowing customers to customize products with options like colors, sizes, text, images, and configurations. Features real-time preview, pricing calculations, and integration with manufacturing workflows.',

        'crm_dashboard': 'Sales performance analytics dashboard providing real-time insights into lead conversion, sales pipeline, team performance, and revenue forecasting. Interactive charts, KPI tracking, and customizable widgets for sales management.',

        'manufacturing_timesheet': 'Production time tracking system linking employee timesheets to manufacturing orders. Tracks labor costs per product, efficiency metrics, overtime analysis, and integration with payroll systems for accurate cost accounting.',

        'vendor_portal_odoo': 'Supplier self-service portal enabling vendors to manage purchase orders, submit invoices, track payments, update product catalogs, and communicate with procurement teams. Includes document sharing and performance analytics.',

        'website_gdpr_odoo': 'GDPR compliance toolkit for websites including cookie consent management, privacy policy integration, data subject rights handling, and audit trails. Ensures legal compliance with European data protection regulations.',

        'multi_barcode_for_products': 'Product identification system supporting multiple barcode formats per product including UPC, EAN, Code128, and custom codes. Enables flexible product scanning across different sales channels and inventory systems.',

        'employee_promotion_in_odoo': 'Career advancement management system tracking employee promotions, salary adjustments, position changes, and approval workflows. Includes promotion history, eligibility criteria, and automated notification systems.',

        'base_accounting_kit': 'Complete accounting foundation providing essential financial management tools including chart of accounts, journal entries, bank reconciliation, tax management, and financial reporting. Serves as the core accounting framework for business operations.',

        'odoo_dynamic_dashboard': 'Customizable business intelligence platform allowing users to create personalized dashboards with drag-and-drop widgets, real-time KPIs, interactive charts, and automated data refresh. Supports role-based dashboard configurations.',

        'pos_face_recognition': 'Biometric customer identification system using facial recognition technology for POS operations. Enables contactless customer identification, loyalty program integration, and enhanced security for retail environments.',

        'hotel_management_odoo': 'Comprehensive hospitality management solution covering room reservations, guest check-in/out, housekeeping schedules, billing integration, and guest services. Includes front desk operations and revenue management tools.',

        'medical_lab_management': 'Healthcare laboratory information system managing patient samples, test orders, result reporting, and quality control. Features integration with medical equipment, automated reporting, and compliance tracking.',

        'franchise_management': 'Multi-location franchise operations platform managing franchise agreements, royalty calculations, performance monitoring, and standardized business processes across franchise networks.',

        'auto_database_backup': 'Automated database backup solution with scheduled backups, cloud storage integration, backup verification, and disaster recovery capabilities. Ensures business continuity and data protection.',

        'whatsapp_mail_messaging': 'Integrated communication platform combining WhatsApp messaging with email functionality. Enables customer communication through multiple channels with message history and automated responses.',

        'theme_autofly': 'Professional automotive industry website theme featuring car dealership layouts, vehicle showcase galleries, service booking systems, and responsive design optimized for automotive businesses.'
    }
    
    # Use specific description if available, otherwise generate one
    if module_name in descriptions:
        detailed_desc = descriptions[module_name]
    else:
        detailed_desc = generate_description_from_analysis(module_data)
    
    return detailed_desc

def generate_description_from_analysis(module_data):
    """Generate description based on technical analysis"""
    
    module_name = module_data['module_name']
    display_name = module_data['display_name']
    summary = module_data.get('summary', '')
    business_value = module_data.get('business_value', '')
    
    # Business context mapping
    context_map = {
        'pos': 'point of sale operations',
        'website': 'e-commerce and web functionality', 
        'hr': 'human resources management',
        'account': 'accounting and financial operations',
        'inventory': 'inventory and warehouse management',
        'project': 'project management and collaboration',
        'crm': 'customer relationship management',
        'purchase': 'procurement and vendor management',
        'sale': 'sales process optimization',
        'manufacturing': 'production and manufacturing operations',
        'report': 'business intelligence and reporting',
        'dashboard': 'performance monitoring and analytics',
        'theme': 'user interface and experience enhancement',
        'barcode': 'automated identification and tracking',
        'approval': 'workflow automation and governance'
    }
    
    # Identify primary business area
    primary_area = 'business process enhancement'
    for key, value in context_map.items():
        if key in module_name.lower():
            primary_area = value
            break
    
    # Build comprehensive description
    description_parts = []
    
    if summary:
        description_parts.append(f"Provides {summary.lower()}")
    else:
        description_parts.append(f"Enhances {primary_area}")
    
    if business_value:
        description_parts.append(f"Delivers {business_value.lower()}")
    
    # Add technical capabilities
    tech_scope = module_data.get('technical_scope', {})
    if tech_scope.get('has_controllers'):
        description_parts.append("includes web-based interfaces and API endpoints")
    
    if tech_scope.get('has_wizards'):
        description_parts.append("features guided step-by-step processes")
    
    if tech_scope.get('has_reports'):
        description_parts.append("provides comprehensive reporting capabilities")
    
    return ". ".join([part.capitalize() for part in description_parts]) + "."

def categorize_modules_business_focused(modules_data):
    """Organize modules by business function with detailed descriptions"""
    
    categories = {
        'Security & Access Control': [],
        'Financial Management & Accounting': [],
        'Sales & Customer Management': [],
        'Procurement & Vendor Management': [],
        'Inventory & Warehouse Operations': [],
        'Manufacturing & Production': [],
        'Human Resources & Payroll': [],
        'Point of Sale & Retail': [],
        'E-commerce & Website': [],
        'Project Management & Collaboration': [],
        'Business Intelligence & Reporting': [],
        'Communication & Messaging': [],
        'User Interface & Themes': [],
        'Industry-Specific Solutions': [],
        'Productivity & Automation Tools': []
    }
    
    # Categorization rules
    for module in modules_data:
        module_name = module['module_name'].lower()
        category = module.get('category', '').lower()
        display_name = module.get('display_name', '').lower()
        
        if any(x in module_name for x in ['access', 'security', 'login', 'password', 'restriction']):
            categories['Security & Access Control'].append(module)
        elif any(x in module_name for x in ['account', 'invoice', 'payment', 'financial', 'loan', 'budget']):
            categories['Financial Management & Accounting'].append(module)
        elif any(x in module_name for x in ['sale', 'crm', 'customer', 'quotation', 'lead']):
            categories['Sales & Customer Management'].append(module)
        elif any(x in module_name for x in ['purchase', 'vendor', 'supplier', 'procurement']):
            categories['Procurement & Vendor Management'].append(module)
        elif any(x in module_name for x in ['inventory', 'stock', 'warehouse', 'picking']):
            categories['Inventory & Warehouse Operations'].append(module)
        elif any(x in module_name for x in ['mrp', 'manufacturing', 'production', 'bom']):
            categories['Manufacturing & Production'].append(module)
        elif any(x in module_name for x in ['hr', 'employee', 'payroll', 'attendance']):
            categories['Human Resources & Payroll'].append(module)
        elif any(x in module_name for x in ['pos', 'point_of_sale']):
            categories['Point of Sale & Retail'].append(module)
        elif any(x in module_name for x in ['website', 'ecommerce', 'portal']):
            categories['E-commerce & Website'].append(module)
        elif any(x in module_name for x in ['project', 'task']):
            categories['Project Management & Collaboration'].append(module)
        elif any(x in module_name for x in ['report', 'dashboard', 'analytics']):
            categories['Business Intelligence & Reporting'].append(module)
        elif any(x in module_name for x in ['mail', 'message', 'discuss', 'chat']):
            categories['Communication & Messaging'].append(module)
        elif any(x in module_name for x in ['theme', 'backend']):
            categories['User Interface & Themes'].append(module)
        elif any(x in module_name for x in ['hotel', 'medical', 'education', 'gym', 'salon']):
            categories['Industry-Specific Solutions'].append(module)
        else:
            categories['Productivity & Automation Tools'].append(module)
    
    return categories

def generate_comprehensive_prd(modules_data):
    """Generate the comprehensive PRD document"""
    
    total_modules = len(modules_data)
    categories = categorize_modules_business_focused(modules_data)
    
    prd_content = f"""
# **COMPREHENSIVE PRODUCT REQUIREMENTS DOCUMENT (PRD)**
## **AllAddons - Complete Odoo 18 Business Enhancement Suite**

### **Executive Summary**
AllAddons represents the most comprehensive collection of Odoo 18 enhancements available, featuring **{total_modules} specialized modules** designed to transform standard Odoo into a complete enterprise business management platform. This suite addresses every aspect of modern business operations from security and compliance to advanced analytics and industry-specific workflows.

### **Project Overview**
- **Project Name**: AllAddons - Complete Odoo 18 Enhancement Suite
- **Total Modules**: {total_modules} custom modules
- **Target Platform**: Odoo 18.0 Community & Enterprise
- **Author**: CBMS TECHNOLOGIES LTD
- **Website**: https://www.mycbms.com
- **License**: Mixed (AGPL-3, LGPL-3 as per individual modules)

### **Business Value Proposition**
This comprehensive suite eliminates the need for multiple vendors by providing a single, integrated solution that enhances every Odoo module. Organizations can achieve complete digital transformation with advanced features for security, automation, reporting, and industry-specific requirements.

---

## **DETAILED MODULE CATALOG BY BUSINESS FUNCTION**

"""
    
    for category_name, modules in categories.items():
        if not modules:
            continue
            
        prd_content += f"\n### **{category_name.upper()} ({len(modules)} modules)**\n\n"
        
        for module in modules:
            display_name = module.get('display_name') or module['module_name'].replace('_', ' ').title()
            detailed_desc = create_detailed_module_description(module)
            business_value = module.get('business_value', 'Enhances operational efficiency')
            key_features = module.get('key_features', [])
            
            prd_content += f"#### **{display_name}**\n"
            prd_content += f"*Module: `{module['module_name']}`*\n\n"
            prd_content += f"**Description:** {detailed_desc}\n\n"
            prd_content += f"**Business Value:** {business_value}\n\n"
            
            if key_features:
                prd_content += f"**Key Features:**\n"
                for feature in key_features[:3]:  # Limit to top 3 features
                    prd_content += f"- {feature}\n"
                prd_content += "\n"
            
            prd_content += "---\n\n"
    
    return prd_content

def main():
    """Generate the comprehensive PRD"""
    
    with open('comprehensive_modules_data.json', 'r') as f:
        modules_data = json.load(f)
    
    prd_content = generate_comprehensive_prd(modules_data)
    
    with open('COMPREHENSIVE_PRD.md', 'w') as f:
        f.write(prd_content)
    
    print("Comprehensive PRD generated: COMPREHENSIVE_PRD.md")
    print(f"Total modules documented: {len(modules_data)}")

if __name__ == "__main__":
    main()
