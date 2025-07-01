# DexBot API Reference Optimization System (TECH-001)

This directory contains the complete API Reference Optimization System for DexBot, implementing TECH-001 requirements.

## Overview

The API Reference Optimization System provides:

- **Multi-format documentation generation** (HTML, Markdown, JSON)
- **Automated consolidation** of existing API references
- **Enhanced metadata extraction** and processing
- **Integration with DexBot invoke tasks**
- **Manual data extraction** from RazorEnhanced

## Quick Start

### 1. Extract API Data from RazorEnhanced

First, you need to extract the API data from your RazorEnhanced installation:

#### Option A: Python Script (Recommended)
```bash
# Run the extraction script with default paths
python scripts/extract_razor_api_data.py

# Or specify custom paths
python scripts/extract_razor_api_data.py --input "C:/Path/To/RazorEnhanced/Config/AutoComplete.json" --output "./api_export/"

# Enable verbose output
python scripts/extract_razor_api_data.py --verbose
```

The script will:
- Read AutoComplete.json from RazorEnhanced
- Extract and analyze API metadata
- Generate comprehensive reports
- Export data in multiple formats

#### Option B: Automatic Fetch
```bash
# Auto-detect and copy from RazorEnhanced installation
invoke fetch-razor-api-data

# Or specify custom paths
invoke fetch-razor-api-data --razor-path "C:/Path/To/RazorEnhanced/Config/" --output-path "./Config/"
```

### 2. Generate API Documentation

```bash
# Generate all formats (HTML, Markdown, JSON)
invoke generate-api-reference

# Generate specific format
invoke generate-api-reference --format html
invoke generate-api-reference --format markdown
invoke generate-api-reference --format json

# Generate multiple formats
invoke generate-api-reference --format "html,markdown"
```

### 3. Complete Workflow

```bash
# Run the complete optimization workflow
invoke api-reference-workflow
```

This will:
1. Consolidate existing API references
2. Generate new documentation in all formats
3. Validate the system integrity

## Directory Structure

```
src/utils/
├── autodoc.py                 # Enhanced AutoDoc system with multi-format support
└── README.md                  # This file

scripts/
└── extract_razor_api_data.py  # Manual script for RazorEnhanced

Config/
└── AutoComplete.json          # API data from RazorEnhanced (copied here)

ref/                          # Generated documentation output
├── html/                     # HTML documentation
│   ├── index.html
│   ├── main.css
│   ├── main.js
│   └── *.html                # Individual class pages
├── markdown/                 # Markdown documentation
│   ├── README.md
│   └── *.md                  # Individual class pages
├── json/                     # JSON documentation
│   ├── api_reference.json
│   ├── search_index.json
│   └── classes/              # Individual class JSON files
└── consolidated/             # Consolidated existing references
    ├── consolidated_api_data.json
    └── consolidation_report.md
```

## Available Tasks

### Core Tasks

- `invoke generate-api-reference` - Generate API documentation
- `invoke consolidate-api-references` - Consolidate existing references
- `invoke validate-api-reference` - Validate system integrity
- `invoke api-reference-workflow` - Complete workflow
- `invoke fetch-razor-api-data` - Fetch data from RazorEnhanced

### Task Options

#### generate-api-reference
- `--format`: Output format(s) - "all", "html", "markdown", "json", or comma-separated
- `--input-path`: Path to AutoComplete.json (default: ./Config/AutoComplete.json)
- `--output-path`: Output directory (default: ./ref/)

#### consolidate-api-references
- `--output-path`: Output directory (default: ./ref/)

#### validate-api-reference
- `--input-path`: Path to AutoComplete.json (default: ./Config/AutoComplete.json)

#### fetch-razor-api-data
- `--razor-path`: Path to RazorEnhanced installation (auto-detected if not specified)
- `--output-path`: Where to save AutoComplete.json (default: ./Config/)

## Output Formats

### HTML Documentation
- **Location**: `ref/html/`
- **Features**: 
  - Modern responsive design with DexBot theming
  - Interactive collapsible sections
  - Search functionality
  - Cross-references and permalinks
  - Font Awesome icons

### Markdown Documentation
- **Location**: `ref/markdown/`
- **Features**:
  - GitHub/GitLab compatible
  - Cross-references between classes
  - Code syntax highlighting
  - Table of contents

### JSON Documentation
- **Location**: `ref/json/`
- **Features**:
  - Complete API data in structured format
  - Search index for quick lookups
  - Individual class files
  - Metadata and statistics

## Manual Script Usage

The script `scripts/extract_razor_api_data.py` is a standalone Python script for extracting API data:

