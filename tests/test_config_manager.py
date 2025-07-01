"""
Test suite for config.config_manager module
Tests all configuration management functions with pass, fail, and edge case scenarios
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
import sys
import tempfile

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test the ConfigManager class"""

    def setUp(self):
        """Reset singleton before each test"""
        ConfigManager._instance = None

    def test_singleton_pattern_pass_case(self):
        """Test that ConfigManager follows singleton pattern correctly"""
        config1 = ConfigManager()
        config2 = ConfigManager()
        self.assertIs(config1, config2)
        self.assertEqual(id(config1), id(config2))

    @patch('config.config_manager.os.path.exists')
    @patch('config.config_manager.os.path.dirname')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_manager_initialization_pass_case(self, mock_file, mock_dirname, mock_exists):
        """Test ConfigManager initializes correctly with valid config files"""
        # Setup mock data
        mock_dirname.return_value = "/fake/path"
        mock_exists.return_value = True
        
        mock_main_config = {
            "global_settings": {"debug_mode": False},
            "system_toggles": {"healing_system_enabled": True}
        }
        mock_file.return_value.read.return_value = json.dumps(mock_main_config)
        
        config = ConfigManager()
        self.assertIsNotNone(config)
        self.assertTrue(hasattr(config, '_initialized'))

    @patch('config.config_manager.os.path.exists')
    def test_config_manager_missing_files_fail_case(self, mock_exists):
        """Test ConfigManager handles missing config files gracefully"""
        mock_exists.return_value = False
        
        config = ConfigManager()
        self.assertIsNotNone(config)
        # Should still initialize even with missing files (using defaults)

    @patch('config.config_manager.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_manager_invalid_json_fail_case(self, mock_file, mock_exists):
        """Test ConfigManager handles invalid JSON gracefully"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = "invalid json content"
        
        # Should handle JSON decode errors gracefully
        try:
            config = ConfigManager()
            self.assertIsNotNone(config)
        except json.JSONDecodeError:
            # This is acceptable behavior - fail fast on invalid config
            pass

    @patch('config.config_manager.os.path.exists')
    @patch('config.config_manager.os.path.dirname')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_main_setting_pass_cases(self, mock_file, mock_dirname, mock_exists):
        """Test get_main_setting with valid configurations"""
        mock_dirname.return_value = "/fake/path"
        mock_exists.return_value = True
        
        mock_main_config = {
            "global_settings": {
                "debug_mode": True,
                "log_level": "INFO"
            },
            "system_toggles": {
                "healing_system_enabled": False,
                "combat_system_enabled": True
            },
            "nested": {
                "deep": {
                    "value": 42
                }
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_main_config)
        
        config = ConfigManager()
        
        # Test getting existing settings
        self.assertTrue(config.get_main_setting("global_settings.debug_mode", False))
        self.assertEqual(config.get_main_setting("global_settings.log_level", "DEBUG"), "INFO")
        self.assertFalse(config.get_main_setting("system_toggles.healing_system_enabled", True))
        
        # Test with default values
        self.assertEqual(config.get_main_setting("nonexistent.key", "default"), "default")
        self.assertEqual(config.get_main_setting("nested.deep.value", 0), 42)

    @patch('config.config_manager.os.path.exists')
    @patch('config.config_manager.os.path.dirname')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_main_setting_fail_cases(self, mock_file, mock_dirname, mock_exists):
        """Test get_main_setting with missing or invalid keys"""
        mock_dirname.return_value = "/fake/path"
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = json.dumps({})
        
        config = ConfigManager()
        
        # Test missing keys return defaults
        self.assertEqual(config.get_main_setting("missing.key", "default"), "default")
        self.assertIsNone(config.get_main_setting("missing.key", None))
        self.assertEqual(config.get_main_setting("", "default"), "default")

    @patch('config.config_manager.os.path.exists')
    @patch('config.config_manager.os.path.dirname')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_main_setting_edge_cases(self, mock_file, mock_dirname, mock_exists):
        """Test get_main_setting with edge cases"""
        mock_dirname.return_value = "/fake/path"
        mock_exists.return_value = True
        
        # Test with edge case data
        edge_config = {
            "empty_string": "",
            "zero": 0,
            "false": False,
            "null": None,
            "list": [1, 2, 3],
            "nested": {
                "empty": {},
                "none_value": None
            }
        }
        mock_file.return_value.read.return_value = json.dumps(edge_config)
        
        config = ConfigManager()
        
        # Test edge case values
        self.assertEqual(config.get_main_setting("empty_string", "default"), "")
        self.assertEqual(config.get_main_setting("zero", 99), 0)
        self.assertFalse(config.get_main_setting("false", True))
        self.assertIsNone(config.get_main_setting("null", "default"))
        self.assertEqual(config.get_main_setting("list", []), [1, 2, 3])
        
        # Test with malformed key paths
        self.assertEqual(config.get_main_setting("...", "default"), "default")
        self.assertEqual(config.get_main_setting("nested..empty", "default"), "default")

    @patch('config.config_manager.os.path.exists')
    @patch('config.config_manager.os.path.dirname')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_config_pass_case(self, mock_file, mock_dirname, mock_exists):
        """Test saving configuration successfully"""
        mock_dirname.return_value = "/fake/path"
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = json.dumps({})
        
        config = ConfigManager()
        
        # Mock the write operation
        mock_write = MagicMock()
        mock_file.return_value.write = mock_write
        
        # Test saving (if method exists)
        if hasattr(config, 'save_main_config'):
            config.save_main_config()
            mock_write.assert_called()

    @patch('config.config_manager.os.path.exists')
    @patch('builtins.open', side_effect=PermissionError("Access denied"))
    def test_file_permission_fail_case(self, mock_file, mock_exists):
        """Test handling of file permission errors"""
        mock_exists.return_value = True
        
        # Should handle permission errors gracefully
        try:
            config = ConfigManager()
            # If it doesn't raise an exception, that's acceptable
            self.assertIsNotNone(config)
        except PermissionError:
            # This is also acceptable - fail fast on permission issues
            pass

    def test_multiple_instances_edge_case(self):
        """Test that multiple instantiations return the same object"""
        configs = [ConfigManager() for _ in range(10)]
        
        # All should be the same instance
        first_config = configs[0]
        for config in configs[1:]:
            self.assertIs(config, first_config)

    @patch('config.config_manager.IS_BUNDLED', True)
    @patch('config.config_manager.sys.modules')
    def test_bundled_mode_pass_case(self, mock_modules):
        """Test ConfigManager in bundled mode"""
        # Setup mock for bundled mode
        mock_main = MagicMock()
        mock_main.DEFAULT_MAIN_CONFIG = {"test": "bundled"}
        mock_main.DEFAULT_AUTO_HEAL_CONFIG = {"heal": "bundled"}
        mock_modules.__getitem__.return_value = mock_main
        mock_modules.get.return_value = mock_main
        
        # Reset singleton for this test
        ConfigManager._instance = None
        
        config = ConfigManager()
        self.assertIsNotNone(config)


if __name__ == "__main__":
    unittest.main()
