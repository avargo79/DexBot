# PRD: UO Item Database System (Consolidated)

**FR-127/128: Complete UO Item Database Optimization & Integration**

**Priority**: High  
**Estimated Effort**: 6-10 hours total  
**Target Version**: v3.2.0  
**Date**: June 30, 2025  
**Status**: Consolidated PRD - Single Source of Truth

> **Note**: This consolidated PRD replaces the individual FR-127 and FR-128 documents, 
> providing a comprehensive view of both database optimization and system integration 
> in a single, coordinated implementation plan.

## 1. Feature Overview

### 1.1 Feature Name
**UO Item Database System** - Complete optimization and integration of UO item reference system

### 1.2 Description
A comprehensive overhaul of DexBot's UO item handling system that consolidates dual reference systems into a single optimized JSON database and fully integrates it into all bot systems. This feature combines database optimization (FR-127) with system integration (FR-128) for a complete end-to-end solution.

### 1.3 User Story
*"As a DexBot user, I want a single, comprehensive item database that powers smart looting decisions, supports flexible configuration options, and provides better item identification across all bot systems."*

### 1.4 Business Value
- **Simplified Maintenance**: Single source of truth eliminates dual-system complexity
- **Enhanced User Experience**: Smart item identification and category-based configuration
- **Improved Performance**: Optimized lookup structures and caching
- **Better Decision Making**: Value-tier based looting and intelligent defaults
- **Developer Efficiency**: Unified API with comprehensive test coverage

## 2. Combined Requirements

### 2.1 Database Optimization (FR-127 Components)

#### 2.1.1 Data Consolidation
- **Requirement**: Migrate all item data from markdown to JSON format
- **Current State**: Dual system with 200+ items in markdown, 41 items in JSON
- **Target**: Single JSON database with 200+ items across 12+ categories
- **Success Criteria**: All markdown items present in JSON with enhanced metadata

#### 2.1.2 Performance Optimization
- **Requirement**: Implement efficient lookup structures for fast queries
- **Technical Details**: Enhanced quick_lookup indices, category groupings, value tier indexing
- **Success Criteria**: Support for lookup by ID, name, alias, category, and value tier

#### 2.1.3 Backward Compatibility
- **Requirement**: Ensure existing scripts continue to work without changes
- **Technical Details**: Maintain current JSON schema while adding enhancements
- **Success Criteria**: All existing utility functions work unchanged

### 2.2 System Integration (FR-128 Components)

#### 2.2.1 Looting System Integration
- **Priority**: High
- **Requirement**: Replace hardcoded item handling with database lookups
- **Current Issues**: 
  - Hardcoded hex IDs (`0x06F4`, `0x06F5` for gold)
  - String matching without database validation
  - No item categorization or value tier support
- **Target**: Full database integration with smart item evaluation

#### 2.2.2 Configuration Enhancement
- **Priority**: High
- **Requirement**: Support both string names and IDs in loot configuration
- **Features**:
  - Configuration validation against database
  - Category-based loot rules (e.g., "all gems")
  - Value tier-based rules (e.g., "high value items")
  - Smart default configurations

#### 2.2.3 Enhanced Item Identification
- **Priority**: Medium
- **Requirement**: Improve item identification and logging across all systems
- **Features**:
  - Database-powered item name resolution
  - Item categorization in loot decisions
  - Enhanced logging with item context
  - Item metadata in evaluation cache

## 3. Implementation Plan

### Phase 1: Database Optimization (2-3 hours)
**Base**: FR-127 Implementation

#### Task 1.1: Analysis & Preparation
- [ ] Compare existing markdown and JSON files
- [ ] Identify data gaps and inconsistencies  
- [ ] Create backup of current JSON database
- [ ] Analyze current `src/utils/uo_items.py` integration points

#### Task 1.2: Database Enhancement
- [ ] Merge all markdown data into JSON structure
- [ ] Implement comprehensive quick_lookup indices
- [ ] Add enhanced metadata (categories, value tiers, aliases)
- [ ] Optimize database structure for performance

#### Task 1.3: Validation & Testing
- [ ] Validate new database structure
- [ ] Test all existing utility functions
- [ ] Run comprehensive test suite
- [ ] Performance benchmark comparison

### Phase 2: Core System Integration (2-3 hours)  
**Base**: FR-128 Phase 1