### Basic Usage
```bash
# Run with default settings
python scripts/extract_razor_api_data.py

# Specify input file
python scripts/extract_razor_api_data.py --input "C:/RazorEnhanced/Config/AutoComplete.json"

# Specify output directory
python scripts/extract_razor_api_data.py --output "./my_api_export/"

# Enable verbose output
python scripts/extract_razor_api_data.py --verbose
```

### Command Line Options
- `--input, -i`: Path to AutoComplete.json file (default: ./Config/AutoComplete.json)
- `--output, -o`: Output directory (default: ./reports/api_extraction/)
- `--verbose, -v`: Enable verbose output
- `--help, -h`: Show help message

### Script Output Files

- `AutoComplete_Export.json` - Complete API data (copy to `Config/AutoComplete.json`)
- `API_Metadata.json` - Extracted metadata and statistics
- `API_Extraction_Report.md` - Detailed extraction report
- `Class_List.txt` - Simple list of all classes
- `Method_Signatures.txt` - All method signatures

## Integration with DexBot Systems

### Configuration Management
The system integrates with DexBot's configuration system through:
- `APIReferenceConfig` class for centralized settings
- Command-line argument support
- Environment variable support (planned)

### Logging and Error Handling
- Comprehensive logging with different levels
- Graceful error handling with detailed error messages
- Progress reporting during generation

### Caching and Performance
- In-memory caching of parsed API data
- Lazy loading of large datasets
- Optimized file I/O operations

## Customization

### HTML Theming
The HTML output uses a customizable theme system:

1. **Theme Configuration**: Modify `HTMLGenerator._load_theme()` in `autodoc.py`
2. **CSS Customization**: Edit the generated `main.css` or override in `_generate_theme_css()`
3. **JavaScript Features**: Enhance interactivity in `_generate_theme_js()`

### Output Formats
To add new output formats:

1. Create a new generator class (e.g., `PDFGenerator`)
2. Implement the `generate(autodoc)` method
3. Register in `APIReferenceOptimizer.generators`
4. Add format option to command-line arguments

### Data Processing
To customize data extraction:

1. Override methods in the `AutoDoc` class
2. Add custom filters and processors
3. Enhance metadata extraction in generators

## Troubleshooting

### Common Issues

#### AutoComplete.json Not Found
```bash
# Check if file exists
ls -la Config/AutoComplete.json

# Fetch from RazorEnhanced
invoke fetch-razor-api-data
```

#### Permission Errors
```bash
# Ensure output directory is writable
chmod 755 ref/

# Run with elevated permissions if needed (Windows)
# Run PowerShell as Administrator
```

#### Memory Issues with Large Files
```bash
# Monitor memory usage
# Consider processing in chunks for very large API files
# Increase system memory if possible
```

### Debug Mode
```bash
# Run with debug logging
python src/utils/autodoc.py --debug

# Or with invoke
invoke generate-api-reference --debug
```

### Validation
```bash
# Validate generated files
invoke validate-api-reference

# Check file integrity
find ref/ -name "*.json" -exec python -m json.tool {} \; > /dev/null
```

## Contributing

### Adding Features
1. Follow the existing code structure
2. Add appropriate logging and error handling
3. Include tests for new functionality
4. Update documentation

### Reporting Issues
When reporting issues, include:
- Command that failed
- Error messages and stack traces
- System information (OS, Python version)
- Size and source of AutoComplete.json

## Performance Optimization

### Large API Files
- The system is optimized for RazorEnhanced's API size (~1-5MB)
- For larger files, consider implementing streaming processors
- Monitor memory usage during generation

### Generation Speed
- HTML generation: ~5-10 seconds
- Markdown generation: ~2-5 seconds  
- JSON generation: ~1-3 seconds
- Complete workflow: ~10-20 seconds

### Caching
- API data is cached in memory during processing
- Generated files are cached until source changes
- Clear cache by restarting the process

## Future Enhancements

See `docs/prds/TECH-001_Implementation_Tasks.md` for planned improvements:

- PDF generation support
- Interactive API explorer
- VS Code extension integration
- Automated API change detection
- Performance benchmarking
- Multi-language support

## License

This system is part of the DexBot project and follows the same license terms.

## Support

For support with the API Reference Optimization System:

1. Check this README for common solutions
2. Review the implementation tasks in `docs/prds/TECH-001_Implementation_Tasks.md`
3. Check existing issues in the project repository
4. Create a new issue with detailed information

---

**TECH-001 API Reference Optimization System**  
*Reducing technical debt, improving developer experience*
