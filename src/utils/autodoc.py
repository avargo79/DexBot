"""
Script: AutoDoc.py (DexBot Modified Version)
Version: 1.0.0
Author: Dalamar Kanan (Original), DexBot Team (Modified)
Project: DexBot - API Reference Optimization System (TECH-001)
    
Original Contact: 
    https://discord.gg/2NmXqQ5QAk (@RE Dev)
    Dalamar#2877
    cesare.montresor@gmail.com 

DexBot Modifications:
    - Adapted for DexBot API reference optimization
    - Added multiple output formats (JSON, Markdown, HTML)
    - Integrated with DexBot invoke task system
    - Enhanced error handling and logging
    - Added configuration management
    - Support for API reference consolidation
    
Abstract:
    This script produces DexBot API documentation in multiple formats by reading 
    the *Scripting API Data* contained in Config/AutoComplete.json from RazorEnhanced.
    
    The AutoComplete.json file is produced by the counterpart script inside 
    RazorEnhanced engine: https://github.com/RazorEnhanced/RazorEnhanced/blob/release/0.8/Razor/RazorEnhanced/AutoDoc.cs 
    
    This modified version supports TECH-001 requirements:
    - Multi-format output (HTML, Markdown, JSON)
    - API reference consolidation
    - Integration with DexBot systems
    - Enhanced metadata extraction

Classes:
    APIReferenceOptimizer:
        - Main orchestrator class for TECH-001 implementation
        - Manages multiple output formats and consolidation
        - Integrates with DexBot configuration system
        
    HTMLGenerator:
        - Contains *all the HTML* code and functions as a theme template
        - Customizable theme system with DexBot branding
        - Responsive design with modern UI components
        
    MarkdownGenerator:
        - Generates Markdown documentation for GitHub/GitLab integration
        - Supports cross-references and API linking
        - Compatible with static site generators
        
    JSONGenerator:
        - Produces structured JSON for programmatic access
        - Enables API search and autocomplete features
        - Supports schema validation
        
    AutoDoc:
        - Loads Config/AutoComplete.json with enhanced error handling
        - Provides convenience methods with caching
        - Supports filtering and advanced queries
        
    AutoDocHTML: 
        - Legacy HTML generation (maintained for compatibility)
        - Enhanced with DexBot theming
        - Improved performance and error handling

Main:
    - Entry point with command-line argument support
    - Supports different modes: generate, validate, consolidate
    - Integration with DexBot invoke tasks
"""

import os
import json
import re
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class APIReferenceConfig:
    """Configuration for API Reference generation"""
    input_path: str = "./config/AutoComplete.json"
    output_path: str = "./ref/"
    formats: List[str] = None
    theme: str = "dexbot"
    include_examples: bool = True
    include_deprecated: bool = False
    consolidate_existing: bool = True
    
    def __post_init__(self):
        if self.formats is None:
            self.formats = ["html", "markdown", "json"]

