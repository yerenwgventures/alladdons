#!/usr/bin/env python3
import os
import re
import json

def extract_manifest_info(manifest_path):
    """Extract key information from a manifest file"""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # More robust regex patterns
        name_match = re.search(r"'name'\s*:\s*['\"]([^'\"]*?)['\"]", content, re.DOTALL)
        summary_match = re.search(r"'summary'\s*:\s*['\"]([^'\"]*?)['\"]", content, re.DOTALL)
        description_match = re.search(r"'description'\s*:\s*['\"]([^'\"]*?)['\"]", content, re.DOTALL)
        category_match = re.search(r"'category'\s*:\s*['\"]([^'\"]*?)['\"]", content, re.DOTALL)
        version_match = re.search(r"'version'\s*:\s*['\"]([^'\"]*?)['\"]", content, re.DOTALL)
        author_match = re.search(r"'author'\s*:\s*['\"]([^'\"]*?)['\"]", content, re.DOTALL)
        application_match = re.search(r"'application'\s*:\s*(True|False)", content)

        # Handle triple-quoted strings
        if not summary_match:
            summary_match = re.search(r"'summary'\s*:\s*\"\"\"([^\"]*?)\"\"\"", content, re.DOTALL)
        if not description_match:
            description_match = re.search(r"'description'\s*:\s*\"\"\"([^\"]*?)\"\"\"", content, re.DOTALL)

        return {
            'name': name_match.group(1).strip() if name_match else '',
            'summary': summary_match.group(1).strip() if summary_match else '',
            'description': description_match.group(1).strip() if description_match else '',
            'category': category_match.group(1).strip() if category_match else '',
            'version': version_match.group(1).strip() if version_match else '',
            'author': author_match.group(1).strip() if author_match else '',
            'application': application_match.group(1) == 'True' if application_match else False
        }
    except Exception as e:
        print(f"Error processing {manifest_path}: {e}")
        return None

def main():
    modules = []
    
    # Walk through all directories
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.'):
            manifest_path = os.path.join(item, '__manifest__.py')
            if os.path.exists(manifest_path):
                info = extract_manifest_info(manifest_path)
                if info:
                    info['module_name'] = item
                    modules.append(info)
    
    # Sort by category then name
    modules.sort(key=lambda x: (x['category'], x['name']))
    
    # Group by category
    categories = {}
    for module in modules:
        cat = module['category'] or 'Uncategorized'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(module)
    
    # Print summary
    print(f"Total modules found: {len(modules)}")
    print(f"Categories: {len(categories)}")
    print("\nCategory breakdown:")
    for cat, mods in categories.items():
        print(f"  {cat}: {len(mods)} modules")
    
    # Save to JSON for further processing
    with open('modules_data.json', 'w') as f:
        json.dump({
            'total_modules': len(modules),
            'categories': categories,
            'modules': modules
        }, f, indent=2)
    
    print("\nData saved to modules_data.json")

if __name__ == "__main__":
    main()
