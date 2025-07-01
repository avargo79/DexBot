# AI-Assisted Development Setup

DexBot is configured for optimal AI-assisted development with GitHub Copilot and other AI tools.

## Quick Start

### GitHub Copilot (Recommended)

1. **Install GitHub Copilot extension** in VS Code
2. **Open the DexBot project** - Copilot will automatically load project-specific instructions
3. **Start coding** - Copilot now understands DexBot's architecture, RazorEnhanced constraints, and coding patterns

**That's it!** No additional configuration needed.

### Optional VS Code Setup

For additional development tools, see [`.vscode/README.md`](.vscode/README.md) for optional VS Code configuration.

## What's Included

### AI Instructions & Context
- **`.github/copilot-instructions.md`** - Comprehensive project guide for AI tools
- **`.vscode/copilot/instructions.md`** - Copilot-specific instructions (auto-loaded)
- **`.github/instructions/`** - Specialized patterns for systems and testing

### Key AI Features
- **RazorEnhanced API knowledge** - AI understands UO scripting constraints
- **Architecture patterns** - Consistent system design across the project
- **Testing requirements** - 3-case pattern with RazorEnhanced API mocking
- **Performance guidelines** - Long-running session optimization
- **Error handling** - Specific exception patterns for bot reliability

## AI Prompt Examples

### Creating a New System
```
Create a new monster_ai_system for DexBot that:
- Follows the existing architecture pattern
- Uses ConfigManager for configuration
- Includes comprehensive error handling
- Has 3-case testing pattern
- Optimizes for 12+ hour runtime sessions
- Uses RazorEnhanced Mobiles and Player APIs
```

### Bug Fixes
```
Fix this issue in DexBot looting system:
- Current behavior: Bot tries to loot empty corpses repeatedly
- Expected behavior: Skip empty corpses after first check
- System affected: looting
- Performance impact: Unnecessary API calls in tight loop
```

### Performance Optimization
```
Optimize this DexBot combat code for:
- Target: Reduce RazorEnhanced API calls by 50%
- Current issue: Calling Mobiles.Filter every 100ms
- Constraints: Single-threaded, memory limited
- Expected improvement: Cache results for 500ms
```

## Compatibility

### Supported AI Tools
- **GitHub Copilot** (Primary) - Full integration with custom instructions
- **Cursor AI** - Compatible via `.cursorrules` file
- **Other AI tools** - Can use `.github/copilot-instructions.md` as context

### Development Environments
- **VS Code** (Recommended) - Full AI integration
- **Other IDEs** - AI instructions available but may need manual setup

## Troubleshooting

### Copilot Not Understanding DexBot Context
1. Verify GitHub Copilot extension is installed and activated
2. Check that `.vscode/copilot/instructions.md` exists
3. Restart VS Code if needed
4. Try a specific DexBot prompt to test AI understanding

### VS Code Settings Conflicts
- VS Code settings are optional - only use if desired
- Copilot instructions work independently of VS Code settings
- See `.vscode/README.md` for optional configuration

### Need Help?
- Check `.github/copilot-instructions.md` for comprehensive AI guidelines
- Review existing systems in `src/systems/` for patterns
- Use AI prompts from the examples above
