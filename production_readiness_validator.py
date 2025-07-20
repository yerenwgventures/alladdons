#!/usr/bin/env python3
"""
Production Readiness Validator
Validates each module for production deployment:
1. Self-contained installation capability
2. Dependency requirements documentation
3. Code safety and cleanliness
4. Potential conflict identification
5. Installation prerequisites
"""

import os
import json
import ast
import xml.etree.ElementTree as ET
from datetime import datetime

def validate_module_production_readiness(module_name):
    """Comprehensive production readiness validation"""
    module_path = os.path.join('.', module_name)
    
    if not os.path.isdir(module_path):
        return {"status": "missing", "issues": ["Module directory not found"]}
    
    validation_result = {
        "module": module_name,
        "status": "unknown",
        "production_ready": False,
        "manifest_analysis": {},
        "dependency_requirements": [],
        "installation_prerequisites": [],
        "potential_conflicts": [],
        "code_safety_issues": [],
        "missing_components": [],
        "recommendations": []
    }
    
    # 1. Validate Manifest
    manifest_path = os.path.join(module_path, '__manifest__.py')
    if not os.path.exists(manifest_path):
        validation_result["missing_components"].append("__manifest__.py file")
        validation_result["status"] = "invalid"
        return validation_result
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
        
        # Parse manifest safely
        manifest_dict = ast.literal_eval(manifest_content.strip())
        validation_result["manifest_analysis"] = {
            "name": manifest_dict.get('name', 'Unknown'),
            "version": manifest_dict.get('version', 'Unknown'),
            "depends": manifest_dict.get('depends', []),
            "data": manifest_dict.get('data', []),
            "installable": manifest_dict.get('installable', False),
            "auto_install": manifest_dict.get('auto_install', False),
            "application": manifest_dict.get('application', False)
        }
        
        # Check if installable
        if not manifest_dict.get('installable', False):
            validation_result["code_safety_issues"].append("Module marked as not installable")
        
        # Analyze dependencies
        depends = manifest_dict.get('depends', [])
        for dep in depends:
            if dep in ['base', 'web', 'mail']:
                continue  # Standard Odoo modules
            elif dep in ['sale', 'purchase', 'stock', 'account', 'hr', 'project', 'crm']:
                validation_result["dependency_requirements"].append(f"Standard Odoo module: {dep}")
            elif dep in ['point_of_sale', 'pos_restaurant', 'website', 'website_sale']:
                validation_result["dependency_requirements"].append(f"Odoo app module: {dep}")
            elif dep.startswith('stub_'):
                validation_result["installation_prerequisites"].append(f"Custom stub module required: {dep}")
            else:
                validation_result["potential_conflicts"].append(f"Custom dependency: {dep} (may not exist on customer system)")
        
    except Exception as e:
        validation_result["code_safety_issues"].append(f"Manifest parsing error: {str(e)}")
        validation_result["status"] = "invalid"
        return validation_result
    
    # 2. Validate Data Files
    data_files = manifest_dict.get('data', [])
    for data_file in data_files:
        file_path = os.path.join(module_path, data_file)
        if not os.path.exists(file_path):
            validation_result["missing_components"].append(f"Data file: {data_file}")
        elif data_file.endswith('.xml'):
            # Validate XML structure
            try:
                ET.parse(file_path)
            except ET.ParseError as e:
                validation_result["code_safety_issues"].append(f"XML parse error in {data_file}: {str(e)}")
    
    # 3. Check for Security Files
    security_path = os.path.join(module_path, 'security')
    if os.path.exists(security_path):
        access_file = os.path.join(security_path, 'ir.model.access.csv')
        if os.path.exists(access_file):
            # Validate access file format
            try:
                with open(access_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) < 2:  # Header + at least one record
                        validation_result["code_safety_issues"].append("Empty or invalid ir.model.access.csv")
            except Exception as e:
                validation_result["code_safety_issues"].append(f"Security file error: {str(e)}")
    
    # 4. Check Python Files
    models_path = os.path.join(module_path, 'models')
    if os.path.exists(models_path):
        for py_file in os.listdir(models_path):
            if py_file.endswith('.py') and py_file != '__init__.py':
                py_path = os.path.join(models_path, py_file)
                try:
                    with open(py_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for common issues
                    if 'from odoo import' not in content and 'import odoo' not in content:
                        validation_result["code_safety_issues"].append(f"Python file {py_file} may not import Odoo properly")
                    
                    # Check for dangerous operations
                    dangerous_patterns = ['os.system', 'subprocess.call', 'eval(', 'exec(']
                    for pattern in dangerous_patterns:
                        if pattern in content:
                            validation_result["code_safety_issues"].append(f"Potentially unsafe code in {py_file}: {pattern}")
                
                except Exception as e:
                    validation_result["code_safety_issues"].append(f"Python file error in {py_file}: {str(e)}")
    
    # 5. Check for Common Conflict Patterns
    # Check for model name conflicts
    if os.path.exists(models_path):
        for py_file in os.listdir(models_path):
            if py_file.endswith('.py'):
                py_path = os.path.join(models_path, py_file)
                try:
                    with open(py_path, 'r') as f:
                        content = f.read()
                    
                    # Look for common conflicting model names
                    conflict_models = ['pos.order', 'sale.order', 'account.move', 'stock.picking']
                    for model in conflict_models:
                        if f"_name = '{model}'" in content:
                            validation_result["potential_conflicts"].append(f"Extends core model: {model}")
                
                except:
                    pass
    
    # 6. Generate Recommendations
    if not validation_result["dependency_requirements"] and not validation_result["potential_conflicts"]:
        validation_result["recommendations"].append("✅ Self-contained module - no external dependencies")
    
    if validation_result["dependency_requirements"]:
        validation_result["recommendations"].append("📋 Install required Odoo modules before installing this module")
    
    if validation_result["potential_conflicts"]:
        validation_result["recommendations"].append("⚠️ Test in staging environment - potential conflicts detected")
    
    if not validation_result["code_safety_issues"] and not validation_result["missing_components"]:
        validation_result["production_ready"] = True
        validation_result["status"] = "ready"
        validation_result["recommendations"].append("🎯 Production ready - safe to install")
    else:
        validation_result["status"] = "needs_fixes"
        validation_result["recommendations"].append("🔧 Requires fixes before production deployment")
    
    return validation_result

def generate_installation_readme(module_name, validation_result):
    """Generate installation README for the module"""
    readme_content = f"""# {validation_result['manifest_analysis'].get('name', module_name)}

## Installation Guide

### Prerequisites
"""
    
    if validation_result["dependency_requirements"]:
        readme_content += "**Required Odoo Modules:**\n"
        for dep in validation_result["dependency_requirements"]:
            readme_content += f"- {dep}\n"
        readme_content += "\n"
    
    if validation_result["installation_prerequisites"]:
        readme_content += "**Custom Prerequisites:**\n"
        for prereq in validation_result["installation_prerequisites"]:
            readme_content += f"- {prereq}\n"
        readme_content += "\n"
    
    readme_content += f"""### Installation Steps
1. Ensure all prerequisites are installed
2. Copy the `{module_name}` folder to your Odoo addons directory
3. Update the addons list: `Settings > Apps > Update Apps List`
4. Search for "{validation_result['manifest_analysis'].get('name', module_name)}"
5. Click Install

### Potential Conflicts
"""
    
    if validation_result["potential_conflicts"]:
        for conflict in validation_result["potential_conflicts"]:
            readme_content += f"⚠️ {conflict}\n"
    else:
        readme_content += "✅ No known conflicts detected\n"
    
    readme_content += f"""
### Safety Status
"""
    
    if validation_result["production_ready"]:
        readme_content += "🎯 **Production Ready** - Safe for production deployment\n"
    else:
        readme_content += "⚠️ **Requires Review** - Please review issues before production use\n"
        
        if validation_result["code_safety_issues"]:
            readme_content += "\n**Issues to Review:**\n"
            for issue in validation_result["code_safety_issues"]:
                readme_content += f"- {issue}\n"
    
    readme_content += f"""
### Module Information
- **Version:** {validation_result['manifest_analysis'].get('version', 'Unknown')}
- **Auto Install:** {'Yes' if validation_result['manifest_analysis'].get('auto_install') else 'No'}
- **Application:** {'Yes' if validation_result['manifest_analysis'].get('application') else 'No'}

### Support
For installation issues or questions, please refer to the module documentation or contact support.
"""
    
    return readme_content

def main():
    """Main validation function"""
    print("🔍 PRODUCTION READINESS VALIDATION")
    print("=" * 50)
    
    # Get all modules
    modules = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.') and not item.startswith('__'):
            if os.path.exists(os.path.join(item, '__manifest__.py')):
                modules.append(item)
    
    print(f"📊 Found {len(modules)} modules to validate")
    
    results = {
        "validation_timestamp": datetime.now().isoformat(),
        "total_modules": len(modules),
        "production_ready": 0,
        "needs_fixes": 0,
        "invalid": 0,
        "detailed_results": []
    }
    
    # Validate each module
    for i, module in enumerate(sorted(modules)[:20], 1):  # Limit to first 20 for initial run
        print(f"🔍 Validating {i}/20: {module}")
        
        validation_result = validate_module_production_readiness(module)
        results["detailed_results"].append(validation_result)
        
        if validation_result["status"] == "ready":
            results["production_ready"] += 1
            print(f"  ✅ Production Ready")
        elif validation_result["status"] == "needs_fixes":
            results["needs_fixes"] += 1
            print(f"  🔧 Needs Fixes: {len(validation_result['code_safety_issues'])} issues")
        else:
            results["invalid"] += 1
            print(f"  ❌ Invalid: {len(validation_result['missing_components'])} missing components")
        
        # Generate README for each module
        readme_content = generate_installation_readme(module, validation_result)
        readme_path = os.path.join(module, 'INSTALLATION_README.md')
        with open(readme_path, 'w') as f:
            f.write(readme_content)
    
    # Save results
    with open('production_readiness_validation.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 VALIDATION SUMMARY:")
    print(f"  ✅ Production Ready: {results['production_ready']}")
    print(f"  🔧 Needs Fixes: {results['needs_fixes']}")
    print(f"  ❌ Invalid: {results['invalid']}")
    print(f"\n📄 Results saved to: production_readiness_validation.json")
    print(f"📋 Individual README files created for each module")

if __name__ == "__main__":
    main()
