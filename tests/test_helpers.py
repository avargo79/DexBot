"""
Test suite for utils.helpers module
Tests all utility functions with pass, fail, and edge case scenarios
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.helpers import get_resource_color, check_bandage_supply, has_healing_resources


class TestHelperFunctions(unittest.TestCase):
    """Test the utility helper functions"""

    def test_get_resource_color_pass_cases(self):
        """Test get_resource_color with valid passing cases"""
        # High amount - should return green
        self.assertEqual(get_resource_color(100, 50, 25), "#00FF00")
        self.assertEqual(get_resource_color(75, 50, 25), "#00FF00")
        self.assertEqual(get_resource_color(51, 50, 25), "#00FF00")
        
        # Medium amount - should return yellow
        self.assertEqual(get_resource_color(50, 50, 25), "#FFFF00")
        self.assertEqual(get_resource_color(30, 50, 25), "#FFFF00")
        self.assertEqual(get_resource_color(26, 50, 25), "#FFFF00")
        
        # Low amount - should return red
        self.assertEqual(get_resource_color(25, 50, 25), "#FF6B6B")
        self.assertEqual(get_resource_color(10, 50, 25), "#FF6B6B")
        self.assertEqual(get_resource_color(0, 50, 25), "#FF6B6B")

    def test_get_resource_color_edge_cases(self):
        """Test get_resource_color with edge cases"""
        # Boundary conditions
        self.assertEqual(get_resource_color(50, 49, 25), "#00FF00")  # Just above high threshold
        self.assertEqual(get_resource_color(25, 50, 24), "#00FF00")  # Medium threshold edge
        
        # Zero thresholds
        self.assertEqual(get_resource_color(1, 0, 0), "#00FF00")
        self.assertEqual(get_resource_color(0, 0, 0), "#FF6B6B")
        
        # Negative values
        self.assertEqual(get_resource_color(-1, 10, 5), "#FF6B6B")
        self.assertEqual(get_resource_color(10, -5, -10), "#00FF00")
        
        # Same thresholds
        self.assertEqual(get_resource_color(10, 10, 10), "#FF6B6B")
        
        # Very large numbers
        self.assertEqual(get_resource_color(999999, 100000, 50000), "#00FF00")

    @patch('utils.helpers.Items')
    @patch('utils.helpers.Logger')
    @patch('utils.helpers.BotConfig')
    @patch('utils.helpers.BotMessages')
    def test_check_bandage_supply_pass_cases(self, mock_messages, mock_config, mock_logger, mock_items):
        """Test check_bandage_supply with valid passing cases"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_instance.BANDAGE_ID = 3617
        mock_config_instance.LOW_BANDAGE_WARNING = 10
        mock_config.return_value = mock_config_instance
        
        mock_messages_instance = MagicMock()
        mock_messages_instance.LOW_BANDAGES = "Low bandages: {}"
        mock_messages_instance.NO_BANDAGES = "No bandages found"
        mock_messages.return_value = mock_messages_instance
        
        # Test with sufficient bandages
        mock_items.BackpackCount.return_value = 50
        result = check_bandage_supply()
        self.assertEqual(result, 50)
        mock_logger.warning.assert_not_called()
        
        # Test with low bandages (should warn)
        mock_items.BackpackCount.return_value = 5
        result = check_bandage_supply()
        self.assertEqual(result, 5)
        mock_logger.warning.assert_called_once()
        
        # Test with exact threshold (should warn)
        mock_logger.warning.reset_mock()
        mock_items.BackpackCount.return_value = 10
        result = check_bandage_supply()
        self.assertEqual(result, 10)
        mock_logger.warning.assert_called_once()

    @patch('utils.helpers.Items')
    @patch('utils.helpers.Logger')
    @patch('utils.helpers.BotConfig')
    @patch('utils.helpers.BotMessages')
    def test_check_bandage_supply_fail_cases(self, mock_messages, mock_config, mock_logger, mock_items):
        """Test check_bandage_supply with failure cases"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_instance.BANDAGE_ID = 3617
        mock_config_instance.LOW_BANDAGE_WARNING = 10
        mock_config.return_value = mock_config_instance
        
        mock_messages_instance = MagicMock()
        mock_messages_instance.NO_BANDAGES = "No bandages found"
        mock_messages.return_value = mock_messages_instance
        
        # Test with no bandages
        mock_items.BackpackCount.return_value = 0
        result = check_bandage_supply()
        self.assertEqual(result, 0)
        mock_logger.error.assert_called_once_with("No bandages found")
        
        # Test with no bandages and log_errors=False
        mock_logger.error.reset_mock()
        result = check_bandage_supply(log_errors=False)
        self.assertEqual(result, 0)
        mock_logger.error.assert_not_called()

    @patch('utils.helpers.Items')
    @patch('utils.helpers.Logger')
    @patch('utils.helpers.BotConfig')
    @patch('utils.helpers.BotMessages')
    def test_check_bandage_supply_edge_cases(self, mock_messages, mock_config, mock_logger, mock_items):
        """Test check_bandage_supply with edge cases"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_instance.BANDAGE_ID = 3617
        mock_config_instance.LOW_BANDAGE_WARNING = 10
        mock_config.return_value = mock_config_instance
        
        mock_messages_instance = MagicMock()
        mock_messages_instance.LOW_BANDAGES = "Low bandages: {}"
        mock_messages.return_value = mock_messages_instance
        
        # Test with negative count (should be treated as 0)
        mock_items.BackpackCount.return_value = -1
        result = check_bandage_supply()
        self.assertEqual(result, 0)
        
        # Test with very large count
        mock_items.BackpackCount.return_value = 999999
        result = check_bandage_supply()
        self.assertEqual(result, 999999)
        
        # Test with threshold of 0
        mock_config_instance.LOW_BANDAGE_WARNING = 0
        mock_items.BackpackCount.return_value = 1
        result = check_bandage_supply()
        self.assertEqual(result, 1)
        mock_logger.warning.assert_not_called()

    @patch('utils.helpers.Items')
    @patch('utils.helpers.BotConfig')
    def test_has_healing_resources_pass_cases(self, mock_config, mock_items):
        """Test has_healing_resources with valid passing cases"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_instance.BANDAGE_ID = 3617
        mock_config_instance.HEAL_POTION_ID = 3852
        mock_config.return_value = mock_config_instance
        
        # Test with both resources available
        mock_items.BackpackCount.side_effect = [5, 3]  # bandages, potions
        has_bandages, has_potions = has_healing_resources()
        self.assertTrue(has_bandages)
        self.assertTrue(has_potions)
        
        # Test with only bandages
        mock_items.BackpackCount.side_effect = [5, 0]
        has_bandages, has_potions = has_healing_resources()
        self.assertTrue(has_bandages)
        self.assertFalse(has_potions)
        
        # Test with only potions
        mock_items.BackpackCount.side_effect = [0, 3]
        has_bandages, has_potions = has_healing_resources()
        self.assertFalse(has_bandages)
        self.assertTrue(has_potions)

    @patch('utils.helpers.Items')
    @patch('utils.helpers.BotConfig')
    def test_has_healing_resources_fail_cases(self, mock_config, mock_items):
        """Test has_healing_resources with failure cases"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_instance.BANDAGE_ID = 3617
        mock_config_instance.HEAL_POTION_ID = 3852
        mock_config.return_value = mock_config_instance
        
        # Test with no resources
        mock_items.BackpackCount.side_effect = [0, 0]
        has_bandages, has_potions = has_healing_resources()
        self.assertFalse(has_bandages)
        self.assertFalse(has_potions)

    @patch('utils.helpers.Items')
    @patch('utils.helpers.BotConfig')
    def test_has_healing_resources_edge_cases(self, mock_config, mock_items):
        """Test has_healing_resources with edge cases"""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_instance.BANDAGE_ID = 3617
        mock_config_instance.HEAL_POTION_ID = 3852
        mock_config.return_value = mock_config_instance
        
        # Test with negative counts (should be treated as False)
        mock_items.BackpackCount.side_effect = [-1, -1]
        has_bandages, has_potions = has_healing_resources()
        self.assertFalse(has_bandages)
        self.assertFalse(has_potions)
        
        # Test with very large counts
        mock_items.BackpackCount.side_effect = [999999, 999999]
        has_bandages, has_potions = has_healing_resources()
        self.assertTrue(has_bandages)
        self.assertTrue(has_potions)
        
        # Test with BackpackCount raising exception
        mock_items.BackpackCount.side_effect = Exception("Mock error")
        with self.assertRaises(Exception):
            has_healing_resources()


if __name__ == "__main__":
    unittest.main()