#### Task 2.1: Looting System Integration
```python
# Add to src/systems/looting.py
from ..utils.uo_items import get_item_database, get_item_id

class LootingSystem:
    def __init__(self):
        # ...existing code...
        self.item_db = get_item_database()
```

#### Task 2.2: Replace Hardcoded Item Handling
```python
# Replace hardcoded gold detection:
def _is_currency(self, item_id: int) -> bool:
    """Check if item is currency using database."""
    return self.item_db.is_currency(item_id)

# Replace generic item evaluation:
def _identify_item(self, item) -> Dict[str, Any]:
    """Identify item using database lookup."""
    item_id = getattr(item, 'ItemID', 0)
    db_item = self.item_db.get_item_by_id(item_id)
    return {
        'id': item_id,
        'name': db_item['name'] if db_item else 'Unknown',
        'category': db_item.get('category', 'unknown') if db_item else 'unknown',
        'value_tier': db_item.get('value_tier', 'unknown') if db_item else 'unknown'
    }
```

#### Task 2.3: Enhanced Loot Evaluation
```python
def _evaluate_item_value(self, item_info: Dict[str, Any]) -> LootDecision:
    """Evaluate item using database information."""
    # Use value_tier and category for smart decisions
    category = item_info.get('category', 'unknown')
    value_tier = item_info.get('value_tier', 'unknown')
    
    # Category-based rules
    if category in self.config.get('always_take_categories', []):
        return LootDecision.TAKE
        
    # Value tier-based rules  
    if value_tier in ['very_high', 'high'] and self.config.get('take_high_value', True):
        return LootDecision.TAKE
        
    # Existing logic as fallback
    return self._legacy_evaluate_item(item_info)
```

### Phase 3: Configuration Enhancement (2-3 hours)
**Base**: FR-128 Phase 2

#### Task 3.1: Enhanced Configuration Loading
```python
def _load_enhanced_config(self) -> None:
    """Load configuration with database enhancement."""
    raw_config = self._load_raw_config()
    
    # Convert string names to IDs
    self.config = self._convert_config_strings(raw_config)
    
    # Validate against database
    self._validate_config_items()
    
    # Add smart defaults
    self._apply_smart_defaults()
```

#### Task 3.2: Category & Value Tier Support
```python
# Support in config:
{
    "always_take": [
        "gems:*",           # All gems category
        "tier:very_high",   # All very high value items  
        "currency:*",       # All currency
        3821               # Specific ID
    ],
    "value_tier_rules": {
        "very_high": "always",
        "high": "if_space",
        "medium": "never"
    }
}
```

### Phase 4: Advanced Features & Polish (1-2 hours)
**Base**: FR-128 Phase 3

#### Task 4.1: Preset Configurations
```python
def generate_preset_config(preset_name: str) -> Dict:
    """Generate preset configurations using database."""
    presets = {
        "conservative": ["currency:*", "tier:very_high"],
        "aggressive": ["currency:*", "tier:high", "tier:medium"],
        "gems_only": ["gems:*"],
        "treasure_hunter": ["gems:*", "jewelry:*", "tier:high"]
    }
    return self._build_config_from_rules(presets[preset_name])
```

#### Task 4.2: Enhanced Logging
```python
Logger.info(f"Looting '{item_info['name']}' ({item_info['category']}) - {item_info['value_tier']} value")
Logger.debug(f"Item evaluation: {item_id} -> {decision} (category: {category}, tier: {value_tier})")
```

### Phase 5: Cleanup & Documentation (1 hour)

#### Task 5.1: Legacy File Cleanup  
- [ ] Remove deprecated `ref/UO_ITEM_IDS_REFERENCE.md`
- [ ] Archive backup files to secure location
- [ ] Clean up temporary development files

#### Task 5.2: Documentation Updates
- [ ] Update all references to point to unified system
- [ ] Update developer documentation
- [ ] Update user configuration guides
- [ ] Update changelog and version notes

## 4. Success Criteria

### Database Optimization Success Criteria
- [ ] JSON database contains 200+ items (vs current ~41)
- [ ] Support for 12+ categories (vs current 8)  
- [ ] Quick_lookup supports 150+ searchable names/aliases
- [ ] All existing utility functions work unchanged
- [ ] Performance improved or maintained
- [ ] Single file to maintain instead of two

