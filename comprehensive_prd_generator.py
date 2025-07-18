#!/usr/bin/env python3
import os
import re
import json

def analyze_module_functionality(module_path):
    """Deeply analyze module to understand its actual business functionality"""
    module_name = os.path.basename(module_path)
    
    # Read manifest for basic info
    manifest_info = read_manifest(os.path.join(module_path, '__manifest__.py'))
    
    # Analyze models to understand data structures
    models_info = analyze_models(module_path)
    
    # Analyze views to understand UI functionality
    views_info = analyze_views(module_path)
    
    # Analyze controllers for web functionality
    controllers_info = analyze_controllers(module_path)
    
    # Generate comprehensive description
    description = generate_detailed_description(
        module_name, manifest_info, models_info, views_info, controllers_info
    )
    
    return {
        'module_name': module_name,
        'display_name': manifest_info.get('name', ''),
        'category': manifest_info.get('category', ''),
        'summary': manifest_info.get('summary', ''),
        'detailed_description': description,
        'business_value': extract_business_value(module_name, manifest_info, models_info),
        'key_features': extract_key_features(module_name, models_info, views_info),
        'technical_scope': {
            'models': len(models_info),
            'views': len(views_info),
            'has_controllers': len(controllers_info) > 0,
            'has_wizards': os.path.exists(os.path.join(module_path, 'wizard')),
            'has_reports': os.path.exists(os.path.join(module_path, 'report'))
        }
    }

def read_manifest(manifest_path):
    """Read and parse manifest file"""
    if not os.path.exists(manifest_path):
        return {}
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        patterns = {
            'name': r"'name'\s*:\s*['\"]([^'\"]*?)['\"]",
            'summary': r"'summary'\s*:\s*['\"]([^'\"]*?)['\"]",
            'description': r"'description'\s*:\s*['\"]([^'\"]*?)['\"]",
            'category': r"'category'\s*:\s*['\"]([^'\"]*?)['\"]",
            'depends': r"'depends'\s*:\s*\[([^\]]*)\]"
        }
        
        result = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.DOTALL)
            if match:
                if key == 'depends':
                    deps = re.findall(r"'([^']*)'", match.group(1))
                    result[key] = deps
                else:
                    result[key] = match.group(1).strip()
            else:
                result[key] = '' if key != 'depends' else []
        
        return result
    except Exception:
        return {}

