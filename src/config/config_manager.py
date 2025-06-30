"""
Configuration Management System for DexBot
Handles loading and saving bot settings from JSON files
"""

import json
import os
import sys
from typing import Dict, Optional


# Helper to detect if running as bundled script (DexBot.py) or as modules
IS_BUNDLED = hasattr(sys.modules.get('__main__'), 'DEFAULT_MAIN_CONFIG')

if IS_BUNDLED:
    DEFAULT_MAIN_CONFIG = sys.modules['__main__'].DEFAULT_MAIN_CONFIG
    DEFAULT_AUTO_HEAL_CONFIG = sys.modules['__main__'].DEFAULT_AUTO_HEAL_CONFIG
    DEFAULT_LOOTING_CONFIG = getattr(sys.modules['__main__'], 'DEFAULT_LOOTING_CONFIG', {})
else:
    # Load from JSON files in development mode
    def load_json_config(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    import os as _os
    _config_dir = _os.path.dirname(_os.path.abspath(__file__))
    DEFAULT_MAIN_CONFIG = load_json_config(_os.path.join(_config_dir, 'default_main_config.json'))
    DEFAULT_AUTO_HEAL_CONFIG = load_json_config(_os.path.join(_config_dir, 'default_auto_heal_config.json'))
    DEFAULT_LOOTING_CONFIG = load_json_config(_os.path.join(_config_dir, 'default_looting_config.json'))


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
        self.combat_config_path = os.path.join(self.config_dir, "combat_config.json")
        self.looting_config_path = os.path.join(self.config_dir, "looting_config.json")

        # Load configurations
        self.main_config = self._load_config(self.main_config_path, self._get_default_main_config())
        self.auto_heal_config = self._load_config(
            self.auto_heal_config_path, self._get_default_auto_heal_config()
        )
        self.combat_config = self._load_config(
            self.combat_config_path, self._get_default_combat_config()
        )
        self.looting_config = self._load_config(
            self.looting_config_path, self._get_default_looting_config()
        )

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

    def save_combat_config(self) -> bool:
        """Save combat configuration to file"""
        return self._save_config(self.combat_config_path, self.combat_config)

    def save_looting_config(self, config: Dict = None) -> bool:
        """Save looting configuration to file"""
        if config is not None:
            self.looting_config = config
        return self._save_config(self.looting_config_path, self.looting_config)

    def save_all_configs(self) -> bool:
        """Save all configuration files"""
        main_saved = self.save_main_config()
        auto_heal_saved = self.save_auto_heal_config()
        combat_saved = self.save_combat_config()
        looting_saved = self.save_looting_config()
        return main_saved and auto_heal_saved and combat_saved and looting_saved

    def reload_configs(self) -> None:
        """Reload all configurations from files"""
        self.main_config = self._load_config(self.main_config_path, self._get_default_main_config())
        self.auto_heal_config = self._load_config(
            self.auto_heal_config_path, self._get_default_auto_heal_config()
        )
        self.combat_config = self._load_config(
            self.combat_config_path, self._get_default_combat_config()
        )
        self.looting_config = self._load_config(
            self.looting_config_path, self._get_default_looting_config()
        )

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

    def get_combat_setting(self, key_path: str, default=None):
        """Get setting from combat config using dot notation"""
        return self._get_nested_value(self.combat_config, key_path, default)

    def set_combat_setting(self, key_path: str, value) -> None:
        """Set setting in combat config using dot notation"""
        self._set_nested_value(self.combat_config, key_path, value)

    def get_looting_setting(self, key_path: str, default=None):
        """Get setting from looting config using dot notation"""
        return self._get_nested_value(self.looting_config, key_path, default)

    def set_looting_setting(self, key_path: str, value) -> None:
        """Set setting in looting config using dot notation"""
        self._set_nested_value(self.looting_config, key_path, value)

    def get_looting_config(self) -> Dict:
        """Get the entire looting configuration"""
        return self.looting_config

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

    def _get_default_main_config(self) -> Dict:
        """Get default main configuration"""
        return {
            "version": "2.0",
            "last_updated": "2025-06-28",
            "description": "DexBot Main Configuration - System toggles and global settings",
            "system_toggles": {"healing_system_enabled": True},
            "global_settings": {
                "debug_mode": False,
                "main_loop_delay_ms": 250,
                "error_recovery_delay_ms": 1000,
                "target_wait_timeout_ms": 1000,
            },
            "gump_interface": {
                "enabled": True,
                "main_gump": {
                    "width": 320,
                    "height": 240,
                    "x_position": 100,
                    "y_position": 100,
                    "update_interval_cycles": 8,
                },
                "minimized_gump": {"width": 100, "height": 30},
                "rate_limiting": {"button_press_delay_ms": 500},
            },
            "safety_settings": {
                "connection_check_enabled": True,
                "death_pause_enabled": True,
                "emergency_stop_on_critical_error": True,
            },
            "logging": {
                "console_logging": True,
                "file_logging": False,
                "log_level": "info",
                "debug_status_interval_cycles": 20,
            },
        }

    def _get_default_auto_heal_config(self) -> Dict:
        """Get default auto heal configuration"""
        return {
            "version": "2.0",
            "last_updated": "2025-06-28",
            "description": "DexBot Auto Heal System Configuration",
            "healing_toggles": {"bandage_healing_enabled": True, "potion_healing_enabled": True},
            "health_thresholds": {
                "healing_threshold_percentage": 95,
                "critical_health_threshold": 50,  # Default value, matches actual config and code behavior
                "bandage_threshold_hp": 1,
            },
            "item_ids": {
                "bandage_id": "0x0E21",
                "heal_potion_id": "0x0F0C",
                "lesser_heal_potion_id": None,
                "greater_heal_potion_id": None,
            },
            "timing_settings": {
                "healing_timer_duration_ms": 11000,
                "potion_cooldown_ms": 10000,
                "bandage_retry_delay_ms": 500,
                "healing_check_interval": 1,
            },
            "resource_management": {
                "bandage_retry_attempts": 3,
                "low_bandage_warning": 10,
                "search_range": 2,
                "bandage_check_interval_cycles": 120,
            },
            "journal_monitoring": {
                "healing_success_msg": "You finish applying the bandages.",
                "healing_partial_msg": "You apply the bandages, but they barely help.",
                "journal_message_type": "System",
            },
            "color_thresholds": {
                "bandage_high_threshold": 20,
                "bandage_medium_threshold": 10,
                "potion_high_threshold": 10,
                "potion_medium_threshold": 5,
                "health_high_threshold": 75,
                "health_medium_threshold": 50,
            },
        }

    def _get_default_combat_config(self) -> Dict:
        """Get default combat configuration"""
        return {
            "description": "DexBot Combat System Configuration - Only activates when player is in War Mode",
            "version": "1.4",
            "last_updated": "2025-06-29",
            "system_toggles": {
                "combat_system_enabled": False,
                "auto_target_enabled": True,
                "auto_attack_enabled": True
            },
            "target_selection": {
                "max_range": 10,
                "priority_mode": "closest",
                "target_types": ["monsters", "hostiles"],
                "ignore_innocents": True,
                "ignore_pets": True,
                "allow_target_blues": False
            },
            "combat_behavior": {
                "attack_delay_ms": 250,
                "target_switch_delay_ms": 500,
                "combat_timeout_ms": 30000,
                "retreat_on_low_health": True,
                "retreat_health_threshold": 30
            },
            "weapon_settings": {
                "auto_equip_weapon": False,
                "preferred_weapon_type": "any",
                "weapon_durability_warning": 10
            },
            "timing_settings": {
                "combat_check_interval": 250,
                "target_scan_interval": 250,
                "combat_loop_delay_ms": 250
            },
            "display_settings": {
                "show_target_name_overhead": True,
                "target_name_display_interval_ms": 3000,
                "target_name_display_color": 53
            }
        }

    def _get_default_looting_config(self) -> Dict:
        """Get default looting configuration"""
        return {
            "version": "1.0",
            "enabled": True,  # Enable by default for testing
            "timing": {
                "corpse_scan_interval_ms": 1000,
                "loot_action_delay_ms": 200,
                "container_open_timeout_ms": 2000,
                "skinning_action_delay_ms": 500
            },
            "behavior": {
                "max_looting_range": 2,  # Reduced from 3 to 2 for better performance
                "auto_skinning_enabled": True,
                "inventory_weight_limit_percent": 90,
                "inventory_item_limit": 120,
                "process_corpses_in_combat": False,
                "prioritize_skinning_over_looting": True
            },
            "loot_lists": {
                "always_take": [
                    1712,  # Gold item ID for reliable detection
                    "Gold", "Coins", "Gem", "Diamond", "Ruby", "Emerald", "Sapphire",
                    "Citrine", "Amethyst", "Tourmaline", "Star Sapphire", "Rare", "Magic"
                ],
                "take_if_space": [
                    "Weapon", "Sword", "Bow", "Crossbow", "Mace", "Staff", "Armor",
                    "Shield", "Helmet", "Ring", "Bracelet", "Necklace", "Reagent",
                    "Potion", "Arrow", "Bolt", "Ingot", "Hide", "Leather", "Cloth"
                ],
                "never_take": [
                    "Bottle", "Empty Bottle", "Bone", "Bones", "Skull", "Ribs",
                    "Candle", "Torch", "Lantern", "Lockpick", "Key", "Hair Dye"
                ]
            },
            "skinning": {
                "enabled": True,
                "require_skinning_knife": True,
                "auto_buy_knives": False,
                "skinnable_creatures": [
                    "Bear", "Wolf", "Deer", "Rabbit", "Cow", "Bull", "Horse",
                    "Sheep", "Goat", "Pig", "Chicken", "Bird", "Eagle"
                ]
            },
            "performance": {
                "max_corpse_queue_size": 10,
                "cache_cleanup_interval_seconds": 60,
                "max_cache_size": 1000,
                "batch_item_processing": True,
                "parallel_skinning_looting": False
            },
            "safety": {
                "pause_on_player_nearby": False,
                "pause_on_combat": True,
                "emergency_stop_conditions": [
                    "inventory_full", "low_health", "player_detected"
                ],
                "max_looting_time_per_corpse_seconds": 30
            },
            "ui": {
                "show_loot_notifications": True,
                "show_skinning_notifications": True,
                "display_stats_in_gump": True,
                "notification_color": 53,
                "stats_update_interval_ms": 1000
            }
        }
