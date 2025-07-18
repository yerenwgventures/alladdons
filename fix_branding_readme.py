#!/usr/bin/env python3
"""
Script to update branding in all README.rst files
Replaces Cybrosys branding with CBMS TECHNOLOGIES LTD branding
Removes technical content and makes documentation business-focused
"""
import os
import re
import sys

def update_readme_branding(file_path):
    """Update branding and content in a single README file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update company references
        content = re.sub(
            r'Cybrosys Techno Solutions',
            'CBMS TECHNOLOGIES LTD',
            content
        )
        
        # Update website URLs
        content = re.sub(
            r'https://cybrosys\.com',
            'https://www.mycbms.com',
            content
        )
        
        content = re.sub(
            r'https://www\.cybrosys\.com',
            'https://www.mycbms.com',
            content
        )
        
        # Update email addresses
        content = re.sub(
            r'odoo@cybrosys\.com',
            'info@mycbms.com',
            content
        )
        
        # Remove technical badges and code snippets (common patterns)
        content = re.sub(
            r'\.\. image:: https://img\.shields\.io/badge/.*?\n',
            '',
            content,
            flags=re.MULTILINE
        )
        
        # Remove installation instructions (too technical)
        content = re.sub(
            r'Installation\n=+\n.*?(?=\n\n[A-Z]|\n\n$|\Z)',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove configuration sections that are too technical
        content = re.sub(
            r'Configuration\n=+\n\* No additional configurations needed\n',
            'Configuration\n=============\n* Easy setup through Odoo Apps interface\n* No complex configuration required\n',
            content
        )
        
        # Update credits section to be more professional
        content = re.sub(
            r'Credits\n-+\n\* Developers:.*?Contact: .*?\n',
            'Support\n-------\n* Professional support available\n* Contact: info@mycbms.com\n',
            content,
            flags=re.DOTALL
        )
        
        # Clean up multiple newlines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all README files"""
    updated_count = 0
    total_count = 0
    
    print("Starting README branding update...")
    
    # Find all README.rst files
    for root, dirs, files in os.walk('.'):
        if 'README.rst' in files:
            readme_path = os.path.join(root, 'README.rst')
            total_count += 1
            
            if update_readme_branding(readme_path):
                updated_count += 1
                print(f"Updated: {readme_path}")
            
            # Progress indicator
            if total_count % 50 == 0:
                print(f"Processed {total_count} files...")
    
    print(f"\nCompleted! Updated {updated_count} out of {total_count} README files.")

if __name__ == "__main__":
    main()