### System Integration Success Criteria
- [ ] Looting system uses database for all item identification
- [ ] Hardcoded item IDs eliminated
- [ ] Configuration supports string names, categories, and value tiers
- [ ] Enhanced logging provides item context
- [ ] Preset configurations available
- [ ] All 66+ existing tests still pass
- [ ] Performance impact < 5%

### Overall Success Criteria
- [ ] Single comprehensive item database system
- [ ] All DexBot systems use database for item handling
- [ ] User experience significantly improved
- [ ] Developer experience enhanced
- [ ] Maintainability improved
- [ ] Performance maintained or improved

## 5. Risk Assessment & Mitigation

### Low Risks
- **Breaking existing functionality**: Comprehensive test suite ensures compatibility
- **Performance impact**: Singleton pattern and caching minimize overhead
- **Data migration**: Well-defined process with backups

### Medium Risks  
- **Complex configuration logic**: Phased approach allows incremental testing
- **Database unavailability**: Graceful fallback mechanisms implemented

### Mitigation Strategies
1. **Comprehensive Testing**: Unit, integration, and live testing at each phase
2. **Phased Implementation**: Can rollback individual phases if needed
3. **Backup Strategy**: Full backups before any data migration
4. **Fallback Mechanisms**: System works without database if needed
5. **Performance Monitoring**: Track impact during implementation

## 6. Dependencies & Prerequisites

### Completed Dependencies
- ✅ Current `src/utils/uo_items.py` utility class
- ✅ Existing test framework and test suite
- ✅ Configuration management system
- ✅ Logging infrastructure

### Ready for Integration  
- 🔄 `src/systems/looting.py` - Ready for database integration
- 🔄 Configuration system - Ready for enhancement
- 🔄 Documentation system - Ready for updates

## 7. Effort & Timeline

### Total Estimated Effort: 8-12 hours
- **Phase 1** (Database): 2-3 hours
- **Phase 2** (Core Integration): 2-3 hours  
- **Phase 3** (Configuration): 2-3 hours
- **Phase 4** (Advanced Features): 1-2 hours
- **Phase 5** (Cleanup): 1 hour
- **Testing** (All Phases): 1-2 hours per phase

### Implementation Timeline
- **Week 1**: Phase 1 (Database Optimization)
- **Week 1**: Phase 2 (Core Integration) 
- **Week 2**: Phase 3 (Configuration Enhancement)
- **Week 2**: Phase 4-5 (Features & Cleanup)

## 8. Acceptance Criteria Summary

### Technical Acceptance
1. **Single Database**: One JSON file replaces dual markdown/JSON system
2. **Full Integration**: All systems use database for item handling  
3. **Enhanced Configuration**: Support for categories, value tiers, and smart defaults
4. **Performance**: No significant performance degradation
5. **Compatibility**: All existing functionality preserved
6. **Test Coverage**: Comprehensive test suite passes

### User Experience Acceptance
1. **Easier Configuration**: String names and categories supported
2. **Better Decisions**: Smart looting based on item value and category
3. **Improved Logging**: Detailed item context in all log messages
4. **Preset Options**: Ready-to-use configuration templates
5. **Error Messages**: Clear feedback for configuration issues

---

**Created**: June 30, 2025  
**Status**: Ready for Implementation  
**Combines**: FR-127 (Database Optimization) + FR-128 (System Integration)  
**Assigned**: Development Team  
**Branch**: `feature/uo-item-database-system`

## Implementation Notes

### Quick Start Order:
1. **Database Migration** (Phase 1) 
2. **Looting Integration** (Phase 2, Tasks 2.1-2.3)
3. **Configuration Enhancement** (Phase 3, Tasks 3.1-3.2)
4. **Advanced Features** (Phase 4)
5. **Cleanup & Documentation** (Phase 5)

### Key Files to Modify:
- `ref/uo_item_database.json` - Primary database file
- `src/systems/looting.py` - Main integration point
- `src/utils/uo_items.py` - Database utilities (if needed)  
- `config/looting_config.json` - Enhanced configuration examples
- Documentation files - Updated references

### Testing Strategy:
- Run test suite after each task completion
- Live testing with sample configurations  
- Performance benchmarking at key milestones
- User acceptance testing with preset configurations

This combined PRD provides a complete roadmap for implementing the full UO Item Database System.
