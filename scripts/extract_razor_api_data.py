"""
DexBot API Reference Data Extractor
Python Script for API Data Processing

This script extracts and prepares API data for the DexBot API reference 
optimization system (TECH-001).

Instructions:
1. Ensure you have access to RazorEnhanced's AutoComplete.json file
2. Run this script with Python: python extract_razor_api_data.py
3. The script will:
   - Read the AutoComplete.json file
   - Extract API metadata
   - Generate a summary report
   - Prepare data for DexBot processing

The output will be displayed in the console and saved to files
that can be used with the DexBot API reference system.
"""

import json
import os
import argparse
import sys
from datetime import datetime
from pathlib import Path

def main():
    """Main extraction function"""
    parser = argparse.ArgumentParser(description='DexBot API Reference Data Extractor (TECH-001)')
    parser.add_argument('--input', '-i', default='./config/AutoComplete.json', 
                       help='Path to AutoComplete.json file (default: ./config/AutoComplete.json)')
    parser.add_argument('--output', '-o', default='./tmp/api_extraction/', 
                       help='Output directory (default: ./tmp/api_extraction/)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    print("🔧 DexBot API Reference Data Extractor (TECH-001)")
    print("=" * 60)
    
    if args.verbose:
        print(f"Input file: {args.input}")
        print(f"Output directory: {args.output}")
    
    try:
        # Configuration
        config_path = args.input
        output_dir = args.output
        
        # Validate input file exists
        if not os.path.exists(config_path):
            print(f"❌ Input file not found: {config_path}")
            print("💡 Make sure to specify the correct path to AutoComplete.json")
            sys.exit(1)
        
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        
        # Read AutoComplete.json
        print("📖 Reading AutoComplete.json...")
        api_data = read_autocomplete_data(config_path)
        
        if not api_data:
            print("❌ Failed to read API data")
            sys.exit(1)
        
        # Extract metadata
        print("🔍 Extracting API metadata...")
        metadata = extract_api_metadata(api_data)
        
        # Generate reports
        print("📊 Generating reports...")
        generate_extraction_reports(api_data, metadata, output_dir)
        
        # Display summary
        display_extraction_summary(metadata)
        
        print("✅ API data extraction completed successfully!")
        print(f"📁 Output saved to: {output_dir}")
        print("🔄 Use the exported files with your DexBot project")
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during extraction: {str(e)}")
        if args.verbose:
            import traceback
            print(traceback.format_exc())
        sys.exit(1)

def read_autocomplete_data(config_path):
    """Read and parse AutoComplete.json"""
    try:
        if not os.path.exists(config_path):
            print(f"❌ AutoComplete.json not found at: {config_path}")
            return None
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        file_size = os.path.getsize(config_path)
        print(f"📄 Loaded AutoComplete.json ({file_size} bytes)")
        
        return data
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        return None

def extract_api_metadata(api_data):
    """Extract comprehensive API metadata"""
    metadata = {
        'extraction_date': datetime.now().isoformat(),
        'razor_version': api_data.get('settings', {}).get('version', 'Unknown'),
        'total_classes': len(api_data.get('classes', [])),
        'total_methods': len(api_data.get('methods', [])),
        'total_properties': len(api_data.get('properties', [])),
        'total_constructors': len(api_data.get('constructors', [])),
        'classes': {},
        'method_signatures': [],
        'property_types': {},
        'namespaces': set()
    }
    
    # Process classes
    for cls in api_data.get('classes', []):
        class_name = cls.get('itemClass', '')
        metadata['classes'][class_name] = {
            'description': cls.get('itemDescription', ''),
            'methods': [],
            'properties': [],
            'constructors': []
        }
        
        # Extract namespace
        if ':' in class_name:
            namespace = class_name.split(':')[0]
            metadata['namespaces'].add(namespace)
    
    # Process methods
    for method in api_data.get('methods', []):
        class_name = method.get('itemClass', '')
        method_name = method.get('itemName', '')
        
        if class_name in metadata['classes']:
            metadata['classes'][class_name]['methods'].append(method_name)
        
        # Build method signature
        params = method.get('paramList', [])
        param_strings = []
        for param in params:
            param_str = f"{param.get('itemName', '')}: {param.get('itemType', '')}"
            param_strings.append(param_str)
        
        signature = f"{class_name}.{method_name}({', '.join(param_strings)})"
        metadata['method_signatures'].append(signature)
    
    # Process properties
    for prop in api_data.get('properties', []):
        class_name = prop.get('itemClass', '')
        prop_name = prop.get('itemName', '')
        prop_type = prop.get('propertyType', '')
        
        if class_name in metadata['classes']:
            metadata['classes'][class_name]['properties'].append(prop_name)
        
        metadata['property_types'][f"{class_name}.{prop_name}"] = prop_type
    
    # Process constructors
    for ctor in api_data.get('constructors', []):
        class_name = ctor.get('itemClass', '')
        
        if class_name in metadata['classes']:
            metadata['classes'][class_name]['constructors'].append(ctor.get('itemName', ''))
    
    # Convert sets to lists for JSON serialization
    metadata['namespaces'] = list(metadata['namespaces'])
    
    return metadata

def generate_extraction_reports(api_data, metadata, output_dir):
    """Generate comprehensive extraction reports"""
    
    # 1. Save complete API data
    api_output_path = os.path.join(output_dir, "AutoComplete_Export.json")
    with open(api_output_path, 'w', encoding='utf-8') as f:
        json.dump(api_data, f, indent=2, ensure_ascii=False)
    
    # 2. Save metadata summary
    metadata_output_path = os.path.join(output_dir, "API_Metadata.json")
    with open(metadata_output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # 3. Generate markdown report
    markdown_report = generate_markdown_report(metadata)
    markdown_output_path = os.path.join(output_dir, "API_Extraction_Report.md")
    with open(markdown_output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    # 4. Generate class list
    class_list = generate_class_list(metadata)
    class_list_path = os.path.join(output_dir, "Class_List.txt")
    with open(class_list_path, 'w', encoding='utf-8') as f:
        f.write(class_list)
    
    # 5. Generate method signatures
    method_signatures = '\n'.join(metadata['method_signatures'])
    signatures_path = os.path.join(output_dir, "Method_Signatures.txt")
    with open(signatures_path, 'w', encoding='utf-8') as f:
        f.write(method_signatures)

def generate_markdown_report(metadata):
    """Generate markdown extraction report"""
    report = f"""# DexBot API Reference Extraction Report

**Generated:** {metadata['extraction_date']}  
**RazorEnhanced Version:** {metadata['razor_version']}

## Summary Statistics

| Category | Count |
|----------|-------|
| Classes | {metadata['total_classes']} |
| Methods | {metadata['total_methods']} |
| Properties | {metadata['total_properties']} |
| Constructors | {metadata['total_constructors']} |
| Namespaces | {len(metadata['namespaces'])} |

## Namespaces

{chr(10).join(f"- {ns}" for ns in sorted(metadata['namespaces']))}

## Top 10 Classes by Method Count

"""
    
    # Sort classes by method count
    class_method_counts = []
    for class_name, class_data in metadata['classes'].items():
        method_count = len(class_data['methods'])
        class_method_counts.append((class_name, method_count))
    
    class_method_counts.sort(key=lambda x: x[1], reverse=True)
    
    for class_name, method_count in class_method_counts[:10]:
        report += f"- **{class_name}**: {method_count} methods\n"
    
    report += f"""
## Top 10 Classes by Property Count

"""
    
    # Sort classes by property count
    class_property_counts = []
    for class_name, class_data in metadata['classes'].items():
        property_count = len(class_data['properties'])
        class_property_counts.append((class_name, property_count))
    
    class_property_counts.sort(key=lambda x: x[1], reverse=True)
    
    for class_name, property_count in class_property_counts[:10]:
        report += f"- **{class_name}**: {property_count} properties\n"
    
    report += f"""
## Next Steps for DexBot Integration

1. Copy the exported files to your DexBot project:
   - `AutoComplete_Export.json` → `Config/AutoComplete.json`
   - `API_Metadata.json` → `ref/metadata/`
   - `API_Extraction_Report.md` → `docs/`

2. Run the DexBot API reference generation:
   ```bash
   invoke generate-api-reference
   ```

3. Review and customize the generated documentation

4. Integrate with your DexBot systems

## File Exports

- `AutoComplete_Export.json` - Complete API data
- `API_Metadata.json` - Extracted metadata and statistics
- `API_Extraction_Report.md` - This report
- `Class_List.txt` - Simple list of all classes
- `Method_Signatures.txt` - All method signatures
"""
    
    return report

def generate_class_list(metadata):
    """Generate simple class list"""
    classes = sorted(metadata['classes'].keys())
    return '\n'.join(classes)

def display_extraction_summary(metadata):
    """Display extraction summary in console"""
    print("📊 API Extraction Summary")
    print("-" * 40)
    print(f"RazorEnhanced Version: {metadata['razor_version']}")
    print(f"Total Classes: {metadata['total_classes']}")
    print(f"Total Methods: {metadata['total_methods']}")
    print(f"Total Properties: {metadata['total_properties']}")
    print(f"Total Constructors: {metadata['total_constructors']}")
    print(f"Namespaces: {len(metadata['namespaces'])}")
    
    print("")
    print("🏆 Top 5 Classes by Method Count:")
    
    # Sort and display top classes
    class_method_counts = []
    for class_name, class_data in metadata['classes'].items():
        method_count = len(class_data['methods'])
        if method_count > 0:
            class_method_counts.append((class_name, method_count))
    
    class_method_counts.sort(key=lambda x: x[1], reverse=True)
    
    for i, (class_name, method_count) in enumerate(class_method_counts[:5]):
        print(f"  {i+1}. {class_name}: {method_count} methods")
    
    print("")
    print("📋 Available Namespaces:")
    for ns in sorted(metadata['namespaces']):
        print(f"  - {ns}")

def copy_instructions():
    """Display copy instructions for developers"""
    print("")
    print("📋 Instructions for DexBot Integration:")
    print("=" * 50)
    print("1. Navigate to the output directory")
    print("2. Copy 'AutoComplete_Export.json' to your DexBot project")
    print("3. Rename it to 'AutoComplete.json' in DexBot/Config/")
    print("4. Run: invoke generate-api-reference")
    print("5. Review generated documentation in ./ref/")
    print("")
    print("🎯 TECH-001 API Reference Optimization Ready!")
    print("")
    print("💡 Usage examples:")
    print("   python extract_razor_api_data.py")
    print("   python extract_razor_api_data.py --input /path/to/AutoComplete.json")
    print("   python extract_razor_api_data.py --output ./my_export/ --verbose")

# Run the extraction
if __name__ == "__main__":
    try:
        main()
        copy_instructions()
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)