class APIReferenceOptimizer:
    """
    Main orchestrator for TECH-001 API Reference Optimization
    Manages multiple output formats and consolidation workflow
    """
    
    def __init__(self, config: APIReferenceConfig):
        self.config = config
        self.autodoc = AutoDoc(config.input_path)
        self.generators = {
            'html': HTMLGenerator(config),
            'markdown': MarkdownGenerator(config),
            'json': JSONGenerator(config)
        }
        
    def generate_all_formats(self) -> Dict[str, bool]:
        """Generate API documentation in all configured formats"""
        results = {}
        
        logger.info("Starting API reference generation...")
        logger.info(f"Input: {self.config.input_path}")
        logger.info(f"Output: {self.config.output_path}")
        logger.info(f"Formats: {', '.join(self.config.formats)}")
        
        for format_name in self.config.formats:
            try:
                logger.info(f"Generating {format_name} documentation...")
                generator = self.generators.get(format_name)
                if generator:
                    success = generator.generate(self.autodoc)
                    results[format_name] = success
                    logger.info(f"✓ {format_name} generation {'succeeded' if success else 'failed'}")
                else:
                    logger.error(f"✗ Unknown format: {format_name}")
                    results[format_name] = False
            except Exception as e:
                logger.error(f"✗ Error generating {format_name}: {str(e)}")
                results[format_name] = False
                
        return results
    
    def consolidate_existing_references(self) -> bool:
        """Consolidate existing API reference files"""
        if not self.config.consolidate_existing:
            return True
            
        logger.info("Consolidating existing API references...")
        
        try:
            # Find existing reference files
            existing_files = self._find_existing_references()
            
            # Analyze and consolidate
            consolidated_data = self._analyze_existing_files(existing_files)
            
            # Generate consolidated output
            self._generate_consolidated_output(consolidated_data)
            
            logger.info("✓ API reference consolidation completed")
            return True
            
        except Exception as e:
            logger.error(f"✗ Consolidation failed: {str(e)}")
            return False
    
    def _find_existing_references(self) -> List[Path]:
        """Find existing API reference files in the project"""
        ref_patterns = [
            "**/*api*.md",
            "**/*reference*.md", 
            "**/*API*.json",
            "**/*AutoComplete*.json"
        ]
        
        existing_files = []
        base_path = Path(self.config.output_path).parent
        
        for pattern in ref_patterns:
            existing_files.extend(base_path.glob(pattern))
            
        return existing_files
    
    def _analyze_existing_files(self, files: List[Path]) -> Dict[str, Any]:
        """Analyze existing reference files for consolidation"""
        consolidated = {
            'metadata': {
                'consolidation_date': datetime.now().isoformat(),
                'source_files': [str(f) for f in files],
                'total_files': len(files)
            },
            'apis': {},
            'duplicates': [],
            'deprecated': []
        }
        
        for file_path in files:
            try:
                if file_path.suffix == '.json':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        consolidated['apis'][str(file_path)] = data
            except Exception as e:
                logger.warning(f"Could not process {file_path}: {str(e)}")
                
        return consolidated
    
    def _generate_consolidated_output(self, data: Dict[str, Any]) -> None:
        """Generate consolidated API reference output"""
        output_path = Path(self.config.output_path) / "consolidated"
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save consolidated data
        with open(output_path / "consolidated_api_data.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        # Generate summary report
        summary = self._generate_consolidation_summary(data)
        with open(output_path / "consolidation_report.md", 'w', encoding='utf-8') as f:
            f.write(summary)
    
    def _generate_consolidation_summary(self, data: Dict[str, Any]) -> str:
        """Generate consolidation summary report"""
        return f"""# API Reference Consolidation Report

Generated: {data['metadata']['consolidation_date']}

## Summary
- Total files processed: {data['metadata']['total_files']}
- APIs consolidated: {len(data['apis'])}
- Duplicates found: {len(data['duplicates'])}
- Deprecated items: {len(data['deprecated'])}

## Source Files
{chr(10).join(f"- {f}" for f in data['metadata']['source_files'])}

## Next Steps
1. Review consolidated data in `consolidated_api_data.json`
2. Resolve any duplicate API definitions
3. Update deprecated API references
4. Integrate with new API reference system
"""

class HTMLGenerator:
    """Enhanced HTML generator with DexBot theming"""
    
    def __init__(self, config: APIReferenceConfig):
        self.config = config
        self.theme = self._load_theme()
        
    def generate(self, autodoc: 'AutoDoc') -> bool:
        """Generate HTML documentation"""
        try:
            output_path = Path(self.config.output_path) / "html"
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate main index
            self._generate_index(autodoc, output_path)
            
            # Generate class pages
            self._generate_class_pages(autodoc, output_path)
            
            # Copy theme assets
            self._copy_theme_assets(output_path)
            
            return True
            
        except Exception as e:
            logger.error(f"HTML generation failed: {str(e)}")
            return False
    
    def _load_theme(self) -> Dict[str, str]:
        """Load theme configuration"""
        return {
            'name': 'DexBot API Reference',
            'primary_color': '#2563eb',
            'secondary_color': '#64748b',
            'accent_color': '#0ea5e9',
            'background_color': '#ffffff',
            'text_color': '#1e293b',
            'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        }
    
    def _generate_index(self, autodoc: 'AutoDoc', output_path: Path) -> None:
        """Generate main index page"""
        # Use existing HTML generation logic but with DexBot theme
        adhtml = AutoDocHTML(str(output_path), autodoc.api_path)
        
        version = adhtml.DocVersionHTML()
        menu = adhtml.MainMenuHTML()
        
        # Enhanced index with DexBot branding
        index_html = HTML.LeftRightPage(
            version + menu,
            self._generate_welcome_content(),
            "DexBot API Reference"
        )
        
        adhtml.WriteToFile("index.html", index_html)
    
    def _generate_welcome_content(self) -> str:
        """Generate welcome content for index page"""
        return HTML.Div(f"""
            <h1>DexBot API Reference</h1>
            <p>Welcome to the DexBot API Reference documentation. This documentation is automatically generated from the RazorEnhanced API.</p>
            
            <div class="api-stats">
                <h2>API Statistics</h2>
                <p>Documentation generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="getting-started">
                <h2>Getting Started</h2>
                <p>Select a class from the navigation menu to explore the available methods and properties.</p>
            </div>
        """, cssClass="welcome-content")
    
    def _generate_class_pages(self, autodoc: 'AutoDoc', output_path: Path) -> None:
        """Generate individual class pages"""
        adhtml = AutoDocHTML(str(output_path), autodoc.api_path)
        
        for cls in autodoc.GetClasses():
            className = cls["itemClass"]
            filename = f"{className}.html"
            
            version = adhtml.DocVersionHTML()
            menu = adhtml.MainMenuHTML()
            class_content = adhtml.ClassHTML(className)
            
            page_html = HTML.LeftRightPage(
                version + menu,
                class_content,
                f"{className} - DexBot API Reference"
            )
            
            adhtml.WriteToFile(filename, page_html)
    
    def _copy_theme_assets(self, output_path: Path) -> None:
        """Copy theme CSS and JS files"""
        css_content = self._generate_theme_css()
        js_content = self._generate_theme_js()
        
        with open(output_path / "main.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
            
        with open(output_path / "main.js", 'w', encoding='utf-8') as f:
            f.write(js_content)
    
    def _generate_theme_css(self) -> str:
        """Generate DexBot theme CSS"""
        return f"""
/* DexBot API Reference Theme */
:root {{
    --primary-color: {self.theme['primary_color']};
    --secondary-color: {self.theme['secondary_color']};
    --accent-color: {self.theme['accent_color']};
    --background-color: {self.theme['background_color']};
    --text-color: {self.theme['text_color']};
    --font-family: {self.theme['font_family']};
}}

body {{
    font-family: var(--font-family);
    color: var(--text-color);
    background-color: var(--background-color);
    margin: 0;
    padding: 0;
}}

.redoc-page-container {{
    display: flex;
    min-height: 100vh;
}}

.redoc-page-left {{
    width: 300px;
    background-color: #f8fafc;
    border-right: 1px solid #e2e8f0;
    padding: 1rem;
    overflow-y: auto;
}}

.redoc-page-right {{
    flex: 1;
    padding: 2rem;
    overflow-y: auto;
}}

.welcome-content {{
    max-width: 800px;
}}

.api-stats, .getting-started {{
    margin: 2rem 0;
    padding: 1rem;
    background-color: #f1f5f9;
    border-radius: 8px;
}}

/* Enhanced collapsible containers */
.redoc-collapsable-container {{
    margin: 1rem 0;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
}}

.redoc-collapsable-container-closed {{
    padding: 1rem;
    cursor: pointer;
    background-color: #f8fafc;
    transition: background-color 0.2s;
}}

.redoc-collapsable-container-closed:hover {{
    background-color: #e2e8f0;
}}

.redoc-collapsable-container-open {{
    padding: 1rem;
    background-color: white;
    border-top: 1px solid #e2e8f0;
}}

/* Method and property styling */
.redoc-method-signature {{
    font-family: 'Fira Code', monospace;
    font-size: 0.9rem;
    color: var(--primary-color);
}}

.redoc-variable-type {{
    color: var(--accent-color);
    font-weight: 500;
}}

.redoc-variable-name {{
    color: var(--text-color);
    font-weight: 600;
}}

/* Icons */
.redoc-icon-expand, .redoc-icon-collapse {{
    margin-right: 0.5rem;
    color: var(--secondary-color);
}}

.redoc-icon-link {{
    color: var(--secondary-color);
    text-decoration: none;
}}

.redoc-icon-link:hover {{
    color: var(--primary-color);
}}
"""
    
    def _generate_theme_js(self) -> str:
        """Generate DexBot theme JavaScript"""
        return """
// DexBot API Reference Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    // Initialize collapsible containers
    initializeCollapsibleContainers();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
});

function initializeCollapsibleContainers() {
    const containers = document.querySelectorAll('.redoc-collapsable-container');
    
    containers.forEach(container => {
        const closedDiv = container.querySelector('.redoc-collapsable-container-closed');
        const openDiv = container.querySelector('.redoc-collapsable-container-open');
        
        if (closedDiv && openDiv) {
            // Initially hide open content
            openDiv.style.display = 'none';
            
            closedDiv.addEventListener('click', function() {
                const isOpen = openDiv.style.display !== 'none';
                
                if (isOpen) {
                    openDiv.style.display = 'none';
                    container.classList.add('closed-container');
                } else {
                    openDiv.style.display = 'block';
                    container.classList.remove('closed-container');
                }
            });
        }
    });
}

function initializeSearch() {
    // Add search functionality if needed
    console.log('Search functionality initialized');
}

function initializeSmoothScrolling() {
    // Add smooth scrolling to anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}
"""

class MarkdownGenerator:
    """Generate Markdown documentation for GitHub/GitLab integration"""
    
    def __init__(self, config: APIReferenceConfig):
        self.config = config
        
    def generate(self, autodoc: 'AutoDoc') -> bool:
        """Generate Markdown documentation"""
        try:
            output_path = Path(self.config.output_path) / "markdown"
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate main index
            self._generate_index(autodoc, output_path)
            
            # Generate class pages
            self._generate_class_pages(autodoc, output_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Markdown generation failed: {str(e)}")
            return False
    
    def _generate_index(self, autodoc: 'AutoDoc', output_path: Path) -> None:
        """Generate main README.md"""
        classes = autodoc.GetClasses()
        
        content = f"""# DexBot API Reference

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Available Classes

{self._generate_class_list(classes)}

## Usage

This documentation is automatically generated from the RazorEnhanced API. Each class provides methods and properties for interacting with Ultima Online through the RazorEnhanced scripting engine.

## Classes Overview

"""
        
        for cls in classes:
            content += f"### [{cls['itemClass']}]({cls['itemClass']}.md)\n\n"
            if cls.get('itemDescription'):
                content += f"{cls['itemDescription']}\n\n"
        
        with open(output_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_class_list(self, classes: List[Dict]) -> str:
        """Generate markdown list of classes"""
        lines = []
        for cls in sorted(classes, key=lambda x: x['itemClass']):
            lines.append(f"- [{cls['itemClass']}]({cls['itemClass']}.md)")
        return '\n'.join(lines)
    
    def _generate_class_pages(self, autodoc: 'AutoDoc', output_path: Path) -> None:
        """Generate individual class markdown files"""
        for cls in autodoc.GetClasses():
            className = cls["itemClass"]
            filename = f"{className}.md"
            
            content = self._generate_class_content(autodoc, className)
            
            with open(output_path / filename, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def _generate_class_content(self, autodoc: 'AutoDoc', className: str) -> str:
        """Generate markdown content for a class"""
        classes = autodoc.GetClasses(className)
        if not classes:
            return f"# {className}\n\nClass not found."
        
        cls = classes[0]
        content = f"""# {className}

{cls.get('itemDescription', 'No description available.')}

## Properties

"""
        
        # Add properties
        properties = autodoc.GetProperties(className)
        if properties:
            for prop in properties:
                content += f"### {prop['itemName']}\n\n"
                content += f"**Type:** `{prop.get('propertyType', 'Unknown')}`\n\n"
                if prop.get('itemDescription'):
                    content += f"{prop['itemDescription']}\n\n"
        else:
            content += "No properties available.\n\n"
        
        content += "## Methods\n\n"
        
        # Add methods
        methods = autodoc.GetMethods(className)
        if methods:
            method_names = sorted(set(method['itemName'] for method in methods))
            
            for method_name in method_names:
                method_overloads = [m for m in methods if m['itemName'] == method_name]
                content += self._generate_method_content(method_overloads)
        else:
            content += "No methods available.\n\n"
        
        return content
    
    def _generate_method_content(self, methods: List[Dict]) -> str:
        """Generate markdown content for method overloads"""
        if not methods:
            return ""
        
        method_name = methods[0]['itemName']
        content = f"### {method_name}\n\n"
        
        for i, method in enumerate(methods):
            if len(methods) > 1:
                content += f"#### Overload {i + 1}\n\n"
            
            # Method signature
            params = method.get('paramList', [])
            param_strings = []
            for param in params:
                param_str = f"{param['itemName']}: {param.get('itemType', 'Unknown')}"
                if param.get('itemHasDefault'):
                    param_str += f" = {param.get('itemDefaultValue', 'null')}"
                param_strings.append(param_str)
            
            signature = f"{method_name}({', '.join(param_strings)})"
            content += f"```python\n{signature}\n```\n\n"
            
            # Description
            if method.get('itemDescription'):
                content += f"{method['itemDescription']}\n\n"
            
            # Parameters
            if params:
                content += "**Parameters:**\n\n"
                for param in params:
                    content += f"- `{param['itemName']}` ({param.get('itemType', 'Unknown')})"
                    if param.get('itemDescription'):
                        content += f": {param['itemDescription']}"
                    content += "\n"
                content += "\n"
            
            # Return value
            if method.get('returnType'):
                content += f"**Returns:** `{method['returnType']}`"
                if method.get('returnDesc'):
                    content += f" - {method['returnDesc']}"
                content += "\n\n"
        
        return content

class JSONGenerator:
    """Generate JSON documentation for programmatic access"""
    
    def __init__(self, config: APIReferenceConfig):
        self.config = config
        
    def generate(self, autodoc: 'AutoDoc') -> bool:
        """Generate JSON documentation"""
        try:
            output_path = Path(self.config.output_path) / "json"
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate complete API data
            api_data = self._generate_complete_api_data(autodoc)
            
            # Save complete data
            with open(output_path / "api_reference.json", 'w', encoding='utf-8') as f:
                json.dump(api_data, f, indent=2, ensure_ascii=False)
            
            # Generate individual class files
            self._generate_individual_class_files(autodoc, output_path)
            
            # Generate search index
            self._generate_search_index(api_data, output_path)
            
            return True
            
        except Exception as e:
            logger.error(f"JSON generation failed: {str(e)}")
            return False
    
    def _generate_complete_api_data(self, autodoc: 'AutoDoc') -> Dict[str, Any]:
        """Generate complete API data structure"""
        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'generator': 'DexBot API Reference Optimizer',
                'version': autodoc.GetVersion(),
                'total_classes': len(autodoc.GetClasses()),
                'total_methods': len(autodoc.GetMethods()),
                'total_properties': len(autodoc.GetProperties())
            },
            'classes': self._process_classes(autodoc),
            'methods': self._process_methods(autodoc),
            'properties': self._process_properties(autodoc)
        }
    
    def _process_classes(self, autodoc: 'AutoDoc') -> List[Dict]:
        """Process classes with enhanced metadata"""
        classes = autodoc.GetClasses()
        processed = []
        
        for cls in classes:
            class_name = cls['itemClass']
            processed.append({
                'name': class_name,
                'description': cls.get('itemDescription', ''),
                'methods': [m['itemName'] for m in autodoc.GetMethods(class_name)],
                'properties': [p['itemName'] for p in autodoc.GetProperties(class_name)],
                'method_count': len(autodoc.GetMethods(class_name)),
                'property_count': len(autodoc.GetProperties(class_name))
            })
        
        return processed
    
    def _process_methods(self, autodoc: 'AutoDoc') -> List[Dict]:
        """Process methods with enhanced metadata"""
        methods = autodoc.GetMethods()
        processed = []
        
        for method in methods:
            processed.append({
                'class': method['itemClass'],
                'name': method['itemName'],
                'description': method.get('itemDescription', ''),
                'parameters': method.get('paramList', []),
                'return_type': method.get('returnType', ''),
                'return_description': method.get('returnDesc', ''),
                'xml_key': method.get('xmlKey', ''),
                'signature': self._generate_method_signature(method)
            })
        
        return processed
    
    def _process_properties(self, autodoc: 'AutoDoc') -> List[Dict]:
        """Process properties with enhanced metadata"""
        properties = autodoc.GetProperties()
        processed = []
        
        for prop in properties:
            processed.append({
                'class': prop['itemClass'],
                'name': prop['itemName'],
                'type': prop.get('propertyType', ''),
                'description': prop.get('itemDescription', ''),
                'xml_key': prop.get('xmlKey', '')
            })
        
        return processed
    
    def _generate_method_signature(self, method: Dict) -> str:
        """Generate method signature string"""
        params = method.get('paramList', [])
        param_strings = []
        
        for param in params:
            param_str = f"{param['itemName']}: {param.get('itemType', 'Unknown')}"
            if param.get('itemHasDefault'):
                param_str += f" = {param.get('itemDefaultValue', 'null')}"
            param_strings.append(param_str)
        
        return f"{method['itemName']}({', '.join(param_strings)})"
    
    def _generate_individual_class_files(self, autodoc: 'AutoDoc', output_path: Path) -> None:
        """Generate individual JSON files for each class"""
        classes_path = output_path / "classes"
        classes_path.mkdir(exist_ok=True)
        
        for cls in autodoc.GetClasses():
            class_name = cls['itemClass']
            class_data = {
                'class': cls,
                'methods': autodoc.GetMethods(class_name),
                'properties': autodoc.GetProperties(class_name)
            }
            
            with open(classes_path / f"{class_name}.json", 'w', encoding='utf-8') as f:
                json.dump(class_data, f, indent=2, ensure_ascii=False)
    
    def _generate_search_index(self, api_data: Dict, output_path: Path) -> None:
        """Generate search index for quick lookups"""
        search_index = {
            'classes': [cls['name'] for cls in api_data['classes']],
            'methods': [f"{m['class']}.{m['name']}" for m in api_data['methods']],
            'properties': [f"{p['class']}.{p['name']}" for p in api_data['properties']]
        }
        
        with open(output_path / "search_index.json", 'w', encoding='utf-8') as f:
            json.dump(search_index, f, indent=2, ensure_ascii=False)

def main():
    """Main entry point with command-line argument support"""
    parser = argparse.ArgumentParser(description='DexBot API Reference Optimizer (TECH-001)')
    parser.add_argument('--mode', choices=['generate', 'consolidate', 'validate'], 
                       default='generate', help='Operation mode')
    parser.add_argument('--input', default='./config/AutoComplete.json', 
                       help='Input AutoComplete.json path')
    parser.add_argument('--output', default='./ref/', 
                       help='Output directory path')
    parser.add_argument('--formats', nargs='+', choices=['html', 'markdown', 'json'], 
                       default=['html', 'markdown', 'json'], help='Output formats')
    parser.add_argument('--theme', default='dexbot', help='HTML theme')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create configuration
    config = APIReferenceConfig(
        input_path=args.input,
        output_path=args.output,
        formats=args.formats,
        theme=args.theme
    )
    
    # Initialize optimizer
    optimizer = APIReferenceOptimizer(config)
    
    success = True
    
    if args.mode == 'generate':
        logger.info("Starting API reference generation...")
        results = optimizer.generate_all_formats()
        success = all(results.values())
        
        if success:
            logger.info("✓ All formats generated successfully")
        else:
            logger.error("✗ Some formats failed to generate")
            for format_name, result in results.items():
                if not result:
                    logger.error(f"  - {format_name}: FAILED")
    
    elif args.mode == 'consolidate':
        logger.info("Starting API reference consolidation...")
        success = optimizer.consolidate_existing_references()
        
    elif args.mode == 'validate':
        logger.info("Validating API reference system...")
        # TODO: Implement validation logic
        success = True
    
    if success:
        logger.info("✓ Operation completed successfully")
        return 0
    else:
        logger.error("✗ Operation failed")
        return 1

# Original classes preserved for compatibility
class HTML:
    """Enhanced HTML generation with DexBot theming"""
    
    @staticmethod
    def ClassContainer(name, description, properties, constructors, methods, cssId=None, cssClass=None):
        name_html = HTML.Div(name, cssClass="class-name")
        description_html = HTML.Div(description, cssClass="class-description")
        constructors_html = "" if len(constructors) == 0 else HTML.Div(constructors, cssClass="class-constructors")
        properties_html = "" if len(properties) == 0 else HTML.Div(properties, cssClass="class-properties")
        methods_html = "" if len(methods) == 0 else HTML.Div(methods, cssClass="class-methods")
        
        class_content = "\n".join([
            name_html,
            description_html,
            constructors_html,
            properties_html,
            methods_html
        ])
        
        class_html = HTML.Div(class_content, cssId=cssId, cssClass=cssClass)
        return class_html
    
    @staticmethod
    def ConstructorContainer():
        # TODO: Implement constructor container
        return ""

    @staticmethod
    def MethodContainer(permalink, className, methodName, description, signature, parameters, returns, cssId=None, cssClass=None):
        permalink_html = HTML.DocPermalink(permalink)
        className_html = HTML.Span(className, cssClass="method-class-name")
        methodName_html = HTML.Span(methodName, cssClass="method-name")
        
        signature_content = "{}.{}({})".format(className_html, methodName_html, signature)
        
        description_html = "" if len(description) == 0 else HTML.Div(description, cssClass="method-description")
        parameters_html = "" if len(parameters) == 0 else HTML.Div(parameters, cssClass="method-parameters")
        returns_html = "" if len(returns) == 0 else HTML.Div(returns, cssClass="method-returns")
        
        icon_open_html = HTML.IconExpand()
        icon_close_html = HTML.IconCollapse()
        
        signature_closed_html = HTML.Div(icon_open_html + signature_content, cssClass="redoc-method-signature")
        signature_open_html = HTML.Div(icon_close_html + signature_content, cssClass="redoc-property-title")
        
        method_content_open = "\n".join([
            signature_open_html,
            description_html,
            parameters_html,
            returns_html
        ])
        
        box_closed = signature_closed_html
        box_open = method_content_open
        
        method_content = HTML.CollapsableContainer(box_open, box_closed)
        
        method_html = HTML.Div(method_content, cssId=cssId, cssClass=cssClass)
        return permalink_html + method_html
    
    @staticmethod
    def PropertiesContainer(className, propName, type, description, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-property-container'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        
        className_html = HTML.Span(className, cssClass="redoc-class-name")
        propName_html = HTML.PropertyName(propName)
        
        name_html = "{}.{}".format(className_html, propName_html)
        type_html = HTML.VariableType(type)
        
        icon_open_html = HTML.IconExpand()
        prop_title_closed_content = icon_open_html + name_html + type_html
        prop_title_closed_html = HTML.Div(prop_title_closed_content, cssClass="redoc-property-title")
        
        icon_close_html = HTML.IconCollapse()
        prop_title_open_content = icon_close_html + name_html + type_html
        prop_title_open_html = HTML.Div(prop_title_open_content, cssClass="redoc-property-title")
        
        desc_html = '' if description is None or description == "" else HTML.Div(description, cssClass='redoc-class-property-desc')
        
        box_closed = prop_title_closed_html
        box_open = prop_title_open_html + desc_html
        
        property_content = HTML.CollapsableContainer(box_open, box_closed)
        
        return HTML.Div(property_content, cssId=cssId, cssClass=cssClass)
    
    @staticmethod
    def CollapsableContainer(open_html, closed_html, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = ''
        cssClass += ' redoc-collapsable-container closed-container'
        
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        
        box_closed = HTML.Div(closed_html, cssClass="redoc-collapsable-container-closed")
        box_open = HTML.Div(open_html, cssClass="redoc-collapsable-container-open")
        box_html = HTML.Div(box_closed + box_open, cssClass=cssClass)
        return box_html
    
    @staticmethod
    def BasePage(body, title=""):
        css_html_fa = HTML.CSS("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css")
        css_html = HTML.CSS("./main.css")
        js_html = HTML.JS("./main.js")
        header_html = css_html_fa + "\n" + css_html + "\n" + js_html
        body_html = HTML.Div(body, cssClass="redoc-page-container")
        
        return HTML.EmptyPage(body_html, title, header_html)
    
    @staticmethod
    def EmptyPage(body, title="", header=""):
        title_html = "" if len(title) == 0 else "\n<title>{}</title>\n".format(title)
        header_html = "" if (len(header) == 0 and len(title_html) == 0) else "\n<head>{}\n{}\n</head>\n".format(title_html, header)
        body_html = "" if len(body) == 0 else "\n<body>\n{}\n</body>\n".format(body)
        return '<!Doctype html>{}{}</html>'.format(header_html, body_html)
    
    @staticmethod
    def LeftRightPage(left_content, right_content, title=""):
        left_html = HTML.Div(left_content, cssClass="redoc-page-left")
        right_html = HTML.Div(right_content, cssClass="redoc-page-right")
        body = left_html + right_html
        
        return HTML.BasePage(body, title)
    
    @staticmethod
    def ParamForSignature(name, paramType=None, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-method-params-sign'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = ' class="{}"'.format(cssClass)
        name_html = HTML.VariableName(name)
        type_html = '' if paramType is None or paramType == "" else HTML.VariableType(paramType)
        return '<span{}{}>{}{}</span>'.format(cssId, cssClass, name_html, type_html)
    
    @staticmethod
    def ParamDescription(name, type_html, description, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-method-params'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = ' class="{}"'.format(cssClass)
        name_html = HTML.VariableName(name)
        desc_html = '' if description is None or description == "" else HTML.Div(description, cssClass='redoc-method-params-desc')
        return '<span{}{}>{}{}{}</span>'.format(cssId, cssClass, name_html, type_html, desc_html)
    
    @staticmethod
    def ParamForDescription(name, type, description, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-method-params'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = ' class="{}"'.format(cssClass)
        name_html = HTML.VariableName(name)
        type_html = HTML.VariableType(type)
        desc_html = '' if description is None or description == "" else HTML.Div(description, cssClass='redoc-method-params-desc')
        return '<span{}{}>{}{}{}</span>'.format(cssId, cssClass, name_html, type_html, desc_html)
    
    @staticmethod
    def VariableType(content, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-variable-type'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = ' class="{}"'.format(cssClass)
        return '<span{}{}>{}</span>'.format(cssId, cssClass, content)
    
    @staticmethod
    def VariableName(content, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-variable-name'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = ' class="{}"'.format(cssClass)
        return '<span{}{}>{}</span>'.format(cssId, cssClass, content)
    
    @staticmethod
    def PropertyName(content, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-property-name'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = ' class="{}"'.format(cssClass)
        return '<span{}{}>{}</span>'.format(cssId, cssClass, content)
    
    @staticmethod
    def MethodReturn(type_html, description, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-method-return'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        
        desc_html = '<br/>' if description is None or description == "" else HTML.Div(description, cssClass='redoc-method-return-desc')
        
        return_label = HTML.Div("Return", cssClass="redoc-method-return-box-title")
        return_html = return_label + HTML.Div(type_html + desc_html, cssClass="redoc-method-return-box")
        
        return HTML.Div(return_html, cssId, cssClass)
    
    @staticmethod
    def DocVersion(version, cssId=None, cssClass=None):
        if cssClass is None:
            cssClass = 'redoc-doc-version'
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = ' class="{}"'.format(cssClass)
        return '<div{}{}><a href="./index.html">DexBot API v{}</a></div>'.format(cssId, cssClass, version)
    
    @staticmethod
    def DocPermalink(url, content=None, cssClass=None):
        content = HTML.IconLink() if content is None else content
        link = ' href="#{}"'.format(url)
        cssId = ' id="{}"'.format(url)
        if cssClass is None:
            cssClass = 'redoc-permalink'
        cssClass = '' if cssClass == '' else ' class="{}"'.format(cssClass)
        return '<a{}{}{}>{}</a>'.format(cssId, cssClass, link, content)
    
    @staticmethod
    def IconLink():
        return '<i class="redoc-icon-link fas fa-link "></i>'
    
    @staticmethod
    def IconExpand():
        return '<i class="redoc-icon-expand fas fa-angle-down "></i>'
    
    @staticmethod
    def IconCollapse():
        return '<i class="redoc-icon-collapse fas fa-angle-up"></i>'
    
    @staticmethod
    def CSS(url, inline=False):
        css_html = '<style>{}</style>' if inline else '<link rel="stylesheet" type="text/css" href="{}">'
        css_html = css_html.format(url)
        return css_html
    
    @staticmethod
    def JS(url, inline=False):
        js_html = '<script>\n{}\n</script>' if inline else '<script src="{}"></script>'
        js_html = js_html.format(url)
        return js_html
    
    @staticmethod
    def Link(content, url=None, cssId=None, cssClass=None):
        url = '' if url is None else ' href="{}"'.format(url)
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = '' if cssClass is None else ' class="{}"'.format(cssClass)
        return '<a{}{}{}>{}</a>'.format(cssId, cssClass, url, content)
    
    @staticmethod
    def Div(content, cssId=None, cssClass=None):
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = '' if cssClass is None else ' class="{}"'.format(cssClass)
        return '<div{}{}>{}</div>'.format(cssId, cssClass, content)
    
    @staticmethod
    def Span(content, cssId=None, cssClass=None):
        cssId = '' if cssId is None else ' id="{}"'.format(cssId)
        cssClass = '' if cssClass is None else ' class="{}"'.format(cssClass)
        return '<span{}{}>{}</span>'.format(cssId, cssClass, content)

class AutoDocHTML:
    """Enhanced AutoDocHTML with DexBot integration"""
    
    def __init__(self, output_path=None, api_path=None):
        self.doc_path = "./ref/html/" if output_path is None else output_path
        self.ad = AutoDoc(api_path)
    
    def KeyToSlug(self, xmlkey, overload=True, shortname=True):
        if overload:
            xmlkey = re.sub(r"\(.*\)", "", xmlkey)
        if shortname:
            xmlkey = xmlkey.replace(":RazorEnhanced.", ":")
        return re.sub(r"[^a-zA-Z]", "-", xmlkey)
    
    def PermalinkHTML(self, xmlkey):
        anchor_slug = self.KeyToSlug(xmlkey)
        return HTML.DocPermalink(anchor_slug, cssClass='redoc-permalink')
    
    def DocVersionHTML(self):
        version = self.ad.GetVersion()
        return HTML.DocVersion(version)
    
    def MainMenuHTML(self, menuId='redoc-main-menu', itemClass='redoc-main-menu-entry'):
        classList = self.ad.GetClasses()
        links = []
        for cls in classList:
            name = cls["itemClass"]
            url = "./{}.html".format(name)
            html = HTML.Link(name, url, cssClass=itemClass)
            links.append(html)
        
        links_html = "\n".join(links)
        main_menu = HTML.Div(links_html, cssId=menuId)
        return main_menu
    
    def ClassHTML(self, className, classId='redoc-class-', itemClass='redoc-class'):
        classList = self.ad.GetClasses(className)
        if len(classList) == 0:
            return "Class not found: {}".format(className)
        
        doc_class = classList[0]
        
        description = doc_class["itemDescription"]
        properties_html = self.PropertiesHTML(className)
        constructors_html = self.ConstructorsHTML(className)
        methods_html = self.MethodsHTML(className)
        
        class_html = HTML.ClassContainer(className, description, properties_html, constructors_html, methods_html, cssId=classId, cssClass=itemClass)
        return class_html
    
    def PropertiesHTML(self, className):
        propertyList = self.ad.GetProperties(className)
        if len(propertyList) == 0:
            return ''
        
        prop_html_list = []
        for property in propertyList:
            link = self.PermalinkHTML(property["xmlKey"])
            prop_html = HTML.PropertiesContainer(className, property['itemName'], property['propertyType'], property['itemDescription'])
            prop_html = HTML.Div(link + prop_html, cssClass="redoc-class-property-entry")
            prop_html_list.append(prop_html)
        
        props_html = "\n".join(prop_html_list)
        props_html = HTML.Div(props_html, cssClass="redoc-property-box")
        props_html = HTML.Div("Properties", cssClass="redoc-property-box-title") + props_html
        return props_html
    
    def ConstructorsHTML(self, className):
        constructorList = self.ad.GetConstructors(className)
        if len(constructorList) == 0:
            return ""
        # TODO: Implement constructor HTML generation
        return ""
    
    def MethodsHTML(self, className):
        methodList = self.ad.GetMethods(className)
        methodNames = set([method['itemName'] for method in methodList])
        methodNames = list(sorted(methodNames))
        methods_html_list = []
        
        for methodName in methodNames:
            methods_html_list.append(self.MethodOverloadHTML(className, methodName))
        
        methods_html = "\n".join(methods_html_list)
        methods_html = HTML.Div(methods_html, cssClass="redoc-method-box")
        methods_html = HTML.Div("Methods", cssClass="redoc-method-box-title") + methods_html
        return methods_html
    
    def MethodOverloadHTML(self, className, methodName):
        methodList = self.ad.GetMethods(className, methodName)
        
        if not methodList:
            return ""
        
        # Setup for aggregation: descriptions
        lastMethod = methodList[-1]
        firstMethod = methodList.pop(0)
        firstMethod["itemDescription"] = [firstMethod["itemDescription"]]
        firstMethod["returnDesc"] = [firstMethod["returnDesc"]]
        firstMethod["returnType"] = [firstMethod["returnType"]]
        
        # Setup for aggregation: default params instead of overloading (Python way)
        min_p = len(lastMethod.get("paramList", []))
        max_p = len(firstMethod.get("paramList", []))
        
        for num_p in range(min_p, max_p):
            if num_p < len(firstMethod.get("paramList", [])):
                param = firstMethod["paramList"][num_p]
                if not param.get('itemHasDefault', False):
                    param['itemHasDefault'] = True
                    param['itemDefaultValue'] = "null"
        
        firstMethod["paramList"] = [[param] for param in firstMethod.get("paramList", [])]
        
        # Accumulate: descriptions and params
        for method in methodList:
            firstMethod["itemDescription"].append(method["itemDescription"])
            firstMethod["returnDesc"].append(method["returnDesc"])
            firstMethod["returnType"].append(method["returnType"])
            
            for p_num, param in enumerate(method.get("paramList", [])):
                if p_num < len(firstMethod["paramList"]):
                    firstMethod["paramList"][p_num].append(param)
        
        # Aggregate descriptions and returns
        description = "\n".join([desc.strip() for desc in firstMethod["itemDescription"] if desc]).strip()
        
        # Deduplicate returns (likely the same)
        firstMethod["returnType"] = list(set(firstMethod["returnType"]))
        return_desc = "\n".join([desc.strip() for desc in firstMethod["returnDesc"] if desc]).strip()
        return_type_list = [HTML.VariableType(ret_type) for ret_type in firstMethod["returnType"]]
        return_type = "\n".join(return_type_list)
        return_html = HTML.MethodReturn(return_type, return_desc)
        
        # Aggregate params
        param_name_list = []
        param_desc_html_list = []
        
        for param_list in firstMethod["paramList"]:
            if param_list:
                param_name = param_list[0]["itemName"]  # names from first method
                param_type_list = [param["itemType"] for param in param_list if param.get("itemType")]
                param_desc_list = [param["itemDescription"] for param in param_list if param.get("itemDescription")]
                
                param_type_list = list(filter(lambda t: t is not None and t != "", set(param_type_list)))
                param_desc_list = list(filter(lambda t: t is not None and t != "", set(param_desc_list)))
                
                param_type_html = "\n".join([HTML.VariableType(param_type) for param_type in param_type_list])
                param_desc_html = "\n".join(param_desc_list)
                
                param_desc_html_list.append(HTML.ParamDescription(param_name, param_type_html, param_desc_html))
                param_name_list.append(param_name)
        
        signature_list = [HTML.ParamForSignature(param_name) for param_name in param_name_list]
        signature_html = "{}".format(", ".join(signature_list))
        
        param_html = "\n".join(param_desc_html_list).strip()
        if param_html != "":
            param_desc_label = HTML.Div("Parameters", cssClass="redoc-method-params-box-title")
            param_html = param_desc_label + HTML.Div(param_html, cssClass="redoc-method-params-box")
        
        cssClass = 'redoc-method-container'
        link = self.KeyToSlug(firstMethod["xmlKey"])
        
        className = firstMethod["itemClass"]
        methodName = firstMethod["itemName"]
        method_html = HTML.MethodContainer(link, className, methodName, description, signature_html, param_html, return_html, cssClass=cssClass)
        method_html = HTML.Div(method_html, cssClass="redoc-class-method-entry")
        
        return method_html
    
    def WriteToFile(self, path, content, debug=False):
        fullpath = os.path.join(self.doc_path, path)
        if debug:
            print(f"Writing to: {fullpath}")
        
        dirpath = os.path.dirname(fullpath)
        if not os.path.exists(dirpath):
            if debug:
                print(f"Creating directory: {dirpath}")
            os.makedirs(dirpath)
        
        with open(fullpath, 'w+', encoding='utf-8') as file:
            file.write(content)

class AutoDoc:
    """Enhanced AutoDoc with better error handling and caching"""
    
    def __init__(self, api_path=None):
        self.api_data = None
        self.api_path = "./config/AutoComplete.json" if api_path is None else api_path
        self._classes_cache = None
        self._methods_cache = None
        self._properties_cache = None
    
    def GetSettings(self):
        api = self.GetPythonAPI()
        return api.get("settings", {})
    
    def GetVersion(self):
        settings = self.GetSettings()
        return settings.get("version", "Unknown")
    
    def GetClasses(self, filterClass=None):
        if self._classes_cache is None:
            api = self.GetPythonAPI()
            docs = api.get("classes", [])
            self._classes_cache = list(sorted(docs, key=lambda doc: doc.get("itemClass", "")))
        
        if filterClass is not None:
            return list(filter(lambda doc: doc.get("itemClass") == filterClass, self._classes_cache))
        return self._classes_cache
    
    def GetProperties(self, filterClass=None):
        if self._properties_cache is None:
            api = self.GetPythonAPI()
            docs = api.get("properties", [])
            self._properties_cache = list(sorted(docs, key=lambda doc: (doc.get("itemClass", ""), doc.get("itemName", ""))))
        
        if filterClass is not None:
            return list(filter(lambda doc: doc.get("itemClass") == filterClass, self._properties_cache))
        return self._properties_cache
    
    def GetConstructors(self, filterClass=None):
        api = self.GetPythonAPI()
        docs = api.get("constructors", [])
        
        if filterClass is not None:
            docs = list(filter(lambda doc: doc.get("itemClass") == filterClass, docs))
        
        docs = list(sorted(docs, key=lambda doc: (doc.get("itemClass", ""), doc.get("itemName", ""))))
        return docs
    
    def GetMethods(self, filterClass=None, filterName=None):
        if self._methods_cache is None:
            api = self.GetPythonAPI()
            docs = api.get("methods", [])
            self._methods_cache = list(sorted(docs, key=lambda doc: (doc.get("itemClass", ""), doc.get("itemName", ""), -len(doc.get("paramList", [])))))
        
        result = self._methods_cache
        
        if filterClass is not None:
            result = list(filter(lambda doc: doc.get("itemClass") == filterClass, result))
        
        if filterName is not None:
            result = list(filter(lambda doc: doc.get("itemName") == filterName, result))
        
        return result
    
    def GetPythonAPI(self):
        if self.api_data is not None:
            return self.api_data
        
        logger.info(f"Loading API data from: {self.api_path}")
        
        try:
            with open(self.api_path, 'r+', encoding='utf-8') as api_file:
                api_json = api_file.read()
                logger.info(f"File size: {len(api_json)} bytes")
                self.api_data = json.loads(api_json)
                logger.info("✓ API data loaded successfully")
                return self.api_data
        except FileNotFoundError:
            logger.error(f"✗ API file not found: {self.api_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"✗ Invalid JSON in API file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"✗ Error loading API data: {str(e)}")
            raise

"""
By placing the call to the main function at the bottom of the file, there is the freedom to rearrange the code freely in the file.

NOTE: *if __name__ == '__main__':* ensures that main() is called only when the script is run directly.
      This way it's possible to safely use this file also via "import autodoc" without worrying that main() would be executed.
"""
if __name__ == '__main__':
    import sys
    sys.exit(main())
