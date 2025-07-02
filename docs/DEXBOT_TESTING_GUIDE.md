# DexBot Testing Guide

## Overview

This document outlines the comprehensive testing approach used in the DexBot project, a high-performance modular bot system for Ultima Online that uses the RazorEnhanced scripting environment. DexBot emphasizes clean architecture, comprehensive testing, and production-ready code quality.

## Testing Philosophy

DexBot employs a robust testing strategy built on the "3-case pattern":

1. **Pass Case**: Tests expected normal operation
2. **Fail Case**: Tests proper handling of error conditions
3. **Edge Case**: Tests boundary conditions and unusual inputs

All systems must pass these three types of tests to be considered production-ready.

## Testing Tools and Infrastructure

### Test Execution

DexBot provides several VS Code tasks for test execution:

- **DexBot: Run Phase 1 Interactive Tests**: Executes the initial test suite with user interaction
- **DexBot: Run Enhanced Automated Tests**: Runs a more comprehensive automated test suite
- **DexBot: Monitor RazorEnhanced Output**: Captures live output from RazorEnhanced during testing
- **DexBot: Generate Test Report**: Creates a summary of test results

### Test Locations

Tests are organized in the `tests/` directory with several key files:

- `test_automation.py`: Core testing framework for interactive tests
- `test_automation_enhanced.py`: Extended testing framework with VS Code integration

## Mock Testing Approach

Since RazorEnhanced operations can't be easily tested in isolation, DexBot employs a sophisticated mock testing framework.

### Mock Infrastructure

1. **RazorEnhanced API Mocks**: Simulated versions of the RazorEnhanced API endpoints
2. **Test Data Fixtures**: Predefined test data that mimics real UO gameplay scenarios
3. **Test Environment**: Isolated test environment that prevents real game interactions

### Mock Testing Process

```python
# Example of mock test for Auto Heal system
def test_auto_heal_bandage_usage(mock_player, mock_journal, mock_items):
    """
    Test that the Auto Heal system correctly uses bandages when health is low.
    """
    # Arrange
    mock_player.Hits = 50          # Set player health to 50%
    mock_player.HitsMax = 100      # Set max health to 100
    mock_items.add_backpack_item("bandage", 5)  # Add 5 bandages to inventory
    
    # Act
    auto_heal_system = AutoHealSystem()
    auto_heal_system.execute_auto_heal_system()
    
    # Assert
    assert mock_items.was_used("bandage")
    assert mock_journal.was_written("You begin applying the bandages")
```

## Test Reporting

All test runs generate detailed reports saved in the `tmp/` directory as JSON files. These reports include:

- Test case name and description
- Pass/fail status
- Execution time
- Error messages (if applicable)
- System resource usage

## Continuous Integration

Test execution is an integral part of the development workflow:

```powershell
# Standard development workflow
python -m invoke validate    # Check system integrity
python -m invoke test        # Run comprehensive test suite
python -m invoke build       # Build and validate bundled DexBot.py
```

## System-Specific Testing Approaches

### Auto Heal System

Tests focus on:
- Proper bandage usage based on health thresholds
- Correct potion usage when bandages are unavailable
- Resource management and inventory tracking
- Journal message processing

### Combat System

Tests focus on:
- Target selection and prioritization
- Attack execution and timing
- Special ability usage
- Combat state management

### Looting System

Tests focus on:
- Corpse detection and management
- Item evaluation based on configuration
- Inventory management during looting
- Performance optimization for large corpse counts

## Performance Testing

DexBot's 12+ hour runtime requirement necessitates extensive performance testing:

1. **Resource Consumption**: Memory and CPU usage monitoring
2. **Long-running Tests**: Extended execution to detect memory leaks
3. **Load Testing**: Simulating high-stress scenarios (multiple targets, corpses)
4. **Bottleneck Identification**: Profiling to find and eliminate performance issues

## Test-Driven Development Process

New features should follow this testing workflow:

1. Write test cases first (pass/fail/edge)
2. Implement minimal code to pass tests
3. Refactor for performance and clarity
4. Verify all tests still pass
5. Document test cases and implementation details

## Test Maintenance

Test suite maintenance is a critical ongoing task:

- Update tests when API changes occur
- Add new test cases for bug fixes
- Improve test performance regularly
- Keep mock data current with game updates

## Troubleshooting Tests

Common test issues and solutions:

- **Failing Tests**: Check for API changes, mock data inconsistencies
- **Slow Tests**: Review for unnecessary pauses, optimize mock operations
- **Inconsistent Results**: Verify deterministic test setup, check for race conditions
- **Environment Issues**: Ensure RazorEnhanced version compatibility

## Best Practices

1. **Isolation**: Each test should run independently
2. **Repeatability**: Tests should produce the same results on every run
3. **Speed**: Tests should execute quickly to enable frequent validation
4. **Clarity**: Test intent should be clear from name and comments
5. **Coverage**: Tests should cover all code paths and edge cases

## Example: Complete Test Case

```python
"""
Test the Auto Heal system with full 3-case pattern coverage.
"""

def test_auto_heal_normal_operation():
    """
    PASS CASE: Test normal operation of Auto Heal with sufficient resources.
    """
    # Arrange - Set up normal conditions
    mock_player.Hits = 60
    mock_player.HitsMax = 100
    mock_items.add_backpack_item("bandage", 10)
    config = BotConfig()
    config.HEALING_ENABLED = True
    config.BANDAGE_HEALING_ENABLED = True
    
    # Act
    auto_heal_system = AutoHealSystem(config)
    result = auto_heal_system.execute_auto_heal_system()
    
    # Assert
    assert result.success is True
    assert mock_items.get_backpack_count("bandage") == 9
    assert mock_journal.contains("You begin applying the bandages")

def test_auto_heal_no_resources():
    """
    FAIL CASE: Test Auto Heal behavior when no healing resources are available.
    """
    # Arrange - Set up failure conditions
    mock_player.Hits = 40
    mock_player.HitsMax = 100
    mock_items.clear_backpack()
    config = BotConfig()
    config.HEALING_ENABLED = True
    
    # Act
    auto_heal_system = AutoHealSystem(config)
    result = auto_heal_system.execute_auto_heal_system()
    
    # Assert
    assert result.success is False
    assert result.error_code == "NO_HEALING_RESOURCES"
    assert mock_logger.contains("No healing resources available")

def test_auto_heal_edge_health_threshold():
    """
    EDGE CASE: Test Auto Heal at exact health threshold boundary.
    """
    # Arrange - Set up edge conditions
    mock_player.Hits = 75  # Exactly at threshold
    mock_player.HitsMax = 100
    mock_items.add_backpack_item("bandage", 5)
    config = BotConfig()
    config.HEALING_ENABLED = True
    config.HEALING_THRESHOLD = 75
    
    # Act
    auto_heal_system = AutoHealSystem(config)
    result = auto_heal_system.execute_auto_heal_system()
    
    # Assert
    assert result.success is True
    assert mock_items.was_used("bandage")
```

## Conclusion

Comprehensive testing is essential for DexBot's reliability during extended operation. By following the testing patterns and practices outlined in this guide, developers can ensure that all systems maintain the high quality standards required for production use.
