#!/bin/bash
# DexBot Feature Preparation Script Launcher
# This bash script simplifies running the feature preparation script

# Default values
FEATURE_NAME=""
NON_INTERACTIVE=false
SKIP_GIT=false
SKIP_CLEANUP=false
SKIP_VALIDATION=false
SHOW_HELP=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --non-interactive)
            NON_INTERACTIVE=true
            shift
            ;;
        --skip-git)
            SKIP_GIT=true
            shift
            ;;
        --skip-cleanup)
            SKIP_CLEANUP=true
            shift
            ;;
        --skip-validation)
            SKIP_VALIDATION=true
            shift
            ;;
        --help|-h)
            SHOW_HELP=true
            shift
            ;;
        *)
            # First non-option argument is feature name
            if [[ -z "$FEATURE_NAME" ]]; then
                FEATURE_NAME="$1"
            fi
            shift
            ;;
    esac
done

# Show help and exit
if [ "$SHOW_HELP" = true ]; then
    echo -e "\e[32mDexBot Feature Preparation Tool - Help\e[0m"
    echo -e "\e[32m=======================================\e[0m"
    echo ""
    echo -e "\e[36mUsage:\e[0m"
    echo -e "  ./prepare_feature.sh [feature-name] [options]"
    echo ""
    echo -e "\e[36mArguments:\e[0m"
    echo -e "  feature-name        Name of the feature to create (will create feature/[feature-name] branch)"
    echo ""
    echo -e "\e[36mOptions:\e[0m"
    echo -e "  --non-interactive   Run without any prompts or user interaction"
    echo -e "  --skip-git          Skip updating Git repository and branch management"
    echo -e "  --skip-cleanup      Skip cleaning temporary files and build artifacts"
    echo -e "  --skip-validation   Skip running validation and tests"
    echo -e "  --help, -h          Display this help information"
    echo ""
    echo -e "\e[36mExamples:\e[0m"
    echo -e "  ./prepare_feature.sh buff-management-system"
    echo -e "  ./prepare_feature.sh buff-management-system --non-interactive"
    echo -e "  ./prepare_feature.sh --skip-validation --skip-cleanup"
    exit 0
fi

# Display header
echo -e "\e[32mDexBot Feature Preparation Tool\e[0m"
echo -e "\e[32m==============================\e[0m"

# Build Python command with arguments based on bash parameters
PYTHON_ARGS=()

if [ -n "$FEATURE_NAME" ]; then
    PYTHON_ARGS+=("$FEATURE_NAME")
fi

if [ "$NON_INTERACTIVE" = true ]; then
    PYTHON_ARGS+=("--non-interactive")
fi

if [ "$SKIP_GIT" = true ]; then
    PYTHON_ARGS+=("--skip-git")
fi

if [ "$SKIP_CLEANUP" = true ]; then
    PYTHON_ARGS+=("--skip-cleanup")
fi

if [ "$SKIP_VALIDATION" = true ]; then
    PYTHON_ARGS+=("--skip-validation")
fi

# Execute Python script with arguments
PYTHON_COMMAND="python tools/prepare_feature.py ${PYTHON_ARGS[*]}"
echo -e "\e[33mExecuting: $PYTHON_COMMAND\e[0m"

python tools/prepare_feature.py "${PYTHON_ARGS[@]}"
RESULT=$?

if [ $RESULT -ne 0 ]; then
    echo -e "\e[31mError running prepare_feature.py (exit code: $RESULT)\e[0m"
    echo -e "\e[33mMake sure Python is installed and in your PATH.\e[0m"
    exit $RESULT
fi

# Only show pause prompt if not in non-interactive mode
if [ "$NON_INTERACTIVE" != true ]; then
    echo -e "\e[36mPress Enter to continue...\e[0m"
    read
fi
