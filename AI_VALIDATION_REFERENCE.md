# 🤖 AI ASSISTANT QUICK REFERENCE

**CRITICAL**: This project has active AI validation enforcement (FR-129)

## Mandatory Commands for AI Assistants

### Git Operations
```bash
# ❌ NEVER use direct git commands
git push origin main

# ✅ ALWAYS use validated commands  
python -m invoke ai-check-command "git push origin main"
```

### Workflow Validation
```bash
# Check current workflow compliance
python -m invoke ai-validate

# Validate any command before execution
python -m invoke ai-check-command "any command here"
```

## System Overview

**Location**: `src/utils/ai_validation.py`
**Configuration**: `config/ai_validation_config.json`
**Tests**: `tests/test_ai_validation.py`

**Key Features**:
- Real-time command validation
- Workflow compliance enforcement
- Adaptive learning from patterns
- Automatic error correction suggestions

## Required Usage Pattern

1. **Always validate git commands**: Use `ai-check-command` wrapper
2. **Check workflow state**: Use `ai-validate` before major operations
3. **Follow suggestions**: System provides corrections for violations

## Integration Points

- Integrated into `tasks.py` invoke system
- Available through `ValidationIntegration` wrapper
- Decorator support for function-level validation

**See**: `.copilot/` directory for comprehensive AI configuration files.
