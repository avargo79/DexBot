# DexBot Changelog

## Version 2.0.1 - 2025-06-28

### Major Changes: Integrated Auto Heal Controls ✅

#### 🎯 **User Experience Improvements**
- **Integrated Main GUMP**: Moved all Auto Heal controls into the main GUMP interface
- **Removed Separate Settings GUMP**: No longer using a dedicated settings window  
- **Streamlined Interface**: All healing toggles now accessible directly from main interface
- **Simplified Navigation**: No need to open separate windows for healing configuration

#### 🔧 **Technical Changes**
- Updated `create_auto_heal_status_section()` to include bandage and potion toggle buttons
- Removed `create_auto_heal_settings_gump()` method completely
- Cleaned up button handlers (removed button IDs 9, 10, 11 for settings navigation)
- Removed `GumpState.SETTINGS` state from state management
- Removed `GUMP_AUTO_HEAL_SETTINGS_ID` configuration constant
- Cleaned up config file to remove obsolete `settings_gump` section

#### 🎨 **Interface Improvements**
- **Two-line Auto Heal Section**: 
  - **Line 1**: Main status with resource counts and usage stats
  - **Line 2**: Individual toggle buttons for bandages and potions with status labels
- **Better UX**: All controls accessible without opening additional windows
- **Cleaner Layout**: More space efficient, integrated design
- **Consistent Styling**: Matches overall GUMP design language

#### 📚 **Documentation Updates**
- Updated README.md to reflect new integrated interface
- Updated PRD to document simplified GUMP system  
- Removed references to separate Settings GUMP throughout documentation
- Added comprehensive changelog documenting all changes

#### 🧪 **Testing & Quality Assurance**
- All existing tests continue to pass ✅
- Configuration system remains fully functional ✅
- No breaking changes to config file structure ✅
- Backward compatibility maintained ✅

#### 💾 **Config File Changes**
- Removed `settings_gump` section from `auto_heal_config.json`
- Updated default configuration template in code
- Existing config files automatically cleaned up on load

---

### Migration Notes
- **✅ No User Action Required**: Changes are backward compatible
- **✅ Existing Configs**: Automatically updated on next load  
- **✅ Interface**: All previous functionality maintained in streamlined design
- **✅ Performance**: Actually improved due to reduced complexity

### What Users Will See
- **Main GUMP** now includes bandage and potion toggle buttons directly in the Auto Heal section
- **No Settings Button**: The separate settings GUMP has been completely removed
- **Faster Access**: Toggle healing methods without opening separate windows
- **Same Functionality**: All previous features remain available and functional

### Developer Benefits  
- **Reduced Complexity**: Fewer GUMP states and handlers to maintain
- **Cleaner Code**: Eliminated duplicate button handling logic
- **Better Performance**: Single GUMP instead of multiple windows
- **Easier Maintenance**: Simpler state management and fewer edge cases

This change significantly improves the user experience by reducing interface complexity while maintaining all functionality in a more accessible and efficient design.
