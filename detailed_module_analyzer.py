#!/usr/bin/env python3
import os
import re
import json

def analyze_module_deeply(module_path):
    """Analyze module files to understand actual functionality"""
    module_name = os.path.basename(module_path)
    analysis = {
        'module_name': module_name,
        'manifest_info': {},
        'models': [],
        'views': [],
        'security': [],
        'data': [],
        'controllers': [],
        'wizards': [],
        'reports': [],
        'static_files': [],
        'functionality_keywords': set()
    }
    
    # Analyze manifest
    manifest_path = os.path.join(module_path, '__manifest__.py')
    if os.path.exists(manifest_path):
        analysis['manifest_info'] = extract_detailed_manifest(manifest_path)
    
    # Analyze directory structure and files
    for root, dirs, files in os.walk(module_path):
        rel_path = os.path.relpath(root, module_path)
        
        # Categorize by directory
        if 'models' in rel_path:
            analysis['models'].extend([f for f in files if f.endswith('.py')])
        elif 'views' in rel_path:
            analysis['views'].extend([f for f in files if f.endswith('.xml')])
        elif 'security' in rel_path:
            analysis['security'].extend(files)
        elif 'data' in rel_path:
            analysis['data'].extend([f for f in files if f.endswith('.xml')])
        elif 'controllers' in rel_path:
            analysis['controllers'].extend([f for f in files if f.endswith('.py')])
        elif 'wizard' in rel_path:
            analysis['wizards'].extend([f for f in files if f.endswith('.py')])
        elif 'report' in rel_path:
            analysis['reports'].extend(files)
        elif 'static' in rel_path:
            analysis['static_files'].extend(files)
    
    # Extract functionality keywords from file names and manifest
    all_text = ' '.join([
        analysis['manifest_info'].get('name', ''),
        analysis['manifest_info'].get('summary', ''),
        analysis['manifest_info'].get('description', ''),
        ' '.join(analysis['models']),
        ' '.join(analysis['views']),
        ' '.join(analysis['controllers']),
        ' '.join(analysis['wizards'])
    ]).lower()
    
    # Extract meaningful keywords
    keywords = extract_functionality_keywords(all_text, module_name)
    analysis['functionality_keywords'] = keywords
    
    return analysis

def extract_detailed_manifest(manifest_path):
    """Extract detailed manifest information"""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # More comprehensive regex patterns
        patterns = {
            'name': r"'name'\s*:\s*['\"]([^'\"]*?)['\"]",
            'summary': r"'summary'\s*:\s*['\"]([^'\"]*?)['\"]",
            'description': r"'description'\s*:\s*['\"]([^'\"]*?)['\"]",
            'category': r"'category'\s*:\s*['\"]([^'\"]*?)['\"]",
            'version': r"'version'\s*:\s*['\"]([^'\"]*?)['\"]",
            'author': r"'author'\s*:\s*['\"]([^'\"]*?)['\"]",
            'depends': r"'depends'\s*:\s*\[([^\]]*)\]",
            'data': r"'data'\s*:\s*\[([^\]]*)\]",
            'application': r"'application'\s*:\s*(True|False)"
        }
        
        result = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.DOTALL)
            if match:
                if key == 'depends' or key == 'data':
                    # Parse list items
                    items = re.findall(r"'([^']*)'", match.group(1))
                    result[key] = items
                else:
                    result[key] = match.group(1).strip()
            else:
                result[key] = '' if key not in ['depends', 'data'] else []
        
        return result
    except Exception as e:
        print(f"Error processing manifest {manifest_path}: {e}")
        return {}

def extract_functionality_keywords(text, module_name):
    """Extract meaningful functionality keywords"""
    # Business functionality keywords
    business_keywords = {
        'accounting': ['account', 'invoice', 'bill', 'payment', 'journal', 'ledger', 'financial', 'tax', 'vat'],
        'sales': ['sale', 'order', 'quotation', 'customer', 'crm', 'lead', 'opportunity'],
        'purchase': ['purchase', 'vendor', 'supplier', 'rfq', 'procurement'],
        'inventory': ['stock', 'warehouse', 'inventory', 'picking', 'delivery', 'transfer'],
        'manufacturing': ['mrp', 'bom', 'production', 'work_order', 'manufacturing'],
        'hr': ['employee', 'payroll', 'attendance', 'leave', 'timesheet'],
        'pos': ['pos', 'point_of_sale', 'receipt', 'payment_terminal'],
        'website': ['website', 'ecommerce', 'portal', 'blog', 'snippet'],
        'project': ['project', 'task', 'milestone', 'gantt'],
        'reporting': ['report', 'dashboard', 'analytics', 'chart', 'graph'],
        'workflow': ['approval', 'workflow', 'stage', 'state'],
        'communication': ['mail', 'message', 'notification', 'discuss', 'chat'],
        'security': ['access', 'permission', 'security', 'restriction', 'login'],
        'automation': ['cron', 'scheduler', 'automatic', 'batch', 'mass'],
        'integration': ['api', 'connector', 'import', 'export', 'sync'],
        'customization': ['custom', 'dynamic', 'configurable', 'wizard', 'template']
    }
    
    found_keywords = set()
    text_lower = text.lower()
    module_lower = module_name.lower()
    
    for category, keywords in business_keywords.items():
        for keyword in keywords:
            if keyword in text_lower or keyword in module_lower:
                found_keywords.add(category)
    
    return found_keywords

def main():
    """Analyze all modules in detail"""
    modules_analysis = []
    
    # Get all module directories
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.') and os.path.exists(os.path.join(item, '__manifest__.py')):
            print(f"Analyzing {item}...")
            analysis = analyze_module_deeply(item)
            modules_analysis.append(analysis)
    
    # Save detailed analysis
    with open('detailed_modules_analysis.json', 'w') as f:
        json.dump(modules_analysis, f, indent=2, default=list)
    
    print(f"Detailed analysis complete for {len(modules_analysis)} modules")
    print("Data saved to detailed_modules_analysis.json")

if __name__ == "__main__":
    main()
