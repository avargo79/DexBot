# Feature Request: UO Item Database Integration

**FR-128: Integrate UO Item Database into DexBot Systems**

## Overview
Integrate the optimized UO Item Database system (FR-127) into the main DexBot systems, specifically the looting system, to replace hardcoded item IDs and improve configuration flexibility.

## Background
Following the completion of FR-127 (UO Item Database Optimization), we now have a comprehensive, well-tested item database system. However, the main DexBot systems (particularly the looting system) still use:
- Hardcoded hex IDs (`0x06F4`, `0x06F5` for gold)
- String-based item matching without database lookups
- Manual configuration requiring knowledge of item IDs

The database system is ready for integration but not yet connected to the live bot systems.

## Current State Analysis

### ✅ What We Have (Complete):
- Comprehensive UO Item Database (`src/utils/uo_items.py`)
- 66 passing unit tests with 100% coverage
- Well-documented API with convenience functions
- Example integration code
- Singleton pattern for performance

### 🚧 Integration Gaps Identified:
1. **Looting System** (`src/systems/looting.py`):
   - No import of UO item database
   - Uses hardcoded hex IDs for gold detection
   - String matching without database validation
   - No item categorization or value tier support

2. **Configuration System**:
   - String-based loot lists not converted to IDs
   - No validation against database
   - Missing smart defaults from database categories

3. **UI/Reporting**:
   - No item name resolution for better user experience
   - Missing item categorization in logs

## Requirements

### Functional Requirements

#### FR-128.1: Looting System Integration
- **Priority**: High
- **Description**: Replace hardcoded item handling with database lookups
- **Tasks**:
  1. Import UO item database in looting system
  2. Replace hardcoded gold IDs with database lookup
  3. Add item identification and categorization
  4. Implement smart item evaluation using value tiers

#### FR-128.2: Configuration Enhancement
- **Priority**: High  
- **Description**: Support both string names and IDs in loot configuration
- **Tasks**:
  1. Add configuration validation against database
  2. Convert string-based config to IDs internally
  3. Support category-based loot rules (e.g., "all gems")
  4. Add value tier-based rules (e.g., "high value items")

#### FR-128.3: Enhanced Item Identification
- **Priority**: Medium
- **Description**: Improve item identification and logging
- **Tasks**:
  1. Replace generic item names with database names
  2. Add item categorization to loot decisions
  3. Enhanced logging with item context
  4. Item metadata in evaluation cache

#### FR-128.4: Smart Configuration Defaults
- **Priority**: Medium
- **Description**: Provide intelligent default configurations
- **Tasks**:
  1. Generate default loot lists from database categories
  2. Add preset configurations for different play styles
  3. Automatic detection of valuable items
  4. Configuration migration tools

### Technical Requirements

#### TECH-128.1: Performance Optimization
- Use singleton pattern to avoid repeated database loads
- Implement caching for frequent lookups
- Minimal impact on existing performance
- Memory-efficient integration

#### TECH-128.2: Backward Compatibility
- Existing configurations continue to work
- Graceful fallback for unknown items
- No breaking changes to existing API
- Migration path for legacy configs

#### TECH-128.3: Error Handling
- Robust handling of missing database
- Graceful degradation if database unavailable
- Clear error messages for configuration issues
- Logging of database integration status

## Implementation Plan

### Phase 1: Core Looting System Integration (High Priority)
**Estimated Time**: 2-3 hours

#### Task 1.1: Import and Initialize Database
```python
# Add to src/systems/looting.py
from ..utils.uo_items import get_item_database, get_item_id
```

#### Task 1.2: Replace Hardcoded Gold Detection
```python
# Replace:
if item_id == 0x06F4 or item_id == 0x06F5:  # Gold coins/piles

# With:
gold_ids = self._get_currency_ids()
if item_id in gold_ids:
```

#### Task 1.3: Add Item Identification Method
```python
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

#### Task 1.4: Enhanced Loot Evaluation
```python
def _evaluate_item_value(self, item_info: Dict[str, Any]) -> LootDecision:
    """Evaluate item using database information."""
    # Use value_tier and category for smart decisions
    # Support category-based rules
    # Implement value tier logic
```

### Phase 2: Configuration System Enhancement (High Priority)
**Estimated Time**: 2-3 hours

#### Task 2.1: Configuration Validation
```python
def _validate_loot_config(self) -> Dict[str, List[int]]:
    """Convert and validate loot configuration against database."""
    # Convert string names to IDs
    # Validate all IDs exist in database
    # Support category wildcards (e.g., "gems:*")
    # Support value tier rules (e.g., "tier:high")
```

#### Task 2.2: Smart Configuration Loading
```python
def _load_enhanced_config(self) -> None:
    """Load configuration with database enhancement."""
    # Convert strings to IDs during load
    # Cache converted configuration
    # Validate against database
    # Log conversion results
