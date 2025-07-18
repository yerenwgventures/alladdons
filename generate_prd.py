#!/usr/bin/env python3
import json
import re

def clean_text(text):
    """Clean and format text for PRD"""
    if not text:
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove common technical phrases
    text = re.sub(r'This module\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Module\s*', '', text, flags=re.IGNORECASE)
    return text.strip()

def categorize_modules(categories):
    """Reorganize modules into logical business categories"""
    business_categories = {
        'Accounting & Finance': [],
        'Sales & CRM': [],
        'Purchase & Procurement': [],
        'Inventory & Warehouse': [],
        'Manufacturing & Production': [],
        'Human Resources': [],
        'Point of Sale': [],
        'Website & E-commerce': [],
        'Project Management': [],
        'Backend Themes': [],
        'Productivity & Tools': [],
        'Industry Specific': [],
        'Communication & Messaging': [],
        'Reporting & Analytics': []
    }
    
    # Mapping rules
    for cat_name, modules in categories.items():
        cat_lower = cat_name.lower()
        
        for module in modules:
            if not module.get('name'):
                continue
                
            # Categorization logic
            if any(x in cat_lower for x in ['accounting', 'account']):
                business_categories['Accounting & Finance'].append(module)
            elif any(x in cat_lower for x in ['sales', 'sale', 'crm']):
                business_categories['Sales & CRM'].append(module)
            elif any(x in cat_lower for x in ['purchase', 'purchases']):
                business_categories['Purchase & Procurement'].append(module)
            elif any(x in cat_lower for x in ['warehouse', 'inventory', 'stock']):
                business_categories['Inventory & Warehouse'].append(module)
            elif any(x in cat_lower for x in ['manufacturing', 'manufcturing', 'mrp']):
                business_categories['Manufacturing & Production'].append(module)
            elif any(x in cat_lower for x in ['human resource', 'hr']):
                business_categories['Human Resources'].append(module)
            elif any(x in cat_lower for x in ['point of sale', 'pos']):
                business_categories['Point of Sale'].append(module)
            elif any(x in cat_lower for x in ['website', 'ecommerce', 'theme']):
                if 'theme' in cat_lower and 'backend' not in cat_lower:
                    business_categories['Website & E-commerce'].append(module)
                elif 'backend' in cat_lower or 'theme' in module.get('name', '').lower():
                    business_categories['Backend Themes'].append(module)
                else:
                    business_categories['Website & E-commerce'].append(module)
            elif any(x in cat_lower for x in ['project']):
                business_categories['Project Management'].append(module)
            elif any(x in cat_lower for x in ['discuss', 'mail', 'message']):
                business_categories['Communication & Messaging'].append(module)
            elif any(x in cat_lower for x in ['industries', 'services']):
                business_categories['Industry Specific'].append(module)
            elif any(x in module.get('name', '').lower() for x in ['report', 'dashboard', 'analytic']):
                business_categories['Reporting & Analytics'].append(module)
            else:
                business_categories['Productivity & Tools'].append(module)
    
    return business_categories

def generate_prd(data):
    """Generate comprehensive PRD"""
    
    prd = f"""
# **HARMONIZED PRODUCT REQUIREMENTS DOCUMENT (PRD)**
## **AllAddons - Comprehensive Odoo 18 Module Collection**

### **Project Overview**
- **Project Name**: AllAddons - Complete Odoo 18 Enhancement Suite
- **Total Modules**: {data['total_modules']} custom modules
- **Target Platform**: Odoo 18.0 Community & Enterprise
- **Author**: CBMS TECHNOLOGIES LTD
- **Website**: https://www.mycbms.com
- **License**: Mixed (AGPL-3, LGPL-3 as per individual modules)

### **Executive Summary**
This comprehensive collection provides {data['total_modules']} specialized Odoo modules designed to enhance every aspect of business operations. From advanced accounting features to sophisticated e-commerce themes, this suite transforms standard Odoo into a powerful, feature-rich business management platform.

---

## **MODULE CATALOG BY BUSINESS FUNCTION**

"""
    
    business_categories = categorize_modules(data['categories'])
    
    for category, modules in business_categories.items():
        if not modules:
            continue
            
        prd += f"\n### **{category.upper()} ({len(modules)} modules)**\n\n"
        
        for module in modules:
            name = module.get('name', module.get('module_name', 'Unknown'))
            summary = clean_text(module.get('summary', ''))
            description = clean_text(module.get('description', ''))
            
            # Create feature description
            feature_desc = summary or description or "Enhances Odoo functionality"
            if len(feature_desc) > 150:
                feature_desc = feature_desc[:147] + "..."
            
            prd += f"**{name}**\n"
            prd += f"- *Features*: {feature_desc}\n"
            prd += f"- *Module*: `{module.get('module_name')}`\n\n"
    
    return prd

def main():
    with open('modules_data.json', 'r') as f:
        data = json.load(f)
    
    prd_content = generate_prd(data)
    
    with open('HARMONIZED_PRD.md', 'w') as f:
        f.write(prd_content)
    
    print("Harmonized PRD generated: HARMONIZED_PRD.md")
    print(f"Total modules cataloged: {data['total_modules']}")

if __name__ == "__main__":
    main()
