#!/bin/bash

# DexBot Build Script - Shell
# Runs the complete build pipeline: clean, lint, test, and bundle

echo "🏗️  DexBot Build Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

check_prerequisites() {
    info "Checking prerequisites..."
    
    # Check Python
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version)
        success "Python found: $PYTHON_VERSION"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version)
        success "Python found: $PYTHON_VERSION"
    else
        error "Python is not installed or not in PATH"
        return 1
    fi
    
    # Check/Install invoke
    if $PYTHON_CMD -c "import invoke" >/dev/null 2>&1; then
        success "invoke is available"
    else
        info "Installing invoke..."
        if $PYTHON_CMD -m pip install invoke; then
            success "invoke installed successfully"
        else
            error "Failed to install invoke"
            return 1
        fi
    fi
    
    return 0
}

run_build() {
    info "Running full build pipeline..."
    echo ""
    
    if $PYTHON_CMD -m invoke build; then
        echo ""
        success "🎉 Build completed successfully!"
        success "📦 Bundled script available at: dist/DexBot.py"
        return 0
    else
        echo ""
        error "❌ Build failed"
        return 1
    fi
}

# Main execution
if check_prerequisites; then
    if run_build; then
        echo ""
        echo -e "${YELLOW}🚀 Next steps:${NC}"
        echo -e "${WHITE}  1. Copy dist/DexBot.py to your RazorEnhanced Scripts folder${NC}"
        echo -e "${WHITE}  2. Run the script in RazorEnhanced${NC}"
        echo ""
        echo -e "${CYAN}Optional:${NC}"
        echo -e "${WHITE}  - Update API docs: $PYTHON_CMD scripts/update_api_docs.py${NC}"
        exit 0
    else
        echo ""
        echo -e "${YELLOW}💡 Troubleshooting:${NC}"
        echo -e "${WHITE}  - Check the error messages above${NC}"
        echo -e "${WHITE}  - Ensure all Python dependencies are installed${NC}"
        echo -e "${WHITE}  - Run individual tasks: $PYTHON_CMD -m invoke lint, $PYTHON_CMD -m invoke test${NC}"
        exit 1
    fi
else
    echo ""
    echo -e "${YELLOW}💡 Please install the required prerequisites:${NC}"
    echo -e "${WHITE}  - Python 3.7+${NC}"
    echo -e "${WHITE}  - pip (Python package manager)${NC}"
    exit 1
fi
