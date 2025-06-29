"""
Configuration Management System for DexBot
Handles loading and saving bot settings from JSON files
"""

import json
import os
from typing import Dict, Optional


class ConfigManager:
    """Configuration manager for loading and saving bot settings from JSON files

    Manages separate configuration files for different bot systems:
    - main_config.json: Overall bot settings and system toggles
    - auto_heal_config.json: Auto Heal system specific settings
    """

    _instance: Optional["ConfigManager"] = None

    def __new__(cls) -> "ConfigManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        # Get the script directory and config path
        self.script_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.config_dir = os.path.join(self.script_dir, "config")

        # Ensure config directory exists
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # Configuration file paths
        self.main_config_path = os.path.join(self.config_dir, "main_config.json")
        self.auto_heal_config_path = os.path.join(self.config_dir, "auto_heal_config.json")

        # Load configurations
        self.main_config = self._load_config(self.main_config_path, {})
        self.auto_heal_config = self._load_config(self.auto_heal_config_path, {})

    def _load_config(self, config_path: str, default_config: Dict) -> Dict:
        """Load configuration from JSON file, create with defaults if not exists"""
        try:
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_configs(default_config, config)
            else:
                # Create default config file
                self._save_config(config_path, default_config)
                return default_config
        except Exception as e:
            print(f"[ConfigManager] Error loading {config_path}: {e}")
            return default_config

    def _save_config(self, config_path: str, config: Dict) -> bool:
        """Save configuration to JSON file"""
        try:
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"[ConfigManager] Error saving {config_path}: {e}")
            return False

    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Recursively merge loaded config with defaults to ensure all keys exist"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def save_main_config(self) -> bool:
        """Save main configuration to file"""
        return self._save_config(self.main_config_path, self.main_config)

    def save_auto_heal_config(self) -> bool:
        """Save auto heal configuration to file"""
        return self._save_config(self.auto_heal_config_path, self.auto_heal_config)

    def save_all_configs(self) -> bool:
        """Save all configuration files"""
        main_saved = self.save_main_config()
        auto_heal_saved = self.save_auto_heal_config()
        return main_saved and auto_heal_saved

    def reload_configs(self) -> None:
        """Reload all configurations from files"""
        self.main_config = self._load_config(self.main_config_path, {})
        self.auto_heal_config = self._load_config(self.auto_heal_config_path, {})

    def get_main_setting(self, key_path: str, default=None):
        """Get setting from main config using dot notation (e.g., 'system_toggles.healing_system_enabled')"""
        return self._get_nested_value(self.main_config, key_path, default)

    def set_main_setting(self, key_path: str, value) -> None:
        """Set setting in main config using dot notation"""
        self._set_nested_value(self.main_config, key_path, value)

    def get_auto_heal_setting(self, key_path: str, default=None):
        """Get setting from auto heal config using dot notation"""
        return self._get_nested_value(self.auto_heal_config, key_path, default)

    def set_auto_heal_setting(self, key_path: str, value) -> None:
        """Set setting in auto heal config using dot notation"""
        self._set_nested_value(self.auto_heal_config, key_path, value)

    def _get_nested_value(self, config: Dict, key_path: str, default=None):
        """Get nested dictionary value using dot notation"""
        try:
            keys = key_path.split(".")
            value = config
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def _set_nested_value(self, config: Dict, key_path: str, value) -> None:
        """Set nested dictionary value using dot notation"""
        keys = key_path.split(".")
        current = config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
