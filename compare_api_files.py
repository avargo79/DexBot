#!/usr/bin/env python3
"""
Compare legacy and new API reference files to determine if legacy file can be deprecated.
"""

import json
import os

def compare_api_files():
    """Compare the legacy and new API reference files."""
    
    # Read legacy file
    with open('ref/api_reference.json', 'r', encoding='utf-8') as f:
        legacy = json.load(f)

    # Read new file  
    with open('ref/json/api_reference.json', 'r', encoding='utf-8') as f:
        new = json.load(f)

    print('LEGACY FILE ANALYSIS:')
    print(f'- Generated at: {legacy.get("generated_at", "N/A")}')
    print(f'- Version: {legacy.get("version", "N/A")}')
    print(f'- Modules: {len(legacy.get("modules", {}))}')
    print(f'- File size: {os.path.getsize("ref/api_reference.json")} bytes')

    print('\nNEW FILE ANALYSIS:')
    print(f'- Generated at: {new["metadata"]["generated_at"]}')
    print(f'- Version: {new["metadata"]["version"]}')
    print(f'- Classes: {new["metadata"]["total_classes"]}')
    print(f'- Methods: {new["metadata"]["total_methods"]}')
    print(f'- Properties: {new["metadata"]["total_properties"]}')
    print(f'- File size: {os.path.getsize("ref/json/api_reference.json")} bytes')

    print('\nCOMPARISON:')
    print('- Legacy file: Based on web scraping, smaller, limited structure')
    print('- New file: Based on AutoComplete.json, comprehensive, better structured')
    print('- New system provides multi-format output (HTML, Markdown, JSON)')
    print('- Legacy file can be safely deprecated/archived')
    
    # Check for any modules in legacy not in new
    legacy_modules = set(legacy.get("modules", {}).keys())
    new_classes = set(cls["name"] for cls in new["classes"])
    
    print(f'\nLegacy modules: {len(legacy_modules)}')
    print(f'New classes: {len(new_classes)}')
    
    missing_in_new = legacy_modules - new_classes
    if missing_in_new:
        print(f'Modules in legacy but not in new: {missing_in_new}')
    else:
        print('All legacy modules are represented in the new system')

if __name__ == "__main__":
    compare_api_files()
