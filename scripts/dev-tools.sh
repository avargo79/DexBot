#!/bin/bash

# DexBot Developer Tools - Shell Script
# Provides automated commands for linting, testing, building, and bundling DexBot

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python environment
check_python() {
    print_status "Checking Python environment..."
    
    if ! command_exists python3 && ! command_exists python; then
        print_error "Python is not installed or not in PATH"
        exit 1
    fi
    
    # Use python3 if available, otherwise python
    PYTHON_CMD="python3"
    if ! command_exists python3; then
        PYTHON_CMD="python"
    fi
    
    print_success "Python found: $($PYTHON_CMD --version)"
}

# Function to check and install invoke if needed
check_invoke() {
    print_status "Checking invoke (pyinvoke)..."
    
    if ! $PYTHON_CMD -c "import invoke" 2>/dev/null; then
        print_warning "invoke not found. Installing..."
        $PYTHON_CMD -m pip install invoke
    fi
    
    print_success "invoke is available"
}

# Function to run linting
run_lint() {
    print_status "Running code linting..."
    
    # Check if we have a tasks.py file
    if [ -f "tasks.py" ]; then
        $PYTHON_CMD -m invoke lint
    else
        # Fallback to direct flake8/black if available
        if command_exists flake8; then
            print_status "Running flake8..."
            flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503
        fi
        
        if command_exists black; then
            print_status "Running black (check mode)..."
            black --check --diff src/ tests/
        fi
        
        if ! command_exists flake8 && ! command_exists black; then
            print_warning "No linting tools found. Please install flake8 and black"
        fi
    fi
    
    print_success "Linting completed"
}

# Function to run tests
run_test() {
    print_status "Running tests..."
    
    if [ -f "tasks.py" ]; then
        $PYTHON_CMD -m invoke test
    else
        # Fallback to direct pytest
        if command_exists pytest; then
            pytest tests/ -v
        elif [ -f "test_dexbot.py" ]; then
            $PYTHON_CMD test_dexbot.py
        else
            print_warning "No test runner found"
        fi
    fi
    
    print_success "Tests completed"
}

# Function to build/validate the project
run_build() {
    print_status "Building/validating project..."
    
    if [ -f "tasks.py" ]; then
        $PYTHON_CMD -m invoke build
    else
        # Fallback validation
        print_status "Validating Python syntax..."
        find src/ -name "*.py" -exec $PYTHON_CMD -m py_compile {} \;
        
        if [ -f "pyproject.toml" ]; then
            print_status "Validating pyproject.toml..."
            $PYTHON_CMD -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))" 2>/dev/null || \
            $PYTHON_CMD -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"
        fi
    fi
    
    print_success "Build completed"
}

# Function to create bundle
run_bundle() {
    print_status "Creating deployment bundle..."
    
    if [ -f "tasks.py" ]; then
        $PYTHON_CMD -m invoke bundle
    else
        # Fallback bundling
        print_status "Creating bundle directory..."
        rm -rf dist/
        mkdir -p dist/dexbot/
        
        # Copy source files
        cp -r src/* dist/dexbot/
        cp main.py dist/dexbot/
        cp DexBot_Modular.py dist/dexbot/
        
        # Copy config files
        if [ -d "config/" ]; then
            cp -r config/ dist/dexbot/
        fi
        
        # Create archive
        cd dist/
        if command_exists zip; then
            zip -r dexbot-bundle.zip dexbot/
            print_success "Bundle created: dist/dexbot-bundle.zip"
        elif command_exists tar; then
            tar -czf dexbot-bundle.tar.gz dexbot/
            print_success "Bundle created: dist/dexbot-bundle.tar.gz"
        else
            print_warning "No archiving tool found. Bundle directory created: dist/dexbot/"
        fi
        cd ..
    fi
    
    print_success "Bundle creation completed"
}

# Function to show help
show_help() {
    echo "DexBot Developer Tools - Shell Version"
    echo "Usage: $0 <command>"
    echo ""
    echo "Available commands:"
    echo "  lint    - Run code linting (flake8, black)"
    echo "  test    - Run test suite"
    echo "  build   - Build/validate the project"
    echo "  bundle  - Create deployment bundle"
    echo "  all     - Run all commands in sequence"
    echo "  help    - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 lint"
    echo "  $0 test"
    echo "  $0 all"
}

# Main script logic
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi
    
    case "$1" in
        "lint")
            check_python
            check_invoke
            run_lint
            ;;
        "test")
            check_python
            check_invoke
            run_test
            ;;
        "build")
            check_python
            check_invoke
            run_build
            ;;
        "bundle")
            check_python
            check_invoke
            run_bundle
            ;;
        "all")
            check_python
            check_invoke
            print_status "Running complete development workflow..."
            run_lint
            run_test
            run_build
            run_bundle
            print_success "All tasks completed successfully!"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Make script executable and run main function
main "$@"
