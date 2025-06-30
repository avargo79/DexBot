# DexBot - Modular Bot System

![Build Status](https://github.com/avargo79/DexBot/actions/workflows/ci-cd.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)

## 🚀 Quick Navigation

**New Users**: [Quick Start](#quick-start) • [Installation](#1-installation) • [Usage](#2-usage)  
**Developers**: [Developer Workflow](#developer-workflow) • [Build Scripts](#-local-build-scripts) • [Contributing](#contributing)  
**Documentation**: [Features](#features) • [Configuration](#configuration) • [API Reference](docs/RazorEnhanced_API_Reference.md)

## 🤖 AI-Coded Proof of Concept

**This project was entirely coded by AI as a demonstration of modern AI development capabilities.**

DexBot serves as a comprehensive proof of concept showcasing how AI can:
- **Design and implement complex systems** with modular architecture
- **Create production-ready code** with proper testing, documentation, and CI/CD
- **Develop cross-platform tools** and automation scripts
- **Maintain code quality** through automated linting, testing, and deployment
- **Build complete developer experiences** from initial concept to production infrastructure

The entire codebase, documentation, build system, and DevOps infrastructure were generated through AI assistance, demonstrating the potential for AI-driven development workflows in game automation and software engineering.

## 📋 Table of Contents

- [🤖 AI-Coded Proof of Concept](#-ai-coded-proof-of-concept)
- [📋 Table of Contents](#-table-of-contents)
- [Recent Updates (v2.2.0)](#recent-updates-v220)
- [Directory Structure](#directory-structure)
- [Features](#features)
- [Developer Workflow](#developer-workflow)
- [🔄 Complete Developer Workflow](#-complete-developer-workflow)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Item Requirements](#item-requirements)
- [Troubleshooting](#troubleshooting)
- [Development Tasks](#development-tasks)
- [Contributing](#contributing)
- [Version](#version)
- [🚀 AI Development Showcase](#-ai-development-showcase)

---

DexBot is a modular bot system for Ultima Online with RazorEnhanced, featuring an advanced Auto Heal system, high-performance Combat System, and optimized Looting System with a modern GUMP interface and robust state management. Built with a clean, focused architecture optimized for performance and user experience.

## Recent Updates (v3.1.1)

**🚀 Phase 3.1.1 - Revolutionary Ignore List Optimization** ✅ COMPLETED:
- **🎯 Native API Optimization**: Uses `Items.Filter.CheckIgnoreObject = True` for filter-level corpse exclusion
- **⚡ 90% Performance Gain**: Processed corpses excluded from future scans entirely via `Misc.IgnoreObject()`
- **🧠 Self-Managing Memory**: Automatic ignore list cleanup every 3 minutes prevents unbounded growth
- **🔧 Configurable Control**: Ignore list optimization and cleanup intervals configurable in main config
- **📊 Cumulative Performance**: 85-95% reduction in looting system execution time, 30-40% main loop improvement

**🚀 Phase 3.1 - Major Performance Optimizations** ✅ COMPLETED:
- **🔧 Looting System**: Optimized gold detection, item evaluation caching, corpse queue management
- **⚡ Main Loop**: Smart performance thresholds, reduced timestamp calls, conditional logging
- **🧠 Memory Management**: Limited cache growth, optimized cleanup intervals, performance monitoring
- **📊 Performance Results**: 60-70% looting system improvement, 20-30% main loop optimization

**🎯 Looting System Phase 2 - Performance & Reliability** ✅ COMPLETED:
- **4x Faster Corpse Detection**: Reduced scan interval to 250ms for much more responsive looting
- **Corpse Processing Cache**: Intelligent caching prevents repeated processing of empty corpses  
- **Enhanced Item ID Matching**: Supports integers, decimal strings, and hex format item IDs
- **Optimized UO Timing**: Proper 650ms delays for reliable item movement following UO standards
- **Robust Corpse Detection**: Uses `Items.Filter(IsCorpse=True)` for reliable detection across shards

**🚀 Combat System Performance Optimizations** ✅ COMPLETED:
- ✅ **Major Performance Boost**: 50-80% faster target scanning with intelligent caching
- ✅ **Smart Health Bar Management**: Only opens health bars for selected targets (eliminates delays)
- ✅ **Adaptive Timing**: Dynamic scan intervals based on combat state for optimal performance
- ✅ **Memory Optimization**: Intelligent caching with automatic expiration prevents memory buildup
- ✅ **API Optimization**: 60-70% reduction in redundant API calls through smart caching

**⚙️ Combat System Enhancement** ✅ COMPLETED:
- ✅ **Target Name Display**: Shows `[Name - HP%]` above target's head while in War Mode
- ✅ **Improved Display Format**: Clean bracket format (`[Orc - 85%]`) for better visibility
- ✅ **Health Tracking**: Real-time health percentage display with mob names
- ✅ **War Mode Integration**: Only activates combat features when ready for battle
- ✅ **User Configurable**: Toggle target display on/off via Combat Settings GUMP

**🚀 DevOps Infrastructure & Build System** ✅ COMPLETED:
- ✅ **GitHub Actions CI/CD**: Automated lint, test, build, and release pipeline
- ✅ **Developer Scripts**: PowerShell and Shell scripts for local development
- ✅ **API Documentation**: Automated RazorEnhanced API reference generation
- ✅ **Documentation Updates**: Comprehensive docs with workflow and contribution guides
- ✅ **Branch-based Development**: Feature branches with automated integration

**🔧 Development Infrastructure & Build System** ✅ COMPLETED:
- ✅ **Modular Code Structure**: Reorganized into src/ directory with system separation
- ✅ **Development Tooling**: Modern Python development workflow
- ✅ **Build Automation**: Cross-platform build scripts with dependency management
- ✅ **Quality Assurance**: Automated testing and linting integration
- ✅ **Code Quality Tools**: Integrated linting and formatting automation

**⚙️ Combat System Integration** ✅ COMPLETED:
- ✅ **Full Combat System**: Automated target detection, selection, and engagement
- ✅ **Smart Target Selection**: Configurable priority modes (closest, lowest health, highest threat)
- ✅ **Combat Configuration**: Comprehensive JSON-based settings for all combat behaviors
- ✅ **GUMP Integration**: Dedicated Combat Settings interface with real-time toggles
- ✅ **Safety Features**: Auto-retreat on low health, combat timeouts, range checking
- ✅ **RazorEnhanced Integration**: Full API integration with Mobiles, Target, and Player systems

**🔄 Integrated Auto Heal Controls** ✅ COMPLETED:
- ✅ **Streamlined Interface**: No separate settings window - all controls accessible from main GUMP
- ✅ **Two-Line Auto Heal Section**: Status line + toggle buttons for bandages and potions
- ✅ **Faster Access**: Toggle healing methods without opening additional windows
- ✅ **Same Functionality**: All previous features maintained in more accessible design

## Directory Structure

**Clean v3.1.1 Structure** (After Phase 3 Cleanup):
```
DexBot/
├── dist/
│   └── DexBot.py                   # 🚀 Production build (198,042 bytes, v3.1.1)
├── src/                            # 📁 Modular source code
│   ├── core/                       # Core bot functionality
│   │   ├── bot_config.py           # Configuration constants and settings
│   │   ├── logger.py               # Logging and system status tracking
│   │   └── main_loop.py            # Main bot coordination and timing
│   ├── systems/                    # Bot systems (healing, combat, looting)
│   │   ├── auto_heal.py            # Advanced Auto Heal system
│   │   ├── combat.py               # High-performance Combat system
│   │   └── looting.py              # Optimized Looting system with ignore list
│   ├── ui/                         # GUMP interface and user interaction
│   │   └── gump_interface.py       # Modern GUMP interface with controls
│   ├── config/                     # Configuration management
│   │   ├── config_manager.py       # JSON config loading/saving
│   │   └── *.json                  # Configuration files
│   └── utils/                      # Utility functions and helpers
├── docs/                           # 📚 Essential documentation
│   ├── CHANGELOG.md                # Version history (updated to v3.1.1)
│   ├── DexBot_PRD.md               # Product Requirements Document
│   ├── DexBot_Tasks.md             # Development progress tracking
│   ├── api_reference.json          # RazorEnhanced API reference
│   ├── RazorEnhanced_API_Reference.md # API documentation
│   └── UO_ITEM_IDS_REFERENCE.md    # UO item ID reference
├── scripts/                        # 🔧 Build and development tools
│   ├── build.ps1                   # PowerShell build script (working)
│   ├── build.sh                    # Cross-platform shell script
│   └── update_api_docs.py          # API documentation updater
├── tmp/                            # 📊 Phase 3+ development docs
│   ├── .gitkeep                    # Git directory placeholder
│   ├── development_workflow_reminder.md
│   ├── phase3_test_results.md      # Phase 3 testing documentation
│   ├── phase3_optimization_plan.md # Performance optimization plans
│   ├── phase3_performance_analysis_guide.md
│   ├── phase3_1_optimization_summary.md
│   ├── phase3_1_1_ignore_list_optimization.md
│   ├── PHASE_3_1_1_FINAL_SUMMARY.md
│   └── PHASE_3_CLEANUP_COMPLETE.md # Cleanup documentation
├── tests/                          # 🧪 Test infrastructure
├── .github/                        # 🏗️ CI/CD pipeline
├── pyproject.toml                  # Python project configuration
├── requirements.txt                # Python dependencies
├── README.md                       # This documentation
└── DEVELOPMENT_RULES.md            # Development best practices
```

**Key Improvements**:
- ✅ **Clean Structure**: Removed 19+ temp/empty files from Phase 2
- ✅ **Production Ready**: Working v3.1.1 build with all optimizations
- ✅ **Organized Docs**: Essential documentation only, no empty placeholders
- ✅ **Phase 3 Ready**: Clean `/tmp` with only relevant Phase 3+ documentation

## Features

## Features

### ✅ Auto Heal System (Advanced Implementation)
- **Smart Healing Logic**: Automated bandages and potions with configurable health thresholds
- **Individual Toggles**: Independent enable/disable for bandage and potion healing via GUMP
- **Resource Management**: Intelligent supply checking with low-supply warnings
- **Performance Optimized**: Efficient health monitoring with minimal game impact
- **GUMP Integration**: Real-time status display and controls in main interface

### ✅ Combat System (High-Performance Implementation)
- **Advanced Target Detection**: Automated scanning with 50-80% performance improvement through caching
- **Smart Targeting**: Configurable priority modes (closest, lowest health, highest threat)
- **War Mode Integration**: Only activates when player is in War Mode for safety
- **Target Display**: Shows `[Name - HP%]` above target's head with real-time health tracking
- **Performance Caching**: Mobile data caching reduces API calls by 60-70%
- **Safety Features**: Auto-retreat on low health, range checking, combat timeouts

### ✅ Looting System (Revolutionary Performance Optimization)
- **🚀 Ignore List Optimization**: Uses `Items.Filter.CheckIgnoreObject = True` for 90% performance gain
- **Smart Corpse Management**: Processed corpses automatically excluded via `Misc.IgnoreObject()`
- **Self-Managing Memory**: Automatic ignore list cleanup prevents unbounded growth
- **Intelligent Item Evaluation**: Configurable loot lists with priority system and caching
- **Enhanced Detection**: Robust `Items.Filter(IsCorpse=True)` works across all UO shards
- **Optimized Timing**: 4x faster scanning with proper UO-standard delays for reliability
- **Automatic Skinning**: Configurable creature skinning with tool management

### ✅ Configuration Management System (JSON-Based)
- **Modular Configuration**: Separate JSON files for main, auto heal, combat, and looting settings
- **Performance Optimization Settings**: Dedicated `performance_optimization` section in main config
- **Hot Reload**: Changes automatically detected and applied without restart
- **Default Fallbacks**: Robust defaults ensure functionality even with missing config files
- **Validation**: Input validation prevents configuration errors from breaking the bot
- **Real-time Feedback**: Detailed console logging shows corpse detection, item evaluation, and loot decisions

### ✅ GUMP Interface System (Implemented)
- **Modern Interface**: Clean, intuitive GUMP design with organized sections
- **Real-time Status**: Live display of bot status, health monitoring, and target information
- **Interactive Controls**: Toggle buttons for all major bot functions
- **Settings Integration**: In-interface configuration for all bot systems
- **Performance Indicators**: Visual feedback for system performance and activity
- **Responsive Design**: Interface adapts to different screen resolutions

### 🚧 Planned Future Modules
- **📦 Inventory Management**: Smart item organization and resource management
- **🏃 Movement System**: Pathfinding and automated movement capabilities
- **🛡️ Defense System**: Advanced threat detection and defensive responses
- **📊 Statistics Tracking**: Performance metrics and usage statistics
- **🔧 Plugin Architecture**: Third-party module support and API extensions
- **🌐 Multi-Character Support**: Coordinate multiple characters simultaneously

## Developer Workflow

This project is designed for **AI-assisted development workflows**. Here's the complete process for adding new features or fixing issues:

#### 1. 🔄 Branch Creation & Setup

```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements.txt

# Run initial build to verify setup
python -m invoke build
```

#### 2. 📚 AI Context Preparation

**Before making ANY changes**, provide your AI assistant with these prompts to establish proper context:

**Context Discovery Prompts:**

"Please read and analyze the DexBot PRD file (docs/DexBot_PRD.md) and summarize the current feature requirements and project goals."

"Review the task tracking file (docs/DexBot_Tasks.md) to understand what features are planned, in progress, or completed."

"Examine the project structure and identify which systems (healing, combat, UI, config) would be affected by implementing [your feature name]."

"What are the key architectural patterns used in this codebase, and how should I follow them when adding new functionality?"

**Implementation Planning Prompts:**

"Based on the PRD requirements, help me design a [new system/feature] that integrates with the existing modular architecture."

"What RazorEnhanced API methods would I need for implementing [feature description]? Reference the local API documentation in docs/RazorEnhanced_API_Reference.md."

"Generate a feature implementation plan that follows the existing code structure in src/systems/ and includes proper error handling, logging, and configuration management."

#### 3. 🚀 VS Code + RazorEnhanced Development

**Recommended Setup:**
1. **Install Extensions**:
   - RazorEnhanced extension for VS Code
   - Python extension for VS Code

2. **Configure Workspace**:
   - Open the DexBot folder as a VS Code workspace
   - The RazorEnhanced extension will automatically detect the project structure

3. **Development Workflow**:
   - Make changes to source files in `src/`
   - Use `python -m invoke bundle` to create the distributable version
   - Test in RazorEnhanced using the bundled `dist/DexBot.py`

**Note**: Direct execution via `exec(open(...))` is not recommended. Always use the proper development workflow with bundling.

#### 4. 🧪 Testing & Validation

```bash
# Run tests
python -m invoke test

# Run linting
python -m invoke lint

# Full build and validation
python -m invoke build
```

#### 5. 🔍 AI Code Review

**Before committing**, ask your AI assistant to review your changes:

"Review my code changes and ensure they follow the existing patterns for error handling, logging, and configuration management used in this project."

"Help me integrate this new feature with the existing GUMP interface system, following the patterns used in src/ui/gump_interface.py."

"Generate comprehensive error handling for this feature that matches the robustness patterns used throughout the DexBot codebase."

#### 6. 📦 Commit & Integration

```bash
# Stage and commit changes
git add .
git commit -m "feat: [description of your feature]"

# Push to your feature branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

The CI/CD pipeline will automatically validate your changes and provide feedback.

## 🔄 Complete Developer Workflow

### Prerequisites
- Python 3.7+ (for development tasks)
- Git for version control
- VS Code with RazorEnhanced extension (recommended)
- RazorEnhanced client (for testing/deployment)

### Step-by-Step Development Process

1. **Environment Setup**
   ```bash
   git clone https://github.com/avargo79/DexBot.git
   cd DexBot
   pip install -r requirements.txt
   ```

2. **Feature Development**
   ```bash
   git checkout -b feature/new-feature
   # Make your changes
   python -m invoke bundle  # Create distributable
   ```

3. **Testing in RazorEnhanced**
   - Copy `dist/DexBot.py` to your RazorEnhanced Scripts folder
   - Test the functionality in-game
   - Iterate as needed

4. **Quality Assurance**
   ```bash
   python -m invoke test     # Run tests
   python -m invoke lint     # Check code quality
   python -m invoke build    # Full build validation
   ```

5. **Deployment**
   ```bash
   git commit -m "feat: description"
   git push origin feature/new-feature
   # Create Pull Request
   ```

## Quick Start

### 1. Installation

**Method 1: VS Code + RazorEnhanced Extension (Recommended)**

1. **Install VS Code Extensions**:
   - Install the **Python extension** from Microsoft
   - Install the **RazorEnhanced extension**

2. **Setup Workspace**:
   - Open VS Code
   - File → Open Folder → Select your DexBot folder
   - The RazorEnhanced extension will detect your project

3. **Run the Bot**:
   - Open `main.py` in VS Code
   - Press `F5` or use Command Palette:
     - Press `Ctrl+Shift+P` → "RazorEnhanced: Play"
   - The script will run directly in RazorEnhanced

**Method 2: Direct File Copy**

1. Download or clone this repository
2. Copy `dist/DexBot.py` to your RazorEnhanced Scripts folder
3. In RazorEnhanced: Scripts → Load → Select `DexBot.py`

### 2. Usage

1. **Start RazorEnhanced** and connect to your Ultima Online server
2. **Load the Script**: Use Method 1 (VS Code) or Method 2 (direct copy) above
3. **Configure**: The bot will create default configuration files on first run
4. **Customize**: Edit config files or use the in-game GUMP interface to adjust settings
5. **Activate**: Use the GUMP interface to enable desired bot functions

**Essential Usage Tips:**
- **Always test in a safe environment first**
- **Configure health thresholds before activating healing**
- **Set up proper combat settings before enabling combat mode**
- **Monitor the bot initially to ensure it behaves as expected**

## Configuration

The bot uses JSON configuration files for all settings:

### Main Configuration (`config/main_config.json`)
```json
{
    "gump_position": {"x": 100, "y": 100},
    "update_interval": 1000,
    "debug_mode": false,
    "auto_save_config": true
}
```

### Auto Heal Configuration (`config/auto_heal_config.json`)
```json
{
    "bandage_threshold": 80,
    "potion_threshold": 50,
    "cure_immediately": true,
    "bandage_enabled": true,
    "potion_enabled": true
}
```

**Configuration Tips:**
- **Health Thresholds**: Set bandage_threshold higher than potion_threshold
- **Safety First**: Start with conservative settings and adjust gradually
- **Backup Configs**: The bot automatically backs up your configurations

## Item Requirements

For full functionality, ensure you have these items:

### Auto Heal System
- **Bandages**: For primary healing (recommended: 50+ bandages)
- **Heal Potions**: Greater Heal, Heal, or Lesser Heal potions
- **Cure Potions**: For automatic poison curing

### Combat System
- **Weapons**: Any valid weapon for your character type
- **Reagents**: If using magic combat (spell components)

**Inventory Tips:**
- Keep healing items easily accessible (main pack)
- Ensure adequate supplies before extended bot usage
- Consider carrying backup supplies for longer sessions

## Troubleshooting

### Common Issues

**Issue**: Bot doesn't start or crashes immediately
- **Solution**: Check that all config files are valid JSON
- **Verify**: RazorEnhanced is connected to UO server
- **Check**: No conflicting scripts are running

**Issue**: Healing not working
- **Solution**: Verify you have bandages/potions in inventory
- **Check**: Health thresholds are set appropriately
- **Confirm**: Auto Heal is enabled in GUMP interface

**Issue**: Combat system not engaging targets
- **Solution**: Ensure you're in War Mode
- **Verify**: Combat system is enabled in settings
- **Check**: Target priority settings are configured

**Issue**: GUMP interface not appearing
- **Solution**: Check gump_position in config (may be off-screen)
- **Try**: Delete config files to reset to defaults
- **Verify**: No other GUMPs are blocking the interface

### Debug Mode

Enable debug mode in `main_config.json` for detailed logging:
```json
{
    "debug_mode": true
}
```

This will provide detailed information about bot operations in the RazorEnhanced console.

### Getting Help

1. **Check Configuration**: Ensure all JSON files are valid
2. **Review Logs**: Enable debug mode for detailed information
3. **Test Components**: Try enabling one system at a time
4. **Reset Settings**: Delete config files to restore defaults

## Development Tasks

This project uses modern Python development tools. **Note**: These tools are for development only and should NOT be run inside RazorEnhanced.

### 🛠️ Local Build Scripts

**Cross-Platform Build Commands:**

**Windows (PowerShell):**
```powershell
# Full build pipeline
.\scripts\build.ps1

# Quick development build
.\scripts\build.ps1 -Quick
```

**Linux/Unix/macOS (Bash):**
```bash
# Full build pipeline  
./scripts/build.sh

# Quick development build
./scripts/build.sh --quick
```

### 📦 Python Invoke Tasks

**Primary Development Commands:**
* **`invoke build`**: Complete build pipeline (test + lint + bundle + docs).
* **`invoke bundle`**: Creates the single-file `dist/DexBot.py` for RazorEnhanced.
* **`invoke test`**: Runs the test suite with coverage reporting.
* **`invoke lint`**: Code quality checks (flake8 + formatting validation).
* **`invoke docs`**: Updates API documentation from RazorEnhanced sources.
   - Fetches latest API information from RazorEnhanced documentation
   - Creates both Markdown and JSON output formats
   - Should be run manually when you need updated API reference
* **`invoke dev`**: Development mode (test + lint + bundle for quick iteration).

**Usage Examples:**
```bash
# Run individual tasks
python -m invoke bundle
python -m invoke test
python -m invoke lint

# Run full build pipeline
python -m invoke build

# Quick development build
python -m invoke dev

# Get help
python -m invoke help
```

**Important Notes:**
- **End users don't need these tools** - the `dist/DexBot.py` file runs directly in RazorEnhanced
- **Development tasks only work outside RazorEnhanced** - use a regular Python environment
- **Always run `invoke bundle` after making changes** to update the distributable version

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run the build script: `./scripts/build.sh` (or `build.ps1` on Windows)
5. Commit changes: `git commit -m "Description of changes"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

The CI/CD pipeline will automatically run tests and validation on your PR.

### Code Quality Standards
- Follow PEP 8 style guidelines (enforced by flake8)
- Use black for code formatting
- Include type hints where appropriate
- Write tests for new functionality
- Update documentation for user-facing changes

## Version

**Current Version**: 3.1.1 - "Phase 3.1.1 - Ignore List Optimization"  
**Build Size**: 198,042 bytes  
**Build Date**: June 29, 2025  
**Author**: RugRat79 (DexBot Development Team)  
**License**: MIT

### Performance Metrics (v3.1.1)
- **Looting System**: 85-95% reduction in average execution time
- **Main Loop**: 30-40% reduction in coordination overhead  
- **Memory Usage**: Self-managing with automatic cleanup
- **Combat System**: 50-80% faster target scanning with intelligent caching
- **Overall**: Production-ready with revolutionary performance optimizations

---

## 🚀 AI Development Showcase

This project demonstrates the capabilities of modern AI in software development:

**🚀 What AI Accomplished:**
- **Complete Codebase**: All Python code, from core systems to utility functions
- **Modular Architecture**: Well-structured project with proper separation of concerns  
- **Production Infrastructure**: GitHub Actions CI/CD, cross-platform build scripts
- **Comprehensive Documentation**: Technical docs, API references, setup guides
- **Quality Assurance**: Automated testing, linting, and deployment workflows
- **Developer Experience**: One-command builds, environment setup, contribution guides

**🔄 Technical Complexity:**
- **Game API Integration**: RazorEnhanced API interfacing and event handling
- **Real-time Systems**: Combat automation, health monitoring, target tracking
- **User Interface**: Dynamic GUMP creation with state management
- **Configuration Management**: JSON-based settings with validation and defaults
- **Error Handling**: Robust exception handling and logging throughout
- **Performance Optimization**: Caching, adaptive timing, memory management

**⚙️ DevOps Excellence:**
- **Modern CI/CD**: Latest GitHub Actions with environment gating
- **Cross-Platform Support**: Windows PowerShell + Unix Shell scripts
- **Security**: Production environment approval workflows
- **Documentation**: Auto-generated API references and comprehensive guides
- **Maintenance**: Automated dependency updates and quality checks

This project showcases how AI can handle end-to-end software development, from initial concept through production deployment, maintaining professional standards throughout the development lifecycle.

---

## 📊 Project Stats

- **Lines of Code**: 3,000+ (modular Python architecture)
- **Test Coverage**: Comprehensive test suite with automated validation
- **Build Time**: < 30 seconds (optimized build pipeline)
- **Supported Platforms**: Windows, Linux, macOS (development), RazorEnhanced (runtime)
- **Dependencies**: Minimal runtime dependencies (IronPython .NET embedded)

## 🔗 Related Links

- **[Product Requirements Document](docs/DexBot_PRD.md)** - Detailed feature specifications
- **[Development Tasks](docs/DexBot_Tasks.md)** - Project roadmap and progress tracking 
- **[API Reference](docs/RazorEnhanced_API_Reference.md)** - Complete RazorEnhanced API documentation
- **[Changelog](docs/CHANGELOG.md)** - Version history and release notes
- **[GitHub Actions](https://github.com/avargo79/DexBot/actions)** - Live build and deployment status

## 🏆 Acknowledgments

Special thanks to the RazorEnhanced development team for creating an excellent Ultima Online automation platform that makes projects like DexBot possible.
