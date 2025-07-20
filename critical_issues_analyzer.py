#!/usr/bin/env python3
"""
Critical Issues Analyzer
Identifies and analyzes the 9 modules with major issues for targeted fixes
"""
import json
import os
import ast
from pathlib import Path

def load_verification_results():
    """Load the comprehensive verification results"""
    try:
        with open('comprehensive_verification_results.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Verification results file not found")
        return None

def analyze_critical_module(module_name):
    """Analyze a specific module with major issues"""
    module_path = Path(module_name)
    
    if not module_path.exists():
        return {"error": "Module directory not found"}
    
    analysis = {
        "module": module_name,
        "issues": [],
        "fixable_issues": [],
        "complex_issues": []
    }
    
    # Check manifest file
    manifest_path = module_path / '__manifest__.py'
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for placeholder content
            if any(placeholder in content.upper() for placeholder in ['TODO', 'PLACEHOLDER', 'CHANGEME']):
                analysis["fixable_issues"].append("Manifest contains placeholder text")
            
            # Parse manifest to check data files
            tree = ast.parse(content)
            manifest_dict = ast.literal_eval(tree.body[0].value)
            
            missing_files = []
            for data_file in manifest_dict.get('data', []):
                if not (module_path / data_file).exists():
                    missing_files.append(data_file)
            
            if missing_files:
                analysis["complex_issues"].append(f"Missing data files: {missing_files}")
                
        except Exception as e:
            analysis["complex_issues"].append(f"Manifest parsing error: {str(e)}")
    
    # Check Python files for major issues
    for py_file in module_path.rglob('*.py'):
        if py_file.name == '__manifest__.py':
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Count pass statements vs implementations
            pass_count = content.count('pass')
            method_count = content.count('def ')
            
            if pass_count > 5 and pass_count > method_count * 0.7:
                analysis["complex_issues"].append(f"{py_file.name}: Mostly empty implementations ({pass_count} pass statements)")
            
            # Check for critical TODOs
            lines = content.split('\n')
            critical_todos = []
            for i, line in enumerate(lines, 1):
                if 'TODO' in line.upper() and any(keyword in line.lower() for keyword in ['critical', 'important', 'fix', 'broken']):
                    critical_todos.append(f"Line {i}: {line.strip()}")
            
            if critical_todos:
                analysis["complex_issues"].extend(critical_todos)
                
        except Exception as e:
            analysis["issues"].append(f"Error reading {py_file.name}: {str(e)}")
    
    # Check XML files for structural issues
    for xml_file in module_path.rglob('*.xml'):
        try:
            with open(xml_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for malformed XML
            if '<record' in content and content.count('<record') != content.count('</record>'):
                analysis["complex_issues"].append(f"{xml_file.name}: Malformed XML records")
            
            # Check for placeholder field names
            if 'field name="template_' in content or 'field name="placeholder_' in content:
                analysis["fixable_issues"].append(f"{xml_file.name}: Placeholder field names")
                
        except Exception as e:
            analysis["issues"].append(f"Error reading {xml_file.name}: {str(e)}")
    
    return analysis

def main():
    print("🔍 CRITICAL ISSUES ANALYZER")
    print("=" * 50)
    
    # Load verification results
    results = load_verification_results()
    if not results:
        return
    
    # Find modules with major issues
    major_issue_modules = []
    for result in results.get('detailed_results', []):
        if result.get('status') == 'MAJOR_ISSUES':
            major_issue_modules.append(result['module'])
    
    print(f"📊 Found {len(major_issue_modules)} modules with major issues")
    print()
    
    if not major_issue_modules:
        print("✅ No modules with major issues found in detailed results")
        return
    
    # Analyze each critical module
    critical_analyses = []
    
    for module in major_issue_modules:
        print(f"🔍 Analyzing {module}...")
        analysis = analyze_critical_module(module)
        critical_analyses.append(analysis)
        
        if "error" in analysis:
            print(f"  ❌ {analysis['error']}")
            continue
        
        print(f"  📋 Issues found:")
        print(f"    🔧 Fixable issues: {len(analysis['fixable_issues'])}")
        print(f"    ⚠️ Complex issues: {len(analysis['complex_issues'])}")
        print(f"    💥 Other issues: {len(analysis['issues'])}")
        
        # Show top issues
        if analysis['fixable_issues']:
            print(f"    🔧 Top fixable: {analysis['fixable_issues'][0]}")
        if analysis['complex_issues']:
            print(f"    ⚠️ Top complex: {analysis['complex_issues'][0]}")
        print()
    
    # Generate fix recommendations
    print("🔧 FIX RECOMMENDATIONS")
    print("-" * 30)
    
    total_fixable = sum(len(a['fixable_issues']) for a in critical_analyses if 'error' not in a)
    total_complex = sum(len(a['complex_issues']) for a in critical_analyses if 'error' not in a)
    
    print(f"📊 Summary:")
    print(f"  🔧 {total_fixable} fixable issues across all critical modules")
    print(f"  ⚠️ {total_complex} complex issues requiring detailed review")
    print()
    
    if total_fixable > 0:
        print("🔧 IMMEDIATE FIXES RECOMMENDED:")
        print("  1. Replace placeholder text in manifests")
        print("  2. Fix placeholder field names in XML files")
        print("  3. Remove or complete TODO comments")
        print()
    
    if total_complex > 0:
        print("⚠️ COMPLEX ISSUES REQUIRING REVIEW:")
        print("  1. Missing data files need to be created or removed from manifest")
        print("  2. Empty implementations need proper code")
        print("  3. Malformed XML needs structural fixes")
        print()
    
    # Save analysis results
    with open('critical_issues_analysis.json', 'w') as f:
        json.dump({
            "total_critical_modules": len(major_issue_modules),
            "total_fixable_issues": total_fixable,
            "total_complex_issues": total_complex,
            "detailed_analyses": critical_analyses
        }, f, indent=2)
    
    print("📄 Detailed analysis saved to critical_issues_analysis.json")
    
    # Deployment recommendation
    print()
    print("🚀 DEPLOYMENT RECOMMENDATION:")
    if total_fixable > total_complex:
        print("  ✅ Most issues are fixable - recommend addressing before deployment")
    else:
        print("  ⚠️ Many complex issues - consider excluding these modules from initial deployment")

if __name__ == "__main__":
    main()
