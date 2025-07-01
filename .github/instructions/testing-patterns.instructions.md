---
description: "Testing patterns and requirements for DexBot"
applyTo: "tests/**/*.py"
---

# DexBot Testing Instructions

When creating tests for DexBot, follow the 3-case testing pattern and RazorEnhanced-specific requirements.

## 3-Case Testing Pattern
Every test module must include:
1. **Pass Case**: Normal operation with expected inputs
2. **Fail Case**: Error conditions and invalid inputs  
3. **Edge Case**: Boundary conditions and unusual scenarios

## Test Structure Template
```python
import unittest
from unittest.mock import Mock, patch, MagicMock
from src.systems.example_system import ExampleSystem

class TestExampleSystem(unittest.TestCase):
    """Test suite for ExampleSystem following 3-case pattern."""
    
    def setUp(self):
        """Set up test fixtures with mocked RazorEnhanced APIs."""
        self.system = ExampleSystem()
        
    def test_normal_operation_pass_case(self):
        """Test normal system operation - PASS CASE."""
        # Test successful operation
        pass
        
    def test_error_handling_fail_case(self):
        """Test error conditions - FAIL CASE."""
        # Test error scenarios
        pass
        
    def test_boundary_conditions_edge_case(self):
        """Test edge cases and boundaries - EDGE CASE."""
        # Test unusual conditions
        pass
```

## RazorEnhanced API Mocking
Mock RazorEnhanced APIs consistently:
```python
@patch('src.systems.example_system.Player')
@patch('src.systems.example_system.Items')
def test_with_razor_apis(self, mock_items, mock_player):
    """Test with mocked RazorEnhanced APIs."""
    # Configure mocks
    mock_player.Name = "TestPlayer"
    mock_player.Hits = 100
    mock_items.FindBySerial.return_value = Mock()
    
    # Run test
    result = self.system.update()
    
    # Verify behavior
    self.assertTrue(result)
    mock_items.FindBySerial.assert_called_once()
```

## Performance Testing
Include performance benchmarks:
```python
def test_performance_requirements(self):
    """Test system meets performance requirements."""
    import time
    
    start_time = time.time()
    for _ in range(1000):
        self.system.update()
    end_time = time.time()
    
    # Should complete 1000 updates in under 1 second
    self.assertLess(end_time - start_time, 1.0)
```

## Memory Testing
Test for memory leaks in long-running scenarios:
```python
def test_memory_usage_long_session(self):
    """Test memory usage during extended operation."""
    import gc
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Simulate long session
    for _ in range(10000):
        self.system.update()
        
    gc.collect()
    final_memory = process.memory_info().rss
    
    # Memory should not increase by more than 10MB
    memory_increase = final_memory - initial_memory
    self.assertLess(memory_increase, 10 * 1024 * 1024)
```

## Test Data Patterns
Use realistic UO data:
```python
# Realistic item serials (8-digit hex)
VALID_ITEM_SERIAL = 0x12345678
INVALID_ITEM_SERIAL = 0x00000000

# Realistic mobile serials
PLAYER_SERIAL = 0x87654321
MONSTER_SERIAL = 0x11223344

# Common UO item IDs
ITEM_ID_GOLD = 0x0EED
ITEM_ID_BANDAGE = 0x0E21
ITEM_ID_GREATER_HEAL_POTION = 0x0F0C
```

## Integration Testing
Test system interactions:
```python
def test_system_integration(self):
    """Test integration between multiple systems."""
    auto_heal = AutoHealSystem()
    combat = CombatSystem()
    
    # Test that systems work together correctly
    # without interfering with each other
    pass
```

## Configuration Testing
Test all configuration scenarios:
```python
def test_configuration_variations(self):
    """Test different configuration settings."""
    configs = [
        {'enabled': True, 'threshold': 50},
        {'enabled': False, 'threshold': 75},
        {'enabled': True, 'threshold': 100}
    ]
    
    for config in configs:
        with self.subTest(config=config):
            system = ExampleSystem()
            system.config = config
            # Test behavior with this config
            pass
```
