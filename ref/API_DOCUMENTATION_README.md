# API Documentation Files

This directory contains multiple API reference files for different purposes and RazorEnhanced versions.

## 📁 **File Overview**

### **Official RazorEnhanced References (v0.8.2.242):**
- **`AutoComplete.py`** (156 KB) - Complete Python type hints for IDE support and development
- **`AutoComplete.json`** (602 KB) - Complete API metadata with detailed method signatures and documentation

### **Project-Generated References (v0.8.2.245):**
- **`api_reference.json`** (71 KB) - Curated API subset with latest version compatibility info
- **`RazorEnhanced_API_Reference.md`** (30 KB) - Human-readable documentation with examples

### **Other References:**
- **`UO_ITEM_IDS_REFERENCE.md`** - Ultima Online item ID reference for development

## 🎯 **Usage Guide**

### **For Development:**
- **Primary**: Use `AutoComplete.py` for IDE type checking, IntelliSense, and error prevention
- **Secondary**: Reference `RazorEnhanced_API_Reference.md` for quick API lookup and examples

### **For Documentation:**
- **Human-readable**: Use `RazorEnhanced_API_Reference.md` for comprehensive API guide
- **Machine-readable**: Use `AutoComplete.json` for automated documentation generation

### **For Compatibility:**
- **Latest Version**: Check `api_reference.json` for v0.8.2.245 compatibility
- **Complete Coverage**: Fall back to `AutoComplete.*` files for comprehensive API surface

## 📊 **Version Information**

| File | Version | Lines | Size | Purpose |
|------|---------|-------|------|---------|
| `AutoComplete.py` | v0.8.2.242 | 7,879 | 156 KB | Type hints & IDE support |
| `AutoComplete.json` | v0.8.2.242 | 18,455 | 602 KB | Complete API metadata |
| `api_reference.json` | v0.8.2.245 | 2,262 | 71 KB | Latest version subset |
| `RazorEnhanced_API_Reference.md` | v0.8.2.245 | 1,390 | 30 KB | Human-readable docs |

## ⚠️ **Version Notes**

- **Minor Differences**: v0.8.2.242 vs v0.8.2.245 have minimal API changes
- **Core Stability**: Essential APIs (Items, Player, Mobiles, etc.) are stable between versions
- **Development Strategy**: Use complete docs (v0.8.2.242) for development, verify against latest version when needed
- **Compatibility**: All methods used in DexBot are available in both versions

## 🚀 **Development Workflow**

1. **IDE Setup**: Import `AutoComplete.py` types for full IntelliSense support
2. **API Discovery**: Browse `RazorEnhanced_API_Reference.md` for method examples
3. **Implementation**: Use type hints from `AutoComplete.py` to catch errors early
4. **Validation**: Cross-reference `api_reference.json` for latest version compatibility
5. **Documentation**: Reference both files when documenting API usage patterns

## 📈 **Benefits**

- **Type Safety**: Complete type hints prevent runtime API errors
- **IDE Support**: Full autocompletion and parameter hints
- **Documentation**: Multiple formats for different use cases
- **Version Coverage**: Support for both current and latest RazorEnhanced versions
- **Development Speed**: Faster coding with comprehensive API reference

## 🔄 **Maintenance**

- **Update Schedule**: Refresh when new RazorEnhanced versions are released
- **Validation**: Test API compatibility with each DexBot release
- **Documentation**: Keep human-readable docs in sync with API changes
- **Type Hints**: Validate type annotations against actual RazorEnhanced behavior
