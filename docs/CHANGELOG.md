# DexBot Changelog

## Version 2.1.1 - Combat System v1.2.1 - 2025-06-29

### Combat System: Updated Target Display Format ✅

#### 🎨 **Display Format Enhancement**
- **Updated Display Format**: Changed from `TARGET: Name - HP%` to clean `[Name - HP%]` format
- **Examples**: 
  - With health data: `[Orc - 85%]`, `[Dragon - 42%]`
  - Without health data: `[Orc]`, `[Skeleton]`
- **Consistent Formatting**: Maintains health percentage when available, shows just name when unavailable
- **Both Message Types**: Updated both overhead messages and fallback console messages

#### 🔧 **Technical Updates**
- Modified `_display_target_name_overhead()` method for cleaner format
- Updated fallback message handling for consistency
- Maintained all existing functionality with improved visual presentation

---

## Version 2.1.0 - Combat System v1.2 - 2025-06-29

### Combat System: Target Name Display Feature ✅

#### 🎯 **New Features**
- **Target Name Display**: Shows target name above mob's head every 3 seconds while in War Mode
- **Health Information**: Displays current HP, max HP, and health percentage in overhead text
- **War Mode Safety**: Only displays when player is actively in War Mode
- **User Toggle**: Can be enabled/disabled via Combat Settings GUMP

#### 🔧 **Technical Enhancements**
- Added `_display_target_name_overhead()` method to CombatSystem class
- Enhanced `monitor_combat()` to update target health info in real-time
- Added display_settings section to combat configuration (version 1.2)
- Integrated with RazorEnhanced `Misc.SendMessage` API for overhead messages
- Added UI toggle button (ID 43) for target name display control

#### ⚙️ **Configuration Updates**
- **Combat Config v1.2**: Added display_settings with 3 new options
  - `show_target_name_overhead`: Enable/disable target name display
  - `target_name_display_interval_ms`: Display frequency (default: 3000ms)
  - `target_name_display_color`: UO color code for text (default: 53)
- Updated ConfigManager with enhanced default combat configuration

#### 🎨 **Interface Improvements**
- Added Target Name Display toggle to Combat Settings GUMP
- Enhanced visual feedback with status indication and tooltip
- Consistent UI styling with existing combat toggles

#### 📚 **Documentation Updates**
- Updated Combat System Integration documentation to version 1.2
- Added comprehensive feature descriptions and configuration guide
- Included usage instructions and testing scenarios

#### 🚀 **Technical Details**
- Bundle size: 115KB with new features
- Enhanced combat monitoring with real-time health tracking
- War Mode integration for safety and user control
- Configurable timing to prevent message spam

---

## Version 2.0.2 - 2025-06-28

### Codebase Cleanup: Removed Unused Systems ✅

#### 🧹 **Code Simplification**
- **Removed Combat System References**: Eliminated all placeholder code and UI for Combat system
- **Removed Looting System References**: Eliminated all placeholder code and UI for Looting system
- **Cleaner Codebase**: Focused on active Auto Heal system only
- **Simplified Configuration**: Removed unused system toggles from config files

#### 🔧 **Technical Changes**
- Removed `COMBAT_ENABLED` and `LOOTING_ENABLED` from BotConfig class
- Removed `COMBAT_SETTINGS` and `LOOTING_SETTINGS` from GumpState enum
- Eliminated Combat/Looting system summary lines from main GUMP
- Removed button handlers for Combat/Looting toggles (buttons 11, 12, 13, 14)
- Cleaned up config files to remove unused system_toggles entries
- Removed commented placeholder code for future systems

#### 🎨 **Interface Improvements**
- **Cleaner Main GUMP**: Only shows active Auto Heal system
- **Focused UI**: No confusing "Not Implemented" placeholders
- **Better User Experience**: Interface only shows working features

#### 📚 **Documentation Updates**
- Updated README.md to remove references to Combat and Looting systems
- Cleaned up feature descriptions to focus on current capabilities

---

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
