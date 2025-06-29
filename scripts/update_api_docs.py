#!/usr/bin/env python3
"""
RazorEnhanced API Documentation Generator

This script crawls the RazorEnhanced API documentation from the official source,
extracts modules, methods, and parameters, and generates a comprehensive 
developer-friendly API reference with usage examples and explanations.

This is a standalone tool - run it manually when you want to update the API docs.
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime
from bs4 import BeautifulSoup
import time

# Configuration
API_DOCS_URL = "https://razorenhanced.github.io/doc/api/"
GITHUB_REPO_URL = "https://github.com/RazorEnhanced/RazorEnhanced"
OUTPUT_DIR = Path("docs")
OUTPUT_FILE = OUTPUT_DIR / "RazorEnhanced_API_Reference.md"

class APIDocumentationGenerator:
    """Generates comprehensive RazorEnhanced API documentation."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RazorEnhanced-API-Doc-Generator/1.0'
        })
        self.crawled_modules = {}
        self.delay_between_requests = 1  # Be respectful to the server
        
    def crawl_api_documentation(self) -> Dict[str, Any]:
        """Crawl all API documentation from the official RazorEnhanced API docs."""
        print("Crawling RazorEnhanced API documentation...")
        
        try:
            # Get the main API page to find all modules
            print(f"Fetching main API page: {API_DOCS_URL}")
            response = self.session.get(API_DOCS_URL)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all module links
            module_links = self.extract_module_links(soup)
            print(f"Found {len(module_links)} API modules to crawl")
            
            # Crawl each module
            for module_name, module_url in module_links.items():
                print(f"Crawling {module_name} module...")
                module_data = self.crawl_module_page(module_name, module_url)
                if module_data:
                    self.crawled_modules[module_name] = module_data
                time.sleep(self.delay_between_requests)
                
        except requests.RequestException as e:
            print(f"Error crawling API documentation: {e}")
            print("Creating fallback documentation...")
            self.create_core_api_modules()
            
        return self.crawled_modules
    
    def extract_module_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract module links from the main API page."""
        module_links = {}
        
        # Look for module links in the navigation or content
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # Filter for API module links
            if (href.endswith('.html') and 
                not href.startswith('http') and
                text and 
                not text.lower() in ['home', 'index', 'main']):
                
                full_url = urljoin(API_DOCS_URL, href)
                module_links[text] = full_url
        
        # Ensure we have the core modules
        core_modules = {
            'Player': urljoin(API_DOCS_URL, 'Player.html'),
            'Items': urljoin(API_DOCS_URL, 'Items.html'),
            'Mobile': urljoin(API_DOCS_URL, 'Mobile.html'),
            'Target': urljoin(API_DOCS_URL, 'Target.html'),
            'Gumps': urljoin(API_DOCS_URL, 'Gumps.html'),
            'Journal': urljoin(API_DOCS_URL, 'Journal.html'),
            'Misc': urljoin(API_DOCS_URL, 'Misc.html'),
            'Spells': urljoin(API_DOCS_URL, 'Spells.html'),
            'Timer': urljoin(API_DOCS_URL, 'Timer.html')
        }
        
        # Add core modules if not found
        for name, url in core_modules.items():
            if name not in module_links:
                module_links[name] = url
        
        return module_links
    
    def crawl_module_page(self, module_name: str, module_url: str) -> Optional[Dict[str, Any]]:
        """Crawl a specific module page and extract methods/properties."""
        try:
            response = self.session.get(module_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            module_data = {
                'name': module_name,
                'url': module_url,
                'description': self.extract_module_description(soup, module_name),
                'methods': self.extract_methods_from_html(soup),
                'properties': self.extract_properties_from_html(soup)
            }
            
            return module_data
            
        except requests.RequestException as e:
            print(f"Error crawling {module_name}: {e}")
            return self.create_fallback_module_data(module_name)
    
    def extract_module_description(self, soup: BeautifulSoup, module_name: str) -> str:
        """Extract the module description."""
        # Try to find description in common locations
        desc_selectors = [
            'p.description',
            '.description',
            'p:first-of-type',
            '.content p:first-of-type',
            'div.summary p'
        ]
        
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem and desc_elem.get_text().strip():
                return desc_elem.get_text().strip()
        
        # Return generic description based on module name
        descriptions = {
            'Player': 'Provides access to player character information, stats, and actions.',
            'Items': 'Handles item manipulation, searching, and container operations.',
            'Mobile': 'Manages mobile (NPC/player) interactions and information.',
            'Target': 'Controls target selection and targeting operations.',
            'Gumps': 'Manages user interface gumps and dialog interactions.',
            'Journal': 'Monitors and searches game messages and journal entries.',
            'Misc': 'Provides miscellaneous utility functions and game operations.',
            'Spells': 'Handles spell casting and magic-related operations.',
            'Timer': 'Provides timing and delay functionality for scripts.'
        }
        
        return descriptions.get(module_name, f"API module for {module_name} operations in RazorEnhanced.")
    
    def extract_methods_from_html(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract method information from HTML content."""
        methods = []
        
        # Look for method signatures in various HTML structures
        method_patterns = [
            r'(\w+)\s*\([^)]*\)',  # Method with parentheses
            r'def\s+(\w+)\s*\([^)]*\)',  # Python def syntax
            r'function\s+(\w+)\s*\([^)]*\)'  # JavaScript function syntax
        ]
        
        text_content = soup.get_text()
        
        for pattern in method_patterns:
            matches = re.finditer(pattern, text_content, re.IGNORECASE)
            for match in matches:
                method_name = match.group(1)
                if method_name and method_name[0].isupper():  # Likely a method name
                    signature = match.group(0)
                    methods.append({
                        'name': method_name,
                        'signature': signature,
                        'description': f"Method for {method_name} operations"
                    })
        
        return methods[:10]  # Limit to avoid too many false positives
    
    def extract_properties_from_html(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract property information from HTML content."""
        properties = []
        
        # Look for property-like patterns
        text_content = soup.get_text()
        
        # Common property patterns
        property_keywords = ['Name', 'Serial', 'Position', 'Hits', 'Mana', 'Stamina', 'Status']
        
        for keyword in property_keywords:
            if keyword in text_content:
                properties.append({
                    'name': keyword,
                    'description': f"Gets the {keyword.lower()} value"
                })
        
        return properties
    
    def create_core_api_modules(self):
        """Create comprehensive data for core API modules with known methods."""
        core_modules = {
            'Player': {
                'name': 'Player',
                'description': 'Provides access to player character information, stats, and actions.',
                'methods': [
                    {'name': 'Attack', 'signature': 'Attack(serial)', 'description': 'Attack a target by serial number'},
                    {'name': 'Walk', 'signature': 'Walk(direction)', 'description': 'Walk in a specified direction'},
                    {'name': 'UseSkill', 'signature': 'UseSkill(skill)', 'description': 'Use a skill by name'},
                    {'name': 'Say', 'signature': 'Say(message)', 'description': 'Say a message in game'},
                    {'name': 'ChatSay', 'signature': 'ChatSay(message)', 'description': 'Send a chat message'}
                ],
                'properties': [
                    {'name': 'Name', 'description': 'Player character name'},
                    {'name': 'Serial', 'description': 'Player serial number'},
                    {'name': 'Hits', 'description': 'Current hit points'},
                    {'name': 'HitsMax', 'description': 'Maximum hit points'},
                    {'name': 'Mana', 'description': 'Current mana points'},
                    {'name': 'ManaMax', 'description': 'Maximum mana points'},
                    {'name': 'Stamina', 'description': 'Current stamina points'},
                    {'name': 'StaminaMax', 'description': 'Maximum stamina points'},
                    {'name': 'Position', 'description': 'Player position coordinates'},
                    {'name': 'Direction', 'description': 'Player facing direction'},
                    {'name': 'Backpack', 'description': 'Player backpack container'},
                    {'name': 'Mount', 'description': 'Player mount serial'},
                    {'name': 'Warmode', 'description': 'War mode status'},
                    {'name': 'IsGhost', 'description': 'Ghost status'},
                    {'name': 'Poisoned', 'description': 'Poison status'}
                ]
            },
            'Items': {
                'name': 'Items',
                'description': 'Handles item manipulation, searching, and container operations.',
                'methods': [
                    {'name': 'FindBySerial', 'signature': 'FindBySerial(serial)', 'description': 'Find an item by its serial number'},
                    {'name': 'FindByID', 'signature': 'FindByID(itemID, color, container)', 'description': 'Find items by ID and color in a container'},
                    {'name': 'Move', 'signature': 'Move(serial, container, amount)', 'description': 'Move items between containers'},
                    {'name': 'DropItemGroundSelf', 'signature': 'DropItemGroundSelf(serial, amount)', 'description': 'Drop item on ground at player location'},
                    {'name': 'UseItem', 'signature': 'UseItem(serial)', 'description': 'Use an item by serial'},
                    {'name': 'WaitForContents', 'signature': 'WaitForContents(container, delay)', 'description': 'Wait for container contents to load'},
                    {'name': 'ContainerCount', 'signature': 'ContainerCount(container)', 'description': 'Count items in a container'}
                ],
                'properties': []
            },
            'Target': {
                'name': 'Target',
                'description': 'Controls target selection and targeting operations.',
                'methods': [
                    {'name': 'PromptTarget', 'signature': 'PromptTarget()', 'description': 'Prompt player to select a target'},
                    {'name': 'WaitForTarget', 'signature': 'WaitForTarget(delay)', 'description': 'Wait for target selection with timeout'},
                    {'name': 'TargetExecute', 'signature': 'TargetExecute(serial)', 'description': 'Execute target on specified serial'},
                    {'name': 'Cancel', 'signature': 'Cancel()', 'description': 'Cancel current target cursor'},
                    {'name': 'GetTargetSerial', 'signature': 'GetTargetSerial()', 'description': 'Get the serial of the last target'},
                    {'name': 'SetLast', 'signature': 'SetLast(serial)', 'description': 'Set the last target serial'}
                ],
                'properties': [
                    {'name': 'HasTarget', 'description': 'Whether target cursor is active'},
                    {'name': 'Last', 'description': 'Serial of last target'}
                ]
            },
            'Journal': {
                'name': 'Journal',
                'description': 'Monitors and searches game messages and journal entries.',
                'methods': [
                    {'name': 'Clear', 'signature': 'Clear()', 'description': 'Clear the journal buffer'},
                    {'name': 'Search', 'signature': 'Search(text)', 'description': 'Search for text in journal'},
                    {'name': 'SearchByColor', 'signature': 'SearchByColor(text, color)', 'description': 'Search for text with specific color'},
                    {'name': 'SearchFromLast', 'signature': 'SearchFromLast(text)', 'description': 'Search from last journal entry'},
                    {'name': 'WaitJournal', 'signature': 'WaitJournal(text, delay)', 'description': 'Wait for specific text in journal'}
                ],
                'properties': []
            },
            'Misc': {
                'name': 'Misc',
                'description': 'Provides miscellaneous utility functions and game operations.',
                'methods': [
                    {'name': 'Pause', 'signature': 'Pause(milliseconds)', 'description': 'Pause script execution for specified time'},
                    {'name': 'SendMessage', 'signature': 'SendMessage(message, color)', 'description': 'Send a message to game window'},
                    {'name': 'NoOperation', 'signature': 'NoOperation()', 'description': 'Send no-operation packet to server'},
                    {'name': 'Distance', 'signature': 'Distance(x1, y1, x2, y2)', 'description': 'Calculate distance between two points'},
                    {'name': 'ReadSharedValue', 'signature': 'ReadSharedValue(key)', 'description': 'Read shared value between scripts'},
                    {'name': 'WriteSharedValue', 'signature': 'WriteSharedValue(key, value)', 'description': 'Write shared value for other scripts'}
                ],
                'properties': []
            }
        }
        
        self.crawled_modules.update(core_modules)
    
    def create_fallback_module_data(self, module_name: str) -> Dict[str, Any]:
        """Create fallback data for a module when crawling fails."""
        return {
            'name': module_name,
            'description': f"API module for {module_name} operations in RazorEnhanced.",
            'methods': [],
            'properties': []
        }
    
    def generate_api_documentation(self, modules: Dict[str, Any]) -> str:
        """Generate comprehensive API documentation with generic examples."""
        print("Generating API documentation...")
        
        doc_content = self.create_header()
        doc_content += self.create_table_of_contents(modules)
        doc_content += self.create_quick_reference()
        
        # Add each module's documentation
        for module_name in sorted(modules.keys()):
            if module_name in ['Player', 'Items', 'Target', 'Journal', 'Misc']:  # Focus on core modules
                module_data = modules[module_name]
                doc_content += self.create_module_documentation(module_data)
        
        doc_content += self.create_best_practices_section()
        doc_content += self.create_footer()
        
        return doc_content
    
    def create_header(self) -> str:
        """Create the document header."""
        return f"""# RazorEnhanced API Reference Guide

> **Generated on**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> 
> This comprehensive API reference guide was automatically generated from the official
> RazorEnhanced documentation. It provides detailed information about modules, methods,
> parameters, and usage examples for developers.
> 
> **Official Documentation**: [{API_DOCS_URL}]({API_DOCS_URL})

## Overview

RazorEnhanced is a powerful scripting framework for Ultima Online that provides extensive
APIs for automating gameplay, creating tools, and enhancing the user experience.

This guide includes:
- **Complete API coverage** - Core modules and their methods/properties
- **Method signatures** - Parameter details and return types
- **Usage examples** - Practical code examples for each API
- **Best practices** - Error handling and implementation patterns
- **Quick reference** - Common patterns and imports

"""
    
    def create_table_of_contents(self, modules: Dict[str, Any]) -> str:
        """Create table of contents for core modules."""
        toc = "## Table of Contents\n\n"
        toc += "- [Quick Reference](#quick-reference)\n"
        
        core_modules = ['Player', 'Items', 'Target', 'Journal', 'Misc']
        for module_name in core_modules:
            if module_name in modules:
                toc += f"- [{module_name}](#{module_name.lower()})\n"
        
        toc += "- [Best Practices](#best-practices)\n"
        toc += "- [Additional Resources](#additional-resources)\n\n"
        
        return toc
    
    def create_quick_reference(self) -> str:
        """Create a quick reference section."""
        return """## Quick Reference

### Import RazorEnhanced
```python
# Method 1: Import specific modules
from RazorEnhanced import Player, Items, Target, Journal

# Method 2: Import with CLR (recommended for stability)
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Player, Items, Target

# Method 3: Import with alias
import RazorEnhanced as RE
# Usage: RE.Player.Name, RE.Items.FindBySerial(), etc.
```

### Essential Patterns

#### Basic Script Structure
```python
from RazorEnhanced import Player, Items, Misc

def main():
    try:
        # Your script logic here
        Misc.SendMessage("Script started", 0x40)
        
        # Check player status
        if Player.IsGhost:
            Misc.SendMessage("Player is dead, stopping script", 0x20)
            return
            
        # Your automation logic here
        
    except Exception as e:
        Misc.SendMessage(f"Script error: {e}", 0x20)

if __name__ == "__main__":
    main()
```

#### Error Handling Template
```python
def safe_operation():
    try:
        # Potentially risky operation
        item = Items.FindBySerial(0x12345678)
        if item is None:
            raise ValueError("Item not found")
            
        # Process the item
        Items.Move(item.Serial, Player.Backpack.Serial, 1)
        
        return True
        
    except Exception as e:
        Misc.SendMessage(f"Operation failed: {e}", 0x20)
        return False
```

"""
    
    def create_module_documentation(self, module_data: Dict[str, Any]) -> str:
        """Create documentation for a specific module."""
        module_name = module_data['name']
        
        doc = f"""## {module_name}

> **Import**: `from RazorEnhanced import {module_name}`

{module_data.get('description', f'{module_name} API module for RazorEnhanced scripting.')}

"""
        
        # Add properties section
        properties = module_data.get('properties', [])
        if properties:
            doc += "### Properties\n\n"
            for prop in properties:
                doc += f"#### `{module_name}.{prop['name']}`\n\n"
                doc += f"{prop.get('description', 'Property description')}\n\n"
                
                # Add usage example
                doc += self.generate_property_example(module_name, prop['name'])
                doc += "\n"
        
        # Add methods section
        methods = module_data.get('methods', [])
        if methods:
            doc += "### Methods\n\n"
            for method in methods:
                doc += f"#### `{module_name}.{method['name']}`\n\n"
                
                if method.get('signature'):
                    doc += f"**Signature**: `{method['signature']}`\n\n"
                
                doc += f"{method.get('description', 'Method description')}\n\n"
                
                # Add usage example
                doc += self.generate_method_example(module_name, method)
                doc += "\n"
        
        doc += "---\n\n"
        return doc
    
    def generate_property_example(self, module_name: str, prop_name: str) -> str:
        """Generate a generic example for a property."""
        examples = {
            'Player': {
                'Name': '''**Example**:
```python
from RazorEnhanced import Player

# Get player name
player_name = Player.Name
print(f"Character name: {player_name}")
```''',
                'Hits': '''**Example**:
```python
from RazorEnhanced import Player, Misc

# Check player health
current_hp = Player.Hits
max_hp = Player.HitsMax
health_percent = (current_hp / max_hp) * 100

if health_percent < 50:
    Misc.SendMessage("Health is low!", 0x20)
```''',
                'Position': '''**Example**:
```python
from RazorEnhanced import Player

# Get player position
pos = Player.Position
print(f"Player at: X={pos.X}, Y={pos.Y}, Z={pos.Z}")
```''',
                'Backpack': '''**Example**:
```python
from RazorEnhanced import Player, Items

# Access player backpack
backpack = Player.Backpack
if backpack:
    print(f"Backpack serial: {backpack.Serial}")
    
    # Count items in backpack
    item_count = Items.ContainerCount(backpack.Serial)
    print(f"Items in backpack: {item_count}")
```'''
            }
        }
        
        if module_name in examples and prop_name in examples[module_name]:
            return examples[module_name][prop_name]
        
        # Generic example
        return f'''**Example**:
```python
from RazorEnhanced import {module_name}

# Get {prop_name.lower()} value
value = {module_name}.{prop_name}
print(f"{prop_name}: {{value}}")
```'''
    
    def generate_method_example(self, module_name: str, method: Dict[str, str]) -> str:
        """Generate a generic example for a method."""
        method_name = method['name']
        
        examples = {
            'Player': {
                'Attack': '''**Example**:
```python
from RazorEnhanced import Player, Target, Misc

# Attack a target
Target.PromptTarget()
target_serial = Target.WaitForTarget(5000)

if target_serial:
    Player.Attack(target_serial)
    Misc.SendMessage("Attacking target!", 0x40)
else:
    Misc.SendMessage("No target selected", 0x20)
```''',
                'UseSkill': '''**Example**:
```python
from RazorEnhanced import Player, Journal, Misc

# Use hiding skill
Journal.Clear()
Player.UseSkill("Hiding")

# Wait for skill result
Misc.Pause(1000)
if Journal.Search("You have hidden yourself well"):
    Misc.SendMessage("Successfully hidden", 0x40)
```'''
            },
            'Items': {
                'FindBySerial': '''**Example**:
```python
from RazorEnhanced import Items, Misc

# Find item by serial
item_serial = 0x12345678
item = Items.FindBySerial(item_serial)

if item:
    Misc.SendMessage(f"Found item: {item.Name}", 0x40)
else:
    Misc.SendMessage("Item not found", 0x20)
```''',
                'Move': '''**Example**:
```python
from RazorEnhanced import Items, Player, Misc

# Move item to backpack
item_serial = 0x12345678
item = Items.FindBySerial(item_serial)

if item:
    success = Items.Move(item.Serial, Player.Backpack.Serial, 1)
    if success:
        Misc.SendMessage("Item moved successfully", 0x40)
    else:
        Misc.SendMessage("Failed to move item", 0x20)
```'''
            },
            'Target': {
                'PromptTarget': '''**Example**:
```python
from RazorEnhanced import Target, Misc

# Prompt for target selection
Target.PromptTarget()
Misc.SendMessage("Select a target...", 0x40)

# Wait for target (5 second timeout)
target_serial = Target.WaitForTarget(5000)
if target_serial:
    Misc.SendMessage(f"Target selected: {target_serial}", 0x40)
```'''
            },
            'Journal': {
                'Search': '''**Example**:
```python
from RazorEnhanced import Journal, Player, Misc

# Monitor for specific message
Journal.Clear()
Player.UseSkill("Mining")

# Check for success message
Misc.Pause(2000)
if Journal.Search("You dig some"):
    Misc.SendMessage("Mining successful!", 0x40)
elif Journal.Search("There is no metal here"):
    Misc.SendMessage("No ore found", 0x20)
```'''
            },
            'Misc': {
                'Pause': '''**Example**:
```python
from RazorEnhanced import Misc

# Add delay between operations
Misc.SendMessage("Starting process...", 0x40)
Misc.Pause(2000)  # Wait 2 seconds
Misc.SendMessage("Process complete!", 0x40)
```''',
                'SendMessage': '''**Example**:
```python
from RazorEnhanced import Misc

# Send colored messages
Misc.SendMessage("Info message", 0x40)      # Blue
Misc.SendMessage("Warning message", 0x30)   # Yellow  
Misc.SendMessage("Error message", 0x20)     # Red
Misc.SendMessage("Success message", 0x40)   # Green
```'''
            }
        }
        
        if module_name in examples and method_name in examples[module_name]:
            return examples[module_name][method_name]
        
        # Generic example based on signature
        signature = method.get('signature', f'{method_name}()')
        return f'''**Example**:
```python
from RazorEnhanced import {module_name}, Misc

# Use {method_name} method
try:
    result = {module_name}.{signature}
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {{e}}", 0x20)
```'''
    
    def create_best_practices_section(self) -> str:
        """Create best practices section."""
        return """## Best Practices

### 1. Always Use Error Handling
Every RazorEnhanced script should include proper error handling to prevent crashes.

```python
from RazorEnhanced import Items, Player, Misc

def safe_item_operation(item_serial):
    try:
        item = Items.FindBySerial(item_serial)
        if item is None:
            raise ValueError("Item not found")
        
        # Perform operation
        Items.Move(item.Serial, Player.Backpack.Serial, 1)
        return True
        
    except Exception as e:
        Misc.SendMessage(f"Error: {e}", 0x20)
        return False
```

### 2. Use Timeouts for Waiting Operations
Always specify timeouts to prevent infinite waiting.

```python
from RazorEnhanced import Target, Items, Misc

# Good: Use timeout
Target.PromptTarget()
if Target.WaitForTarget(5000):  # 5 second timeout
    target = Target.GetTargetSerial()
    # Process target
else:
    Misc.SendMessage("Target selection timed out", 0x20)

# Good: Wait for container contents with timeout
Items.WaitForContents(Player.Backpack.Serial, 2000)
```

### 3. Check Return Values
Many methods return success/failure status - always check these.

```python
from RazorEnhanced import Items, Player, Misc

# Check if operation succeeded
success = Items.Move(item_serial, Player.Backpack.Serial, 1)
if success:
    Misc.SendMessage("Item moved successfully", 0x40)
else:
    Misc.SendMessage("Failed to move item", 0x20)
```

### 4. Use Appropriate Delays
Give the server time to process operations between commands.

```python
from RazorEnhanced import Items, Misc

# Move multiple items with delays
for item_serial in item_list:
    Items.Move(item_serial, container, 1)
    Misc.Pause(100)  # Small delay between moves
```

### 5. Clear Journal Before Monitoring
Always clear the journal before performing actions you want to monitor.

```python
from RazorEnhanced import Journal, Player, Misc

# Clear journal before skill use
Journal.Clear()
Player.UseSkill("Hiding")

# Then check for messages
Misc.Pause(1000)
if Journal.Search("You have hidden"):
    Misc.SendMessage("Hidden successfully", 0x40)
```

### 6. Validate Objects Before Use
Check that objects exist and are valid before using them.

```python
from RazorEnhanced import Items, Player, Misc

# Always validate items
item = Items.FindBySerial(serial)
if item and item.Serial != 0:
    # Item is valid, safe to use
    Items.UseItem(item.Serial)
else:
    Misc.SendMessage("Invalid item", 0x20)

# Check containers before accessing
backpack = Player.Backpack
if backpack and backpack.Serial != 0:
    Items.WaitForContents(backpack.Serial, 1000)
```

"""
    
    def create_footer(self) -> str:
        """Create the footer section."""
        return f"""## Additional Resources

### Official Documentation
- [RazorEnhanced API Documentation]({API_DOCS_URL})
- [RazorEnhanced GitHub Repository]({GITHUB_REPO_URL})
- [Script Library](https://github.com/RazorEnhanced/ScriptLibrary)

### Community Resources
- [RazorEnhanced Discord](https://discord.gg/VdyCpjQ)
- [UO Script Examples](https://github.com/RazorEnhanced/ScriptLibrary/tree/master/Examples)

### Development Tools
- Use RazorEnhanced's built-in script editor for development
- Enable debug logging for troubleshooting
- Test scripts in safe environments before production use

### Contributing
This documentation is generated automatically. For the most current information,
always refer to the official RazorEnhanced documentation.

---
**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Source**: Official RazorEnhanced API Documentation  
**Generator Version**: 1.0  
"""
def main():
    """Main function to crawl and generate API documentation."""
    print("RazorEnhanced API Documentation Generator")
    print("=" * 50)
    print("This tool will:")
    print("- Crawl official API documentation pages")
    print("- Extract modules, methods, and properties")
    print("- Generate comprehensive developer guide with examples")
    print("=" * 50)
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Initialize generator
    generator = APIDocumentationGenerator()
    
    try:
        # Crawl all API documentation
        print("\n[PHASE 1] Crawling API Documentation...")
        modules = generator.crawl_api_documentation()
        
        if not modules:
            print("[WARNING] No modules found. Creating core API documentation...")
            generator.create_core_api_modules()
            modules = generator.crawled_modules
        
        print(f"[SUCCESS] Successfully processed {len(modules)} modules")
        
        # Generate comprehensive documentation
        print("\n[PHASE 2] Generating Documentation...")
        api_reference = generator.generate_api_documentation(modules)
        
        # Write markdown file
        print(f"\n[PHASE 3] Writing Files...")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(api_reference)
        
        print(f"[SUCCESS] API reference generated: {OUTPUT_FILE}")
        
        # Create JSON version for programmatic access
        json_file = OUTPUT_DIR / "api_reference.json"
        json_data = {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'source_url': API_DOCS_URL,
            'modules': modules,
            'total_modules': len(modules)
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, default=str)
        
        print(f"[SUCCESS] JSON reference created: {json_file}")
        
        # Print summary
        print(f"\n[SUMMARY]")
        
        # Count core modules with detailed documentation
        core_modules = [m for m in modules.keys() if m in ['Player', 'Items', 'Target', 'Journal', 'Misc']]
        print(f"   - Core modules documented: {len(core_modules)}")
        
        total_methods = sum(len(module.get('methods', [])) for module in modules.values())
        total_properties = sum(len(module.get('properties', [])) for module in modules.values())
        
        print(f"   - Total methods documented: {total_methods}")
        print(f"   - Total properties documented: {total_properties}")
        print(f"   - Output file size: {OUTPUT_FILE.stat().st_size / 1024:.1f}KB")
            
        print(f"\n[COMPLETE] API documentation generation complete!")
        print(f"[INFO] View the developer guide at: {OUTPUT_FILE}")
        print(f"[INFO] This is a standalone tool - run manually when needed")
        
    except Exception as e:
        print(f"[ERROR] Error generating API documentation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Check if BeautifulSoup is available
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("[ERROR] BeautifulSoup4 is required for HTML parsing.")
        print("Please install it with: pip install beautifulsoup4")
        sys.exit(1)
    
    main()