def analyze_models(module_path):
    """Analyze model files to understand data structures"""
    models_path = os.path.join(module_path, 'models')
    models_info = []
    
    if not os.path.exists(models_path):
        return models_info
    
    for file in os.listdir(models_path):
        if file.endswith('.py') and file != '__init__.py':
            file_path = os.path.join(models_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract model classes and their purposes
                class_matches = re.findall(r'class\s+(\w+)\(.*?\):\s*"""([^"]*?)"""', content, re.DOTALL)
                for class_name, docstring in class_matches:
                    models_info.append({
                        'class_name': class_name,
                        'file': file,
                        'purpose': docstring.strip()
                    })
                
                # Extract _name attributes to understand model names
                name_matches = re.findall(r"_name\s*=\s*['\"]([^'\"]+)['\"]", content)
                for name in name_matches:
                    models_info.append({
                        'model_name': name,
                        'file': file
                    })
                    
            except Exception:
                continue
    
    return models_info

def analyze_views(module_path):
    """Analyze view files to understand UI functionality"""
    views_path = os.path.join(module_path, 'views')
    views_info = []
    
    if not os.path.exists(views_path):
        return views_info
    
    for file in os.listdir(views_path):
        if file.endswith('.xml'):
            file_path = os.path.join(views_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract view types and purposes
                view_types = re.findall(r'<field name="view_type">([^<]+)</field>', content)
                model_refs = re.findall(r'<field name="model">([^<]+)</field>', content)
                
                views_info.append({
                    'file': file,
                    'view_types': view_types,
                    'models': model_refs
                })
                    
            except Exception:
                continue
    
    return views_info

def analyze_controllers(module_path):
    """Analyze controller files for web functionality"""
    controllers_path = os.path.join(module_path, 'controllers')
    controllers_info = []
    
    if not os.path.exists(controllers_path):
        return controllers_info
    
    for file in os.listdir(controllers_path):
        if file.endswith('.py') and file != '__init__.py':
            file_path = os.path.join(controllers_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract route definitions
                routes = re.findall(r"@route\(['\"]([^'\"]+)['\"]", content)
                controllers_info.extend(routes)
                    
            except Exception:
                continue
    
    return controllers_info

def generate_detailed_description(module_name, manifest_info, models_info, views_info, controllers_info):
    """Generate comprehensive business-focused description"""
    
    # Module name analysis for business context
    name_keywords = {
        'access': 'security and access control',
        'restriction': 'access restrictions and limitations',
        'ip': 'IP address management',
        'loan': 'financial loan management',
        'payment': 'payment processing',
        'invoice': 'invoicing and billing',
        'pos': 'point of sale operations',
        'website': 'website and e-commerce functionality',
        'report': 'reporting and analytics',
        'dashboard': 'business intelligence dashboards',
        'theme': 'user interface themes',
        'barcode': 'barcode scanning and management',
        'inventory': 'inventory and stock management',
        'manufacturing': 'production and manufacturing',
        'hr': 'human resources management',
        'project': 'project management',
        'crm': 'customer relationship management',
        'purchase': 'procurement and purchasing',
        'sale': 'sales management',
        'account': 'accounting and finance'
    }
    
    # Identify primary business function
    primary_function = "business process enhancement"
    for keyword, description in name_keywords.items():
        if keyword in module_name.lower():
            primary_function = description
            break
    
    # Build description based on analysis
    description_parts = []
    
    # Start with primary function
    description_parts.append(f"Provides comprehensive {primary_function}")
    
    # Add model-based functionality
    if models_info:
        model_purposes = [m.get('purpose', '') for m in models_info if m.get('purpose')]
        if model_purposes:
            description_parts.append(f"Features include {', '.join(model_purposes[:3])}")
    
    # Add web functionality if controllers exist
    if controllers_info:
        description_parts.append("Includes web-based interfaces and API endpoints")
    
    # Add UI enhancements if views exist
    if views_info:
        description_parts.append("Provides enhanced user interface components")
    
    return ". ".join(description_parts) + "."

def extract_business_value(module_name, manifest_info, models_info):
    """Extract clear business value proposition"""
    
    value_mapping = {
        'access_restriction': 'Enhanced security through IP-based access control',
        'loan_management': 'Complete loan lifecycle management from application to repayment',
        'pos': 'Improved point of sale efficiency and customer experience',
        'dashboard': 'Real-time business insights and performance monitoring',
        'report': 'Advanced reporting capabilities for data-driven decisions',
        'invoice': 'Streamlined billing and payment collection processes',
        'inventory': 'Optimized stock management and warehouse operations',
        'website': 'Enhanced online presence and e-commerce capabilities',
        'theme': 'Professional and modern user interface design',
        'hr': 'Improved human resource management and employee engagement'
    }
    
    for key, value in value_mapping.items():
        if key in module_name.lower():
            return value
    
    return "Enhances operational efficiency and user experience"

def extract_key_features(module_name, models_info, views_info):
    """Extract key features based on technical analysis"""
    features = []
    
    # Feature extraction based on models
    model_names = [m.get('model_name', '') for m in models_info if m.get('model_name')]
    
    feature_patterns = {
        'approval': 'Multi-level approval workflows',
        'wizard': 'Guided step-by-step processes',
        'report': 'Comprehensive reporting tools',
        'dashboard': 'Interactive dashboard views',
        'import': 'Data import capabilities',
        'export': 'Data export functionality',
        'email': 'Email integration and notifications',
        'sms': 'SMS communication features',
        'barcode': 'Barcode scanning support',
        'qr': 'QR code generation and scanning'
    }
    
    for pattern, feature in feature_patterns.items():
        if any(pattern in name.lower() for name in model_names + [module_name]):
            features.append(feature)
    
    return features[:5]  # Limit to top 5 features

def main():
    """Generate comprehensive PRD with detailed descriptions"""
    modules_data = []
    
    print("Analyzing modules for comprehensive PRD...")
    
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.') and os.path.exists(os.path.join(item, '__manifest__.py')):
            print(f"Analyzing {item}...")
            analysis = analyze_module_functionality(item)
            modules_data.append(analysis)
    
    # Save comprehensive analysis
    with open('comprehensive_modules_data.json', 'w') as f:
        json.dump(modules_data, f, indent=2)
    
    print(f"Comprehensive analysis complete for {len(modules_data)} modules")
    print("Data saved to comprehensive_modules_data.json")

if __name__ == "__main__":
    main()
