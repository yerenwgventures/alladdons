#!/usr/bin/env python3
"""
ZOE'S DEEP ANALYTICS FIXER
Fix all analytics models with SQL view creation issues
"""
import os
import re
from pathlib import Path

def fix_analytics_model_sql_issues(file_path):
    """Fix SQL view creation issues in analytics models"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove or comment out the init method with SQL view creation
        if 'def init(self):' in content and 'CREATE OR REPLACE VIEW' in content:
            # Find the init method and comment it out
            init_pattern = r'(\s+def init\(self\):.*?(?=\n\s{4}def|\n\s{0,3}class|\n\s{0,3}$|\Z))'
            
            def comment_init_method(match):
                method_content = match.group(1)
                # Comment out each line
                lines = method_content.split('\n')
                commented_lines = []
                for line in lines:
                    if line.strip():
                        commented_lines.append('    # ' + line)
                    else:
                        commented_lines.append(line)
                return '\n'.join(commented_lines)
            
            content = re.sub(init_pattern, comment_init_method, content, flags=re.DOTALL)
            
            print(f"    ✅ Commented out SQL view creation in {file_path}")
            
        # Add missing tools import if needed
        if 'tools.drop_view_if_exists' in content and 'from odoo import' in content:
            if 'tools' not in content.split('from odoo import')[1].split('\n')[0]:
                content = content.replace('from odoo import', 'from odoo import tools,')
                print(f"    ✅ Added tools import in {file_path}")
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"    ❌ Error fixing {file_path}: {e}")
        return False

def main():
    print("🔧 ZOE'S DEEP ANALYTICS FIXER")
    print("=" * 50)
    
    # Find all analytics model files
    analytics_files = []
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('_analytics.py') and 'models' in root:
                analytics_files.append(Path(root) / file)
    
    print(f"📊 Found {len(analytics_files)} analytics model files")
    
    fixed_count = 0
    
    for analytics_file in analytics_files:
        print(f"🔧 Fixing {analytics_file}")
        if fix_analytics_model_sql_issues(analytics_file):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} analytics model files")
    print("🎉 ZOE'S DEEP ANALYTICS FIXING COMPLETE!")

if __name__ == "__main__":
    main()