```

### Phase 3: Enhanced Features (Medium Priority)
**Estimated Time**: 2-3 hours

#### Task 3.1: Category-Based Rules
```python
# Support in config:
"always_take": [
    "gems:*",           # All gems
    "tier:very_high",   # All very high value items
    "currency:*",       # All currency
    3821               # Specific ID
]
```

#### Task 3.2: Enhanced Logging
```python
Logger.info(f"Looting {item_info['name']} ({item_info['category']}) - {item_info['value_tier']} value")
```

#### Task 3.3: Configuration Presets
```python
def generate_preset_config(preset_name: str) -> Dict:
    """Generate preset configurations using database."""
    # "conservative": currency + very_high only
    # "aggressive": currency + high + medium value
    # "gems_only": all gems
    # "custom": user-defined categories
```

### Phase 4: Testing and Integration (All Phases)
**Estimated Time**: 1-2 hours per phase

#### Task 4.1: Unit Tests
- Test database integration in looting system
- Test configuration validation
- Test item identification
- Test enhanced evaluation logic

#### Task 4.2: Integration Tests
- Test with real configurations
- Test performance impact
- Test backward compatibility
- Test error handling

#### Task 4.3: User Testing
- Test in live environment
- Validate loot decisions
- Check performance
- Verify logging improvements

## Success Criteria

### Phase 1 Success Criteria
- [ ] Looting system imports and uses UO item database
- [ ] Hardcoded gold IDs replaced with database lookup
- [ ] Item identification works for all database items
- [ ] Enhanced loot evaluation uses item metadata
- [ ] All existing functionality preserved
- [ ] Performance impact < 5%

### Phase 2 Success Criteria  
- [ ] Configuration validation against database
- [ ] String-to-ID conversion working
- [ ] Category-based rules supported
- [ ] Value tier rules supported
- [ ] Backward compatibility maintained
- [ ] Clear error messages for invalid config

### Phase 3 Success Criteria
- [ ] Preset configurations available
- [ ] Enhanced logging with item context
- [ ] Category wildcards working
- [ ] Value tier filtering working
- [ ] Configuration migration tools available

### Overall Success Criteria
- [ ] All 66+ existing tests still pass
- [ ] New integration tests pass
- [ ] Live testing successful
- [ ] Performance maintained or improved
- [ ] User experience enhanced
- [ ] Documentation updated

## Risk Assessment

### Low Risks
- **Breaking existing functionality**: Mitigated by comprehensive tests
- **Performance impact**: Mitigated by singleton pattern and caching
- **Configuration compatibility**: Mitigated by backward compatibility design

### Medium Risks
- **Complex configuration logic**: Mitigated by phased approach and testing
- **Database unavailability**: Mitigated by graceful fallback mechanisms

### Mitigation Strategies
1. **Comprehensive Testing**: Unit, integration, and live testing
2. **Phased Implementation**: Can rollback individual phases
3. **Fallback Mechanisms**: System works without database if needed
4. **Performance Monitoring**: Track impact during implementation

## Dependencies
- ✅ FR-127 (UO Item Database Optimization) - Complete
- ✅ Comprehensive test suite - Complete  
- ✅ `src/utils/uo_items.py` - Complete
- 🔄 `src/systems/looting.py` - Ready for integration
- 🔄 Configuration system - Ready for enhancement

## Effort Estimate
**Total: 6-8 hours** across 4 phases
- Phase 1: 2-3 hours (Core Integration)
- Phase 2: 2-3 hours (Configuration)  
- Phase 3: 2-3 hours (Enhanced Features)
- Phase 4: 1-2 hours (Testing per phase)

## Priority
**High** - Completes the UO Item Database optimization work and significantly improves user experience

## Acceptance Criteria
1. **Integration Complete**: All systems use database for item identification
2. **Configuration Enhanced**: Support for string names, categories, and value tiers
3. **Performance Maintained**: No significant performance degradation
4. **Backward Compatible**: Existing configurations work unchanged
5. **Well Tested**: All functionality covered by automated tests
6. **User Experience**: Better logging, smarter defaults, easier configuration

---
**Created**: 2025-06-30  
**Status**: Ready for Implementation  
**Depends On**: FR-127 (Complete)  
**Assigned**: Development Team

## Implementation Notes

### Quick Start Implementation Order:
1. **Start with Task 1.1**: Import database in looting system
2. **Continue with Task 1.2**: Replace hardcoded gold IDs  
3. **Add Task 1.3**: Item identification method
4. **Test Phase 1**: Ensure no regressions
5. **Proceed to Phase 2**: Configuration enhancement

### Code Locations:
- **Primary**: `src/systems/looting.py` (lines 540, 1015, 1053-1105)
- **Secondary**: Configuration loading logic
- **Support**: Enhanced logging and caching

### Testing Strategy:
- Run existing test suite after each task
- Add integration tests for new functionality
- Live testing with sample configurations
- Performance benchmarking

This PRD provides a clear roadmap for completing the UO Item Database integration work.
