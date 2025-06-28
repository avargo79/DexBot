"""
DexBot.py - Modular Dexxor Bot System
A modular bot system with Auto Heal as the first component.

Author: RugRat79
Version: 1.0
License: MIT
"""

from AutoComplete import *
from typing import Dict, List, Optional, Union, Tuple
import time
import json
import os

# ===========================================
# CONFIGURATION MANAGEMENT SYSTEM
# ===========================================

class ConfigManager:
    """Configuration manager for loading and saving bot settings from JSON files
    
    Manages separate configuration files for different bot systems:
    - main_config.json: Overall bot settings and system toggles
    - auto_heal_config.json: Auto Heal system specific settings
    """
    _instance: Optional['ConfigManager'] = None
    
    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        
        # Get the script directory and config path
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_dir = os.path.join(self.script_dir, "config")
        
        # Ensure config directory exists
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # Configuration file paths
        self.main_config_path = os.path.join(self.config_dir, "main_config.json")
        self.auto_heal_config_path = os.path.join(self.config_dir, "auto_heal_config.json")
        
        # Load configurations
        self.main_config = self._load_config(self.main_config_path, self._get_default_main_config())
        self.auto_heal_config = self._load_config(self.auto_heal_config_path, self._get_default_auto_heal_config())
    
    def _load_config(self, config_path: str, default_config: Dict) -> Dict:
        """Load configuration from JSON file, create with defaults if not exists"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
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
            with open(config_path, 'w') as f:
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
        self.main_config = self._load_config(self.main_config_path, self._get_default_main_config())
        self.auto_heal_config = self._load_config(self.auto_heal_config_path, self._get_default_auto_heal_config())
    
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
            keys = key_path.split('.')
            value = config
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def _set_nested_value(self, config: Dict, key_path: str, value) -> None:
        """Set nested dictionary value using dot notation"""
        keys = key_path.split('.')
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
            "system_toggles": {
                "healing_system_enabled": True,
                "combat_system_enabled": False,
                "looting_system_enabled": False,
                "fishing_system_enabled": False,
                "buff_system_enabled": False,
                "weapon_management_enabled": False,
                "inventory_management_enabled": False
            },
            "global_settings": {
                "debug_mode": False,
                "main_loop_delay_ms": 250,
                "error_recovery_delay_ms": 1000,
                "target_wait_timeout_ms": 1000
            },
            "gump_interface": {
                "enabled": True,
                "main_gump": {
                    "width": 320,
                    "height": 240,
                    "x_position": 100,
                    "y_position": 100,
                    "update_interval_cycles": 8
                },
                "minimized_gump": {
                    "width": 100,
                    "height": 30
                },
                "rate_limiting": {
                    "button_press_delay_ms": 500
                }
            },
            "safety_settings": {
                "connection_check_enabled": True,
                "death_pause_enabled": True,
                "emergency_stop_on_critical_error": True
            },
            "logging": {
                "console_logging": True,
                "file_logging": False,
                "log_level": "info",
                "debug_status_interval_cycles": 20
            }
        }
    
    def _get_default_auto_heal_config(self) -> Dict:
        """Get default auto heal configuration"""
        return {
            "version": "2.0",
            "last_updated": "2025-06-28",
            "description": "DexBot Auto Heal System Configuration",
            "healing_toggles": {
                "bandage_healing_enabled": True,
                "potion_healing_enabled": True
            },
            "health_thresholds": {
                "healing_threshold_percentage": 95,
                "critical_health_threshold": 50,
                "bandage_threshold_hp": 1
            },
            "item_ids": {
                "bandage_id": "0x0E21",
                "heal_potion_id": "0x0F0C",
                "lesser_heal_potion_id": None,
                "greater_heal_potion_id": None
            },
            "timing_settings": {
                "healing_timer_duration_ms": 11000,
                "potion_cooldown_ms": 10000,
                "bandage_retry_delay_ms": 500,
                "healing_check_interval": 1
            },
            "resource_management": {
                "bandage_retry_attempts": 3,
                "low_bandage_warning": 10,
                "search_range": 2,
                "bandage_check_interval_cycles": 120
            },
            "journal_monitoring": {
                "healing_success_msg": "You finish applying the bandages.",
                "healing_partial_msg": "You apply the bandages, but they barely help.",
                "journal_message_type": "System"
            },
            "color_thresholds": {
                "bandage_high_threshold": 20,
                "bandage_medium_threshold": 10,
                "potion_high_threshold": 10,
                "potion_medium_threshold": 5,
                "health_high_threshold": 75,
                "health_medium_threshold": 50
            }
        }

# ===========================================
# ENUMS AND STATE MANAGEMENT
# ===========================================

class GumpState:
    """Simple enumeration of possible GUMP states (using class constants for compatibility)"""
    CLOSED = "closed"
    MAIN_FULL = "main_full"
    MAIN_MINIMIZED = "main_minimized"
    AUTO_HEAL_SETTINGS = "auto_heal_settings"
    COMBAT_SETTINGS = "combat_settings"
    LOOTING_SETTINGS = "looting_settings"

# ===========================================
# CONSTANTS AND CONFIGURATION
# ===========================================

class BotConfig:
    """Configuration constants for DexBot - now loads from JSON config files
    
    This class manages all configuration constants using the Singleton pattern
    and ConfigManager for persistent storage.
    """
    _instance: Optional['BotConfig'] = None
    
    def __new__(cls) -> 'BotConfig':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        
        # Initialize config manager
        self.config_manager = ConfigManager()
        self._load_settings()
    
    def _load_settings(self) -> None:
        """Load all settings from configuration files"""
        # System toggles from main config
        self.HEALING_ENABLED = self.config_manager.get_main_setting('system_toggles.healing_system_enabled', True)
        self.COMBAT_ENABLED = self.config_manager.get_main_setting('system_toggles.combat_system_enabled', False)
        self.LOOTING_ENABLED = self.config_manager.get_main_setting('system_toggles.looting_system_enabled', False)
        self.FISHING_ENABLED = self.config_manager.get_main_setting('system_toggles.fishing_system_enabled', False)
        self.DEBUG_MODE = self.config_manager.get_main_setting('global_settings.debug_mode', False)
        
        # Auto Heal specific toggles
        self.BANDAGE_HEALING_ENABLED = self.config_manager.get_auto_heal_setting('healing_toggles.bandage_healing_enabled', True)
        self.POTION_HEALING_ENABLED = self.config_manager.get_auto_heal_setting('healing_toggles.potion_healing_enabled', True)
        
        # Item IDs (convert hex strings to integers)
        bandage_id_str = self.config_manager.get_auto_heal_setting('item_ids.bandage_id', '0x0E21')
        self.BANDAGE_ID = int(bandage_id_str, 16) if isinstance(bandage_id_str, str) else bandage_id_str
        
        heal_potion_id_str = self.config_manager.get_auto_heal_setting('item_ids.heal_potion_id', '0x0F0C')
        self.HEAL_POTION_ID = int(heal_potion_id_str, 16) if isinstance(heal_potion_id_str, str) else heal_potion_id_str
        
        # Timer names (constants)
        self.HEALING_TIMER = "HEALING"
        
        # Timing settings from configs
        self.HEALING_TIMER_DURATION = self.config_manager.get_auto_heal_setting('timing_settings.healing_timer_duration_ms', 11000)
        self.HEALING_CHECK_INTERVAL = self.config_manager.get_auto_heal_setting('timing_settings.healing_check_interval', 1)
        self.POTION_COOLDOWN_MS = self.config_manager.get_auto_heal_setting('timing_settings.potion_cooldown_ms', 10000)
        self.BANDAGE_RETRY_DELAY = self.config_manager.get_auto_heal_setting('timing_settings.bandage_retry_delay_ms', 500)
        
        # Global timing settings
        self.DEFAULT_SCRIPT_DELAY = self.config_manager.get_main_setting('global_settings.main_loop_delay_ms', 250)
        self.TARGET_WAIT_TIMEOUT = self.config_manager.get_main_setting('global_settings.target_wait_timeout_ms', 1000)
        self.ERROR_RECOVERY_DELAY = self.config_manager.get_main_setting('global_settings.error_recovery_delay_ms', 1000)
        self.WAITING_DELAY = 1000  # Static constant
        
        # Resource management settings
        self.SEARCH_RANGE = self.config_manager.get_auto_heal_setting('resource_management.search_range', 2)
        self.BANDAGE_RETRY_ATTEMPTS = self.config_manager.get_auto_heal_setting('resource_management.bandage_retry_attempts', 3)
        self.LOW_BANDAGE_WARNING = self.config_manager.get_auto_heal_setting('resource_management.low_bandage_warning', 10)
        self.BANDAGE_CHECK_INTERVAL_CYCLES = self.config_manager.get_auto_heal_setting('resource_management.bandage_check_interval_cycles', 120)
        
        # Health thresholds
        self.BANDAGE_THRESHOLD = self.config_manager.get_auto_heal_setting('health_thresholds.bandage_threshold_hp', 1)
        self.HEALING_THRESHOLD_PERCENTAGE = self.config_manager.get_auto_heal_setting('health_thresholds.healing_threshold_percentage', 95)
        self.CRITICAL_HEALTH_THRESHOLD = self.config_manager.get_auto_heal_setting('health_thresholds.critical_health_threshold', 50)
        
        # Journal monitoring settings
        self.HEALING_SUCCESS_MSG = self.config_manager.get_auto_heal_setting('journal_monitoring.healing_success_msg', "You finish applying the bandages.")
        self.HEALING_PARTIAL_MSG = self.config_manager.get_auto_heal_setting('journal_monitoring.healing_partial_msg', "You apply the bandages, but they barely help.")
        self.JOURNAL_MESSAGE_TYPE = self.config_manager.get_auto_heal_setting('journal_monitoring.journal_message_type', "System")
        
        # GUMP settings
        self.GUMP_ID = 12345  # Static constant
        self.GUMP_UPDATE_INTERVAL_CYCLES = self.config_manager.get_main_setting('gump_interface.main_gump.update_interval_cycles', 8)
        self.GUMP_WIDTH = self.config_manager.get_main_setting('gump_interface.main_gump.width', 320)
        self.GUMP_HEIGHT = self.config_manager.get_main_setting('gump_interface.main_gump.height', 240)
        self.GUMP_X = self.config_manager.get_main_setting('gump_interface.main_gump.x_position', 100)
        self.GUMP_Y = self.config_manager.get_main_setting('gump_interface.main_gump.y_position', 100)
        self.GUMP_MIN_WIDTH = self.config_manager.get_main_setting('gump_interface.minimized_gump.width', 100)
        self.GUMP_MIN_HEIGHT = self.config_manager.get_main_setting('gump_interface.minimized_gump.height', 30)
        
        # Color thresholds
        self.BANDAGE_HIGH_THRESHOLD = self.config_manager.get_auto_heal_setting('color_thresholds.bandage_high_threshold', 20)
        self.BANDAGE_MEDIUM_THRESHOLD = self.config_manager.get_auto_heal_setting('color_thresholds.bandage_medium_threshold', 10)
        self.POTION_HIGH_THRESHOLD = self.config_manager.get_auto_heal_setting('color_thresholds.potion_high_threshold', 10)
        self.POTION_MEDIUM_THRESHOLD = self.config_manager.get_auto_heal_setting('color_thresholds.potion_medium_threshold', 5)
        self.HEALTH_HIGH_THRESHOLD = self.config_manager.get_auto_heal_setting('color_thresholds.health_high_threshold', 75)
        self.HEALTH_MEDIUM_THRESHOLD = self.config_manager.get_auto_heal_setting('color_thresholds.health_medium_threshold', 50)
        
        # Button Icons - Static constants (these don't need to be configurable)
        self.BUTTON_ENABLED = 4017
        self.BUTTON_ENABLED_PRESSED = 4019
        self.BUTTON_DISABLE = 4005
        self.BUTTON_DISABLE_PRESSED = 4007
        self.BUTTON_CANCEL = 4020
        self.BUTTON_CANCEL_PRESSED = 4022
        self.BUTTON_MINIMIZE_NORMAL = 5004
        self.BUTTON_MINIMIZE_PRESSED = 5005
        self.BUTTON_MAXIMIZE_NORMAL = 4011
        self.BUTTON_MAXIMIZE_PRESSED = 4013
        self.BUTTON_DEBUG_ENABLED = 4026
        self.BUTTON_DEBUG_ENABLED_PRESSED = 4028
        self.BUTTON_DEBUG_DISABLED = 4002
        self.BUTTON_DEBUG_DISABLED_PRESSED = 4004
        self.BUTTON_SETTINGS = 4014
        self.BUTTON_SETTINGS_PRESSED = 4016
        self.BUTTON_BACK = 4001
        self.BUTTON_BACK_PRESSED = 4003
    
    def save_settings(self) -> bool:
        """Save current settings back to configuration files"""
        try:
            # Update main config values
            self.config_manager.set_main_setting('system_toggles.healing_system_enabled', self.HEALING_ENABLED)
            self.config_manager.set_main_setting('system_toggles.combat_system_enabled', self.COMBAT_ENABLED)
            self.config_manager.set_main_setting('global_settings.debug_mode', self.DEBUG_MODE)
            
            # Update auto heal config values
            self.config_manager.set_auto_heal_setting('healing_toggles.bandage_healing_enabled', self.BANDAGE_HEALING_ENABLED)
            self.config_manager.set_auto_heal_setting('healing_toggles.potion_healing_enabled', self.POTION_HEALING_ENABLED)
            
            # Save all configs
            return self.config_manager.save_all_configs()
            
        except Exception as e:
            print(f"[BotConfig] Error saving settings: {e}")
            return False
    
    def reload_settings(self) -> None:
        """Reload settings from configuration files"""
        self.config_manager.reload_configs()
        self._load_settings()

class BotMessages:
    """Centralized message constants for consistent logging
    
    This class manages all user-facing messages using the Singleton pattern
    to ensure consistent messaging across the application.
    """
    _instance: Optional['BotMessages'] = None
    
    def __new__(cls) -> 'BotMessages':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
    
    # System status messages
    STARTING = "[DexBot] Bot system starting..."
    ACTIVE = "[DexBot] Bot active - Press ESC to stop"
    STOPPED = "[DexBot] Bot system stopped"
    WAITING_FOR_RESURRECTION = "[DexBot] Player is dead - waiting for resurrection..."
    PLAYER_RESURRECTED = "[DexBot] Player resurrected - resuming bot functions"
    DISCONNECTED = "[DexBot] Player disconnected - stopping script"
    HEALING_DISABLED = "[DexBot] Auto Heal system is disabled"
    HEALING_ENABLED = "[DexBot] Auto Heal system is enabled"
    BANDAGE_HEALING_DISABLED = "[DexBot] Bandage healing is disabled"
    BANDAGE_HEALING_ENABLED = "[DexBot] Bandage healing is enabled"
    POTION_HEALING_DISABLED = "[DexBot] Potion healing is disabled" 
    POTION_HEALING_ENABLED = "[DexBot] Potion healing is enabled"
    
    # Action messages
    BANDAGE_APPLIED = "[DexBot] Applied bandage successfully"
    BANDAGE_APPLYING = "[DexBot] Applying bandage to self"
    HEAL_POTION_USED = "[DexBot] Used heal potion (critical health)"
    
    # Error messages
    NO_BANDAGES = "[DexBot] No bandages found in backpack"
    NO_HEAL_RESOURCES = "[DexBot] No healing resources (bandages or potions) found"
    LOW_BANDAGES = "[DexBot] WARNING: Low bandage supply! ({} remaining)"
    MAIN_LOOP_ERROR = "[DexBot] Error in main loop: {}"
    BANDAGE_ERROR = "[DexBot] Error applying bandage: {}"
    HEAL_POTION_ERROR = "[DexBot] Error using heal potion: {}"
    
    # GUMP interface messages
    GUMP_TITLE = "DexBot Control Panel"
    GUMP_STATUS_ONLINE = "ONLINE"
    GUMP_STATUS_OFFLINE = "OFFLINE"
    GUMP_HEALING_ACTIVE = "ACTIVE"
    GUMP_HEALING_INACTIVE = "INACTIVE"

# ===========================================
# LOGGING AND STATUS SYSTEM
# ===========================================

class Logger:
    """Simple logging system with different levels
    
    Provides standardized logging functionality with debug, info, error, and warning levels.
    Debug messages are only shown when DEBUG_MODE is enabled.
    """
    
    @staticmethod
    def debug(message: str) -> None:
        """Log debug message (only shown when DEBUG_MODE is enabled)"""
        if BotConfig().DEBUG_MODE:
            print(f"[DEBUG] {message}")
    
    @staticmethod
    def info(message: str) -> None:
        """Log informational message"""
        print(message)
    
    @staticmethod
    def error(message: str) -> None:
        """Log error message"""
        print(f"[ERROR] {message}")
    
    @staticmethod
    def warning(message: str) -> None:
        """Log warning message"""
        print(f"[WARNING] {message}")

class SystemStatus:
    """Track system status and statistics
    
    Singleton class that maintains runtime statistics and status information
    for all bot systems including healing, GUMP state, and performance metrics.
    """
    _instance: Optional['SystemStatus'] = None
    
    def __new__(cls) -> 'SystemStatus':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize all instance variables
            cls._instance.healing_active = False
            cls._instance.bandage_count = 0
            cls._instance.heal_potion_count = 0  # Track heal potions used
            cls._instance.bandage_check_counter = 0
            cls._instance.gump_update_counter = 0
            cls._instance.runtime_cycles = 0  # Track runtime in loop cycles
            cls._instance.gump_closed = False  # Track if GUMP was manually closed
            cls._instance.gump_minimized = False  # Track if GUMP is minimized
            cls._instance.last_health = 0  # Track health changes for real-time updates
            cls._instance.health_change_threshold = 5  # Update GUMP if health changes by this amount
            # Track last displayed values to avoid unnecessary updates
            cls._instance.last_displayed_health = 0
            cls._instance.last_displayed_max_health = 0
            cls._instance.last_displayed_bandages = 0
            cls._instance.last_displayed_runtime = 0
            cls._instance.last_displayed_healing_enabled = None
            cls._instance.last_displayed_debug_enabled = None
            cls._instance.last_displayed_bandage_healing_enabled = None
            cls._instance.last_displayed_potion_healing_enabled = None
            cls._instance.last_displayed_bandages_used = 0
            cls._instance.last_displayed_heal_potions_used = 0
            cls._instance.last_button_press_time = 0  # Prevent rapid button presses
            cls._instance.current_gump_state = GumpState.CLOSED  # Track which GUMP should be visible
        return cls._instance
    
    def increment_bandage_count(self) -> None:
        """Increment bandage usage counter"""
        self.bandage_count += 1
    
    def increment_heal_potion_count(self) -> None:
        """Increment heal potion usage counter"""
        self.heal_potion_count += 1
    
    def get_status_report(self) -> Dict[str, Union[str, int]]:
        """Get comprehensive status report"""
        return {
            'healing': 'Active' if self.healing_active else 'Inactive',
            'bandages_used': self.bandage_count,
            'heal_potions_used': self.heal_potion_count
        }
    
    def set_gump_state(self, state: str) -> None:
        """Set the current GUMP state"""
        self.current_gump_state = state
        Logger.debug(f"GUMP state changed to: {state}")
    
    def get_gump_state(self) -> str:
        """Get the current GUMP state"""
        return self.current_gump_state
    
    def is_gump_visible(self) -> bool:
        """Check if any GUMP should be visible"""
        return self.current_gump_state != GumpState.CLOSED
    
    def get_runtime_minutes(self) -> int:
        """Get runtime in minutes (estimated from cycles)"""
        # Each cycle is approximately 250ms (DEFAULT_SCRIPT_DELAY)
        # So runtime_cycles * 250ms / 60000ms = minutes
        estimated_minutes = (self.runtime_cycles * 250) // 60000
        return max(0, estimated_minutes)  # Ensure non-negative
    
    def increment_runtime(self) -> None:
        """Increment runtime cycle counter"""
        self.runtime_cycles += 1
    
    def check_health_change(self) -> bool:
        """Check if health has changed significantly to trigger GUMP update"""
        current_health = Player.Hits
        health_changed = abs(current_health - self.last_health) >= self.health_change_threshold
        self.last_health = current_health
        return health_changed
    
    def check_gump_data_changed(self) -> bool:
        """Check if any data displayed in the gump has changed"""
        config = BotConfig()
        
        # Get current values
        current_health = Player.Hits
        current_max_health = Player.HitsMax
        bandage_count = Items.FindByID(config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
        current_bandages = bandage_count.Amount if bandage_count else 0
        current_runtime = self.get_runtime_minutes()
        current_healing_enabled = config.HEALING_ENABLED
        current_debug_enabled = config.DEBUG_MODE
        current_bandage_healing_enabled = config.BANDAGE_HEALING_ENABLED
        current_potion_healing_enabled = config.POTION_HEALING_ENABLED
        current_bandages_used = self.bandage_count
        current_heal_potions_used = self.heal_potion_count
        
        # Check if any values have changed
        data_changed = (
            current_health != self.last_displayed_health or
            current_max_health != self.last_displayed_max_health or
            current_bandages != self.last_displayed_bandages or
            current_runtime != self.last_displayed_runtime or
            current_healing_enabled != self.last_displayed_healing_enabled or
            current_debug_enabled != self.last_displayed_debug_enabled or
            current_bandage_healing_enabled != self.last_displayed_bandage_healing_enabled or
            current_potion_healing_enabled != self.last_displayed_potion_healing_enabled or
            current_bandages_used != self.last_displayed_bandages_used or
            current_heal_potions_used != self.last_displayed_heal_potions_used
        )
        
        # Update last displayed values if data changed
        if data_changed:
            self.last_displayed_health = current_health
            self.last_displayed_max_health = current_max_health
            self.last_displayed_bandages = current_bandages
            self.last_displayed_runtime = current_runtime
            self.last_displayed_healing_enabled = current_healing_enabled
            self.last_displayed_debug_enabled = current_debug_enabled
            self.last_displayed_bandage_healing_enabled = current_bandage_healing_enabled
            self.last_displayed_potion_healing_enabled = current_potion_healing_enabled
            self.last_displayed_bandages_used = current_bandages_used
            self.last_displayed_heal_potions_used = current_heal_potions_used
        
        return data_changed

# ===========================================
# UTILITY FUNCTIONS
# ===========================================

def get_resource_color(amount: int, high_threshold: int, medium_threshold: int) -> str:
    """Get color code based on resource amount and thresholds
    
    Args:
        amount: Current resource amount
        high_threshold: Threshold for green color
        medium_threshold: Threshold for yellow color
        
    Returns:
        Color code string (green, yellow, or red)
    """
    if amount > high_threshold:
        return "#00FF00"  # Green
    elif amount > medium_threshold:
        return "#FFFF00"  # Yellow
    else:
        return "#FF6B6B"  # Red

def check_bandage_supply(log_errors: bool = True) -> int:
    """Check bandage supply and warn if low
    
    Args:
        log_errors: Whether to log error messages for missing bandages
    
    Returns:
        Number of bandages found in backpack
    """
    config = BotConfig()
    messages = BotMessages()
    
    bandages = Items.FindByID(config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
    if bandages:
        if bandages.Amount <= config.LOW_BANDAGE_WARNING and log_errors:
            Logger.warning(messages.LOW_BANDAGES.format(bandages.Amount))
        return bandages.Amount
    else:
        if log_errors:
            Logger.error(messages.NO_BANDAGES)
        return 0

def has_healing_resources() -> Tuple[bool, bool]:
    """Check if player has healing resources available
    
    Returns:
        Tuple of (has_bandages, has_heal_potions)
    """
    config = BotConfig()
    has_bandages = bool(Items.FindByID(config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE))
    has_heal_potions = bool(Items.FindByID(config.HEAL_POTION_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE))
    return has_bandages, has_heal_potions

# ===========================================
# AUTO HEAL SYSTEM (Based on Dexxor.py)
# ===========================================

def process_healing_journal():
    """
    Process journal for healing completion messages.
    Part of the Auto Heal system - based on Dexxor.py healing system with enhanced logging.
    """
    config = BotConfig()
    messages = BotMessages()
    status = SystemStatus()
    
    # Check if Auto Heal is enabled
    if not config.HEALING_ENABLED:
        return
    
    if Timer.Check(config.HEALING_TIMER):
        if Journal.SearchByType(config.HEALING_SUCCESS_MSG, config.JOURNAL_MESSAGE_TYPE):
            Timer.Create(config.HEALING_TIMER, config.HEALING_CHECK_INTERVAL)
            Logger.info(messages.BANDAGE_APPLIED)
            status.increment_bandage_count()
            status.healing_active = False  # Reset healing status when bandaging completes
        elif Journal.SearchByType(config.HEALING_PARTIAL_MSG, config.JOURNAL_MESSAGE_TYPE):
            Timer.Create(config.HEALING_TIMER, config.HEALING_CHECK_INTERVAL)
            Logger.info(messages.BANDAGE_APPLIED)
            status.increment_bandage_count()
            status.healing_active = False  # Reset healing status when bandaging completes
    
    Journal.Clear()

def execute_auto_heal_system():
    """
    Execute the Auto Heal system - intelligently use bandages and heal potions based on health status.
    Enhanced with better resource checking, error handling, and individual healing method toggles.
    
    The system respects BANDAGE_HEALING_ENABLED and POTION_HEALING_ENABLED configuration options,
    allowing users to enable/disable healing methods independently via the GUMP interface.
    """
    config = BotConfig()
    messages = BotMessages()
    status = SystemStatus()
    
    # Check if Auto Heal is enabled
    if not config.HEALING_ENABLED:
        return False
    
    # Safety checks
    if Player.IsGhost or not Player.Visible:
        Logger.debug("Player is ghost or invisible - skipping Auto Heal")
        return False
    
    # Check if healing is on cooldown
    if Timer.Check(config.HEALING_TIMER):
        Logger.debug("Auto Heal on cooldown - skipping")
        return False

    # Periodic bandage supply check (every 120 loop cycles ~ 30 seconds)
    # Only check bandage supply if bandage healing is enabled
    if config.BANDAGE_HEALING_ENABLED:
        status.bandage_check_counter += 1
        if status.bandage_check_counter >= config.BANDAGE_CHECK_INTERVAL_CYCLES:
            bandage_count = check_bandage_supply()
            status.bandage_check_counter = 0
            if bandage_count == 0:
                return False

    # Determine if healing is needed
    health_missing = Player.HitsMax - Player.Hits
    health_percentage = (Player.Hits / Player.HitsMax) * 100
    needs_healing = (health_missing > config.BANDAGE_THRESHOLD or 
                    Player.Poisoned or 
                    health_percentage < config.HEALING_THRESHOLD_PERCENTAGE)
    
    if needs_healing:
        Logger.debug(f"Auto Heal needed - Health: {Player.Hits}/{Player.HitsMax} ({health_percentage:.1f}%)")
        
        # Check for available healing resources
        has_bandages, has_heal_potions = has_healing_resources()
        
        # Apply enable/disable filters for healing methods
        can_use_bandages = has_bandages and config.BANDAGE_HEALING_ENABLED
        can_use_potions = has_heal_potions and config.POTION_HEALING_ENABLED
        
        # If no enabled healing resources available, log error and return
        if not can_use_bandages and not can_use_potions:
            if not has_bandages and not has_heal_potions:
                Logger.error(messages.NO_HEAL_RESOURCES)
            else:
                # Provide specific info about what's disabled
                disabled_methods = []
                if has_bandages and not config.BANDAGE_HEALING_ENABLED:
                    disabled_methods.append("bandages")
                if has_heal_potions and not config.POTION_HEALING_ENABLED:
                    disabled_methods.append("potions")
                Logger.debug(f"Healing needed but disabled methods: {', '.join(disabled_methods)}")
            return False
        
        # Prioritize heal potions for faster healing when health is very low
        if health_percentage < config.CRITICAL_HEALTH_THRESHOLD and can_use_potions:
            # Use heal potion for critical health
            try:
                Items.UseItemByID(config.HEAL_POTION_ID, -1)
                Logger.info(messages.HEAL_POTION_USED)
                status.increment_heal_potion_count()
                status.healing_active = True
                # Short cooldown for potion use
                Timer.Create(config.HEALING_TIMER, config.POTION_COOLDOWN_MS)
                return True
            except Exception as e:
                Logger.error(messages.HEAL_POTION_ERROR.format(str(e)))
        
        # Use bandages for normal healing
        if can_use_bandages:
            # Retry mechanism for bandage application
            for attempt in range(config.BANDAGE_RETRY_ATTEMPTS):
                try:
                    # Apply bandage
                    Items.UseItemByID(config.BANDAGE_ID, -1)
                    Target.WaitForTarget(config.TARGET_WAIT_TIMEOUT)
                    Target.Self()
                    
                    # Use standard timer duration
                    Timer.Create(config.HEALING_TIMER, config.HEALING_TIMER_DURATION)
                    
                    Logger.info(messages.BANDAGE_APPLYING)
                    status.healing_active = True
                    return True
                    
                except Exception as e:
                    Logger.error(messages.BANDAGE_ERROR.format(str(e)))
                    if attempt < config.BANDAGE_RETRY_ATTEMPTS - 1:
                        Logger.debug(f"Retrying bandage application (attempt {attempt + 2})")
                        Misc.Pause(config.BANDAGE_RETRY_PAUSE_MS)
                    else:
                        status.healing_active = False
                        return False
        elif config.BANDAGE_HEALING_ENABLED:
            # Only show "no bandages" error if bandage healing is enabled
            Logger.error(messages.NO_BANDAGES)
            return False
    
    status.healing_active = False
    return False

# ===========================================
# GUMP INTERFACE SYSTEM
# ===========================================

class GumpInterface:
    """In-game GUMP interface for bot control and status display"""
    
    class GumpSection:
        """Reusable component for creating consistent UI sections in the gump"""
        
        @staticmethod
        def create_section(gd, title, x, y, width, content_lines=None, title_color="#87CEEB", content_indent="2em", 
                          toggle_button=None):
            """
            Create a standardized section with title and content, optionally with a toggle button
            
            Args:
                gd: Gump definition object
                title: Section title text
                x, y: Position coordinates
                width: Section width
                content_lines: List of content line dictionaries with 'text' and optional 'color'
                title_color: Color for the section title
                content_indent: CSS margin-left value for content indentation
                toggle_button: Optional dict with button config: {
                    'enabled': bool,
                    'button_id': int,
                    'enabled_art': int,
                    'enabled_pressed_art': int,
                    'disabled_art': int,
                    'disabled_pressed_art': int,
                    'tooltip': str
                }
            
            Returns:
                The Y position after this section (for positioning next elements)
            """
            current_y = y
            section_start_x = x
            
            # If toggle button is provided, add it to the left of the section
            if toggle_button:
                button_x = x - 45  # Position button to the left with margin
                button_y = current_y + 2  # Align with section title
                
                # Choose button art based on enabled state
                if toggle_button['enabled']:
                    button_art = toggle_button['enabled_art']
                    button_pressed_art = toggle_button['enabled_pressed_art']
                else:
                    button_art = toggle_button['disabled_art']
                    button_pressed_art = toggle_button['disabled_pressed_art']
                
                # Add the toggle button
                Gumps.AddButton(gd, button_x, button_y, button_art, button_pressed_art, 
                               toggle_button['button_id'], 1, 0)
                
                # Add tooltip if provided
                if 'tooltip' in toggle_button:
                    Gumps.AddTooltip(gd, toggle_button['tooltip'])
            
            # Add section title (centered)
            title_html = f'<center><basefont color="{title_color}" size="3"><b>{title}</b></basefont></center>'
            Gumps.AddHtml(gd, section_start_x, current_y, width, 20, title_html, False, False)
            current_y += 20
            
            # Add content lines if provided
            if content_lines:
                for line in content_lines:
                    line_text = line.get('text', '')
                    line_color = line.get('color', '#FFFFFF')
                    
                    # Apply indentation using div with margin-left
                    content_html = f'<div style="margin-left: {content_indent};"><basefont color="{line_color}" size="2">{line_text}</basefont></div>'
                    Gumps.AddHtml(gd, section_start_x, current_y, width, 20, content_html, False, False)
                    current_y += 20
            
            return current_y
        
        @staticmethod
        def create_player_status_section(gd, x, y, width):
            """Create the player status section using the standardized format"""
            config = BotConfig()
            health_percentage = (Player.Hits / Player.HitsMax) * 100 if Player.HitsMax > 0 else 0
            health_color = get_resource_color(
                int(health_percentage), 
                config.HEALTH_HIGH_THRESHOLD, 
                config.HEALTH_MEDIUM_THRESHOLD
            )
            
            # Create content lines for player status
            content_lines = [
                {
                    'text': f'HP: <basefont color="{health_color}" size="3"><b>{Player.Hits}/{Player.HitsMax}</b></basefont> <basefont color="#CCCCCC" size="2">({health_percentage:.0f}%)</basefont>',
                    'color': '#FFFFFF'
                }
            ]
            
            return GumpInterface.GumpSection.create_section(
                gd, "PLAYER STATUS", x, y, width, content_lines
            )
        
        @staticmethod
        def create_auto_heal_status_section(gd, x, y, width):
            """Create an Auto Heal section with integrated toggle controls for all healing options"""
            config = BotConfig()
            messages = BotMessages()
            status = SystemStatus()
            
            current_y = y
            
            # Main Auto Heal toggle button (left side)
            main_toggle_x = x - 45
            main_toggle_y = current_y + 2
            
            # Choose button art based on enabled state
            if config.HEALING_ENABLED:
                main_toggle_art = config.BUTTON_ENABLED
                main_toggle_pressed_art = config.BUTTON_ENABLED_PRESSED
                heal_status_text = f'<basefont color="#00FF00" size="3"><b>AUTO HEAL</b></basefont>'
                status_text = f'{"Healing..." if status.healing_active else "Ready"}'
                status_color = "#FFFF00" if status.healing_active else "#00FF00"
            else:
                main_toggle_art = config.BUTTON_DISABLE
                main_toggle_pressed_art = config.BUTTON_DISABLE_PRESSED
                heal_status_text = f'<basefont color="#FF0000" size="3"><b>AUTO HEAL</b></basefont>'
                status_text = "Disabled"
                status_color = "#FF0000"
            
            # Add main enable/disable toggle button
            Gumps.AddButton(gd, main_toggle_x, main_toggle_y, main_toggle_art, main_toggle_pressed_art, 1, 1, 0)
            Gumps.AddTooltip(gd, f"Toggle Auto Heal System ({'ON' if config.HEALING_ENABLED else 'OFF'})")
            
            # Get resource counts for display
            bandage_count = Items.FindByID(config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
            bandage_amount = bandage_count.Amount if bandage_count else 0
            heal_potion_count = Items.FindByID(config.HEAL_POTION_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
            heal_potion_amount = heal_potion_count.Amount if heal_potion_count else 0
            
            # First line: Main status and resource counts
            main_status_line = f'{heal_status_text} - <basefont color="{status_color}" size="2"><b>{status_text}</b></basefont> | ' \
                             f'<basefont color="#CCCCCC" size="2">B:</basefont><basefont color="#FFFFFF" size="2"><b>{bandage_amount}</b></basefont> ' \
                             f'<basefont color="#CCCCCC" size="2">P:</basefont><basefont color="#FFFFFF" size="2"><b>{heal_potion_amount}</b></basefont> | ' \
                             f'<basefont color="#CCCCCC" size="2">Used: </basefont><basefont color="#FFFFFF" size="2"><b>{status.bandage_count}/{status.heal_potion_count}</b></basefont>'
            
            # Add the main status line
            Gumps.AddHtml(gd, x, current_y, width, 20, main_status_line, False, False)
            current_y += 22
            
            # Second line: Individual healing method toggles
            # Bandage healing toggle
            bandage_toggle_x = x
            bandage_toggle_y = current_y + 2
            if config.BANDAGE_HEALING_ENABLED:
                bandage_art = config.BUTTON_ENABLED
                bandage_pressed_art = config.BUTTON_ENABLED_PRESSED
                bandage_status = "ON"
                bandage_color = "#00FF00"
            else:
                bandage_art = config.BUTTON_DISABLE
                bandage_pressed_art = config.BUTTON_DISABLE_PRESSED
                bandage_status = "OFF"
                bandage_color = "#FF0000"
                
            Gumps.AddButton(gd, bandage_toggle_x, bandage_toggle_y, bandage_art, bandage_pressed_art, 7, 1, 0)  # Button ID 7 for bandages
            Gumps.AddTooltip(gd, f"Toggle Bandage Healing ({'ON' if config.BANDAGE_HEALING_ENABLED else 'OFF'})")
            
            # Potion healing toggle
            potion_toggle_x = x + 120
            potion_toggle_y = current_y + 2
            if config.POTION_HEALING_ENABLED:
                potion_art = config.BUTTON_ENABLED
                potion_pressed_art = config.BUTTON_ENABLED_PRESSED
                potion_status = "ON"
                potion_color = "#00FF00"
            else:
                potion_art = config.BUTTON_DISABLE
                potion_pressed_art = config.BUTTON_DISABLE_PRESSED
                potion_status = "OFF"
                potion_color = "#FF0000"
                
            Gumps.AddButton(gd, potion_toggle_x, potion_toggle_y, potion_art, potion_pressed_art, 8, 1, 0)  # Button ID 8 for potions
            Gumps.AddTooltip(gd, f"Toggle Potion Healing ({'ON' if config.POTION_HEALING_ENABLED else 'OFF'})")
            
            # Labels for the toggle buttons
            toggle_labels = f'<basefont color="#CCCCCC" size="2">Bandages: </basefont><basefont color="{bandage_color}" size="2"><b>{bandage_status}</b></basefont>' \
                          f'     <basefont color="#CCCCCC" size="2">Potions: </basefont><basefont color="{potion_color}" size="2"><b>{potion_status}</b></basefont>'
            
            Gumps.AddHtml(gd, x + 25, current_y + 4, width - 25, 15, toggle_labels, False, False)
            
            return current_y + 25  # Return Y position after both lines
        
        @staticmethod
        def create_system_summary_line(gd, x, y, width, system_name, enabled, active, status_text, 
                                     enable_button_id, settings_button_id):
            """
            Create a single-line system summary with toggle, name, status, and settings button
            
            Args:
                gd: Gump definition object
                x, y: Position coordinates
                width: Line width
                system_name: Display name of the system (e.g., "AUTO HEAL")
                enabled: Whether the system is enabled
                active: Whether the system is currently active/working
                status_text: Status description (e.g., "Ready", "Healing...", "Disabled")
                enable_button_id: Button ID for enable/disable toggle
                settings_button_id: Button ID for opening settings GUMP
            
            Returns:
                The Y position after this line (for positioning next elements)
            """
            config = BotConfig()
            current_y = y
            
            # Enable/Disable toggle button (left side)
            toggle_x = x - 40
            toggle_y = current_y + 2
            
            if enabled:
                toggle_art = config.BUTTON_ENABLED
                toggle_pressed_art = config.BUTTON_ENABLED_PRESSED
                system_color = "#00FF00" if active else "#FFFF00"
                toggle_tooltip = f"Disable {system_name}"
            else:
                toggle_art = config.BUTTON_DISABLE
                toggle_pressed_art = config.BUTTON_DISABLE_PRESSED
                system_color = "#FF0000"
                toggle_tooltip = f"Enable {system_name}"
            
            Gumps.AddButton(gd, toggle_x, toggle_y, toggle_art, toggle_pressed_art, enable_button_id, 1, 0)
            Gumps.AddTooltip(gd, toggle_tooltip)
            
            # Settings button (right side)
            settings_x = x + width - 25
            settings_y = current_y + 2
            Gumps.AddButton(gd, settings_x, settings_y, config.BUTTON_SETTINGS, config.BUTTON_SETTINGS_PRESSED, settings_button_id, 1, 0)
            Gumps.AddTooltip(gd, f"Open {system_name} Settings")
            
            # System summary line
            if enabled and active:
                status_display = f'<basefont color="#FFFF00" size="2"><b>{status_text}</b></basefont>'
            elif enabled:
                status_display = f'<basefont color="#00FF00" size="2"><b>{status_text}</b></basefont>'
            else:
                status_display = f'<basefont color="#888888" size="2"><b>Disabled</b></basefont>'
            
            summary_line = f'<basefont color="{system_color}" size="3"><b>{system_name}</b></basefont> - {status_display}'
            
            # Add the summary line (with space for buttons on both sides)
            line_x = x + 5  # Small margin from toggle button
            line_width = width - 35  # Leave space for settings button
            Gumps.AddHtml(gd, line_x, current_y, line_width, 20, summary_line, False, False)
            
            return current_y + 25  # Return Y position after this line
    
    @staticmethod
    def create_status_gump():
        """Create and display the appropriate GUMP based on current state"""
        config = BotConfig()
        messages = BotMessages()
        status = SystemStatus()
        
        try:
            # Close any existing GUMP to ensure clean state
            Gumps.CloseGump(config.GUMP_ID)
            
            # Determine which GUMP to create based on current state
            current_state = status.get_gump_state()
            
            if current_state == GumpState.CLOSED:
                # Don't create any GUMP
                return
            elif current_state == GumpState.MAIN_MINIMIZED or status.gump_minimized:
                GumpInterface.create_minimized_gump()
                status.set_gump_state(GumpState.MAIN_MINIMIZED)
            elif current_state == GumpState.AUTO_HEAL_SETTINGS:
                GumpInterface.create_auto_heal_settings_gump()
            elif current_state == GumpState.COMBAT_SETTINGS:
                # TODO: Implement Combat Settings GUMP
                Logger.info("[DexBot] Combat Settings GUMP not implemented yet, returning to main")
                status.set_gump_state(GumpState.MAIN_FULL)
                GumpInterface.create_main_gump_new()
            elif current_state == GumpState.LOOTING_SETTINGS:
                # TODO: Implement Looting Settings GUMP
                Logger.info("[DexBot] Looting Settings GUMP not implemented yet, returning to main")
                status.set_gump_state(GumpState.MAIN_FULL)
                GumpInterface.create_main_gump_new()
            else:
                # Default to main GUMP (MAIN_FULL or unknown state)
                GumpInterface.create_main_gump_new()
                status.set_gump_state(GumpState.MAIN_FULL)
                
        except Exception as e:
            Logger.error(f"Error creating GUMP: {str(e)}")
    
    @staticmethod
    def create_full_gump():
        """Create the full-size status GUMP"""
        config = BotConfig()
        messages = BotMessages()
        status = SystemStatus()
        
        # Get current status information
        health_percentage = (Player.Hits / Player.HitsMax) * 100 if Player.HitsMax > 0 else 0
        bandage_count = Items.FindByID(config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
        bandage_amount = bandage_count.Amount if bandage_count else 0
        runtime_minutes = status.get_runtime_minutes()
        
        # Create GUMP using proper Razor Enhanced pattern
        gd = Gumps.CreateGump(movable=True)
        Gumps.AddPage(gd, 0)
        
        # Background
        Gumps.AddBackground(gd, 0, 0, config.GUMP_WIDTH, config.GUMP_HEIGHT, 30546)
        Gumps.AddAlphaRegion(gd, 0, 0, config.GUMP_WIDTH, config.GUMP_HEIGHT)
        
        # Add title at the top center of the gump
        Gumps.AddHtml(gd, 70, 5, config.GUMP_WIDTH - 20, 25, f'<center><basefont color="#FFD700" size="5"><b>{messages.GUMP_TITLE}</b></basefont></center>', False, False)
        
        # Window control buttons in upper right corner (like standard dialog windows)
        # Close Button - positioned in upper right corner
        close_button_x = config.GUMP_WIDTH - 40  # Moved further left for better spacing
        close_button_y = 5  # Top edge aligned with title
        Gumps.AddButton(gd, close_button_x, close_button_y, config.BUTTON_CANCEL, config.BUTTON_CANCEL_PRESSED, 4, 1, 0)
        Gumps.AddTooltip(gd, "Close Interface")
        
        # Minimize Button - positioned to the left of close button with more spacing
        minimize_button_x = config.GUMP_WIDTH - 70  # Increased spacing between buttons
        minimize_button_y = 5  # Same Y as close button
        Gumps.AddButton(gd, minimize_button_x, minimize_button_y, config.BUTTON_MINIMIZE_NORMAL, config.BUTTON_MINIMIZE_PRESSED, 3, 1, 0)
        Gumps.AddTooltip(gd, "Minimize Interface")
        
        # Add online status just below the title
        Gumps.AddHtml(gd, 80, 30, config.GUMP_WIDTH - 20, 20, f'<center><basefont color="#00FF00" size="3"><b>● {messages.GUMP_STATUS_ONLINE}</b></basefont> <basefont color="#CCCCCC" size="2">| Runtime: </basefont><basefont color="#FFFFFF" size="3"><b>{runtime_minutes}m</b></basefont></center>', False, False)
        
        # Use reusable section components for consistent UI
        # Reserve space for section toggle buttons (40px width + 5px margin)
        button_space = 45
        section_x = 25 + button_space  # Indent sections to make room for buttons
        section_width = config.GUMP_WIDTH - 50 - button_space
        
        # Player Status Section using reusable component (no button needed)
        current_y = GumpInterface.GumpSection.create_player_status_section(gd, section_x, 65, section_width)
        
        # Add spacing between sections
        current_y += 10
        
        # Auto Heal System Section with integrated toggle button
        current_y = GumpInterface.GumpSection.create_auto_heal_status_section(gd, section_x, current_y, section_width)
        
        # Example: Adding new sections is now easy with the reusable component
        # current_y += 10  # Add spacing
        # current_y = GumpInterface.GumpSection.create_section(
        #     gd, "COMBAT SYSTEM", section_x, current_y, section_width,
        #     content_lines=[
        #         {'text': 'Status: <basefont color="#00FF00" size="3"><b>READY</b></basefont>', 'color': '#FFFFFF'},
        #         {'text': 'Targets: <basefont color="#FFFF00" size="3"><b>3</b></basefont>', 'color': '#FFFFFF'}
        #     ]
        # )
        
        # Compact button layout in bottom area
        
        # Debug Button - positioned in bottom left corner
        debug_button_x = 20  # Left edge with reduced padding
        debug_button_y = config.GUMP_HEIGHT - 35  # Moved up for compact design
        
        if config.DEBUG_MODE:
            Gumps.AddButton(gd, debug_button_x, debug_button_y, config.BUTTON_DEBUG_ENABLED, config.BUTTON_DEBUG_ENABLED_PRESSED, 2, 1, 0)  # Blue button (enabled)
            debug_status = "ON"
            debug_color = "#00BFFF"  # Deep sky blue for enabled debug
        else:
            Gumps.AddButton(gd, debug_button_x, debug_button_y, config.BUTTON_DEBUG_DISABLED, config.BUTTON_DEBUG_DISABLED_PRESSED, 2, 1, 0)  # Gray button (disabled)
            debug_status = "OFF"
            debug_color = "#888888"  # Darker gray for disabled debug
        Gumps.AddTooltip(gd, f"Toggle Debug Mode (Currently {debug_status})")
        
        # Debug button label (bottom left) - smaller font
        debug_labels = f"""
        <basefont color="{debug_color}" size="2"><b>DEBUG</b></basefont><br>
        <basefont color="#CCCCCC" size="1">{debug_status}</basefont>
        """
        Gumps.AddHtml(gd, debug_button_x - 3, debug_button_y + 15, 60, 25, debug_labels, False, False)
        
        # Send the GUMP
        Gumps.SendGump(config.GUMP_ID, Player.Serial, config.GUMP_X, config.GUMP_Y, gd.gumpDefinition, gd.gumpStrings)
        
        Logger.debug("Full status GUMP created and displayed")
    
    @staticmethod
    def create_minimized_gump():
        """Create the minimized status GUMP"""
        config = BotConfig()
        messages = BotMessages()
        status = SystemStatus()
        
        # Create compact GUMP
        gd = Gumps.CreateGump(movable=True)
        Gumps.AddPage(gd, 0)
        
        # Background
        Gumps.AddBackground(gd, 0, 0, config.GUMP_MIN_WIDTH, config.GUMP_MIN_HEIGHT, 30546)
        Gumps.AddAlphaRegion(gd, 0, 0, config.GUMP_MIN_WIDTH, config.GUMP_MIN_HEIGHT)
        
        # Title in upper left corner
        Gumps.AddHtml(gd, 5, 5, 65, 20, f'<basefont color="#FFD700" size="3"><b>DexBot</b></basefont>', False, False)
        
        # Expand button in upper right corner (no text label) - closer to title
        expand_button_x = config.GUMP_MIN_WIDTH - 22  # Closer to edge for tighter spacing
        expand_button_y = 5  # Top edge aligned with title
        Gumps.AddButton(gd, expand_button_x, expand_button_y, config.BUTTON_MAXIMIZE_NORMAL, config.BUTTON_MAXIMIZE_PRESSED, 5, 1, 0)
        Gumps.AddTooltip(gd, "Expand Interface")
        
        # Send the GUMP
        Gumps.SendGump(config.GUMP_ID, Player.Serial, config.GUMP_X, config.GUMP_Y, gd.gumpDefinition, gd.gumpStrings)
        
        Logger.debug("Minimized status GUMP created and displayed")

    @staticmethod
    def handle_gump_response():
        """Handle player interactions with the GUMP"""
        config = BotConfig()
        status = SystemStatus()
        
        # Don't handle GUMP responses if it was manually closed
        if status.gump_closed:
            return False
        
        try:
            # Rate limiting: prevent rapid button presses (minimum 500ms between presses)
            current_time = time.time()
            if current_time - status.last_button_press_time < 0.5:
                return True  # Ignore rapid button presses
            
            # Check if our GUMP has a response
            gd = Gumps.GetGumpData(config.GUMP_ID)
            if gd and gd.buttonid > 0:
                button_pressed = gd.buttonid
                
                # Update last button press time
                status.last_button_press_time = current_time
                
                # Close and recreate the GUMP to clear the button press
                Gumps.CloseGump(config.GUMP_ID)
                
                if button_pressed == 1:  # Toggle Auto Heal (only in full GUMP)
                    config.HEALING_ENABLED = not config.HEALING_ENABLED
                    status_msg = "enabled" if config.HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Auto Heal system {status_msg} via GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()
                    
                elif button_pressed == 2:  # Toggle Debug Mode (only in full GUMP)
                    config.DEBUG_MODE = not config.DEBUG_MODE
                    status_msg = "enabled" if config.DEBUG_MODE else "disabled"
                    Logger.info(f"[DexBot] Debug mode {status_msg} via GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()
                    
                elif button_pressed == 3:  # Minimize GUMP (only in full GUMP)
                    status.gump_minimized = True
                    Logger.info("[DexBot] Status GUMP minimized")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()
                    
                elif button_pressed == 4:  # Close GUMP (only in full GUMP)
                    status.gump_closed = True  # Mark GUMP as closed
                    status.set_gump_state(GumpState.CLOSED)  # Update state
                    Logger.info("[DexBot] Status GUMP closed")
                    return False  # Signal that GUMP was closed
                    
                elif button_pressed == 5:  # Maximize GUMP (only in minimized GUMP)
                    status.gump_minimized = False
                    Logger.info("[DexBot] Status GUMP maximized")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()
                    
                elif button_pressed == 7:  # Toggle Bandage Healing (only in full GUMP)
                    config.BANDAGE_HEALING_ENABLED = not config.BANDAGE_HEALING_ENABLED
                    status_msg = "enabled" if config.BANDAGE_HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Bandage healing {status_msg} via GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()
                    
                elif button_pressed == 8:  # Toggle Potion Healing (only in full GUMP)
                    config.POTION_HEALING_ENABLED = not config.POTION_HEALING_ENABLED
                    status_msg = "enabled" if config.POTION_HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Potion healing {status_msg} via GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()
                
                elif button_pressed == 10:  # Open Auto Heal Settings GUMP
                    Logger.info("[DexBot] Opening Auto Heal Settings")
                    status.set_gump_state(GumpState.AUTO_HEAL_SETTINGS)
                    GumpInterface.create_auto_heal_settings_gump()
                
                elif button_pressed == 11:  # Toggle Combat System (future)
                    Logger.info("[DexBot] Combat System toggle pressed (not implemented)")
                    GumpInterface.create_status_gump()
                
                elif button_pressed == 12:  # Open Combat Settings GUMP (future)
                    Logger.info("[DexBot] Combat Settings pressed (not implemented)")
                    GumpInterface.create_status_gump()
                
                elif button_pressed == 13:  # Toggle Looting System (future)
                    Logger.info("[DexBot] Looting System toggle pressed (not implemented)")
                    GumpInterface.create_status_gump()
                
                elif button_pressed == 14:  # Open Looting Settings GUMP (future)
                    Logger.info("[DexBot] Looting Settings pressed (not implemented)")
                    GumpInterface.create_status_gump()
                
                elif button_pressed == 20:  # Back to Main GUMP (from Auto Heal Settings)
                    Logger.info("[DexBot] Returning to main GUMP")
                    status.set_gump_state(GumpState.MAIN_FULL)
                    GumpInterface.create_status_gump()
                
                elif button_pressed == 21:  # Toggle Bandage Healing (in Auto Heal Settings)
                    config.BANDAGE_HEALING_ENABLED = not config.BANDAGE_HEALING_ENABLED
                    status_msg = "enabled" if config.BANDAGE_HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Bandage healing {status_msg} via Settings GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Recreate the Auto Heal Settings GUMP to show updated state
                    GumpInterface.create_auto_heal_settings_gump()
                
                elif button_pressed == 22:  # Toggle Potion Healing (in Auto Heal Settings)
                    config.POTION_HEALING_ENABLED = not config.POTION_HEALING_ENABLED
                    status_msg = "enabled" if config.POTION_HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Potion healing {status_msg} via Settings GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Recreate the Auto Heal Settings GUMP to show updated state
                    GumpInterface.create_auto_heal_settings_gump()
                    
        except Exception as e:
            Logger.debug(f"GUMP response handling error: {str(e)}")
        
        return True  # GUMP is still active

    @staticmethod
    def create_main_gump_new():
        """Create the new modular main GUMP with system summary lines"""
        config = BotConfig()
        messages = BotMessages()
        status = SystemStatus()
        
        # Get current status information
        runtime_minutes = status.get_runtime_minutes()
        
        # Create GUMP using proper Razor Enhanced pattern
        gd = Gumps.CreateGump(movable=True)
        Gumps.AddPage(gd, 0)
        
        # Background
        Gumps.AddBackground(gd, 0, 0, config.GUMP_WIDTH, config.GUMP_HEIGHT, 30546)
        Gumps.AddAlphaRegion(gd, 0, 0, config.GUMP_WIDTH, config.GUMP_HEIGHT)
        
        # Add title at the top center of the gump
        Gumps.AddHtml(gd, 70, 5, config.GUMP_WIDTH - 20, 25, f'<center><basefont color="#FFD700" size="5"><b>{messages.GUMP_TITLE}</b></basefont></center>', False, False)
        
        # Window control buttons in upper right corner
        # Close Button
        close_button_x = config.GUMP_WIDTH - 40
        close_button_y = 5
        Gumps.AddButton(gd, close_button_x, close_button_y, config.BUTTON_CANCEL, config.BUTTON_CANCEL_PRESSED, 4, 1, 0)
        Gumps.AddTooltip(gd, "Close Interface")
        
        # Minimize Button
        minimize_button_x = config.GUMP_WIDTH - 70
        minimize_button_y = 5
        Gumps.AddButton(gd, minimize_button_x, minimize_button_y, config.BUTTON_MINIMIZE_NORMAL, config.BUTTON_MINIMIZE_PRESSED, 3, 1, 0)
        Gumps.AddTooltip(gd, "Minimize Interface")
        
        # Add online status and runtime just below the title
        Gumps.AddHtml(gd, 80, 30, config.GUMP_WIDTH - 20, 20, f'<center><basefont color="#00FF00" size="3"><b>● {messages.GUMP_STATUS_ONLINE}</b></basefont> <basefont color="#CCCCCC" size="2">| Runtime: </basefont><basefont color="#FFFFFF" size="3"><b>{runtime_minutes}m</b></basefont></center>', False, False)
        
        # System summary section
        section_x = 65  # Centered position for system lines
        section_width = config.GUMP_WIDTH - 130  # Leave space for buttons on both sides
        current_y = 65
        
        # Player Status Section (keep as-is for now)
        current_y = GumpInterface.GumpSection.create_player_status_section(gd, section_x, current_y, section_width)
        current_y += 15  # Add spacing
        
        # Systems header
        Gumps.AddHtml(gd, section_x, current_y, section_width, 20, f'<center><basefont color="#87CEEB" size="3"><b>SYSTEMS</b></basefont></center>', False, False)
        current_y += 25
        
        # Auto Heal System Summary Line
        heal_status_text = "Healing..." if status.healing_active else "Ready"
        current_y = GumpInterface.GumpSection.create_system_summary_line(
            gd, section_x, current_y, section_width,
            system_name="AUTO HEAL",
            enabled=config.HEALING_ENABLED,
            active=status.healing_active,
            status_text=heal_status_text,
            enable_button_id=1,  # Toggle Auto Heal
            settings_button_id=10  # Open Auto Heal Settings
        )
        current_y += 5  # Small spacing between systems
        
        # Combat System Summary Line (placeholder for future)
        current_y = GumpInterface.GumpSection.create_system_summary_line(
            gd, section_x, current_y, section_width,
            system_name="COMBAT",
            enabled=config.COMBAT_ENABLED,
            active=False,  # Not implemented yet
            status_text="Not Implemented",
            enable_button_id=11,  # Toggle Combat (future)
            settings_button_id=12  # Open Combat Settings (future)
        )
        current_y += 5
        
        # Looting System Summary Line (placeholder for future)
        current_y = GumpInterface.GumpSection.create_system_summary_line(
            gd, section_x, current_y, section_width,
            system_name="LOOTING",
            enabled=False,  # Not implemented yet
            active=False,  # Not implemented yet
            status_text="Not Implemented",
            enable_button_id=13,  # Toggle Looting (future)
            settings_button_id=14  # Open Looting Settings (future)
        )
        
        # Debug Button - positioned in bottom left corner
        debug_button_x = 20
        debug_button_y = config.GUMP_HEIGHT - 35
        
        if config.DEBUG_MODE:
            Gumps.AddButton(gd, debug_button_x, debug_button_y, config.BUTTON_DEBUG_ENABLED, config.BUTTON_DEBUG_ENABLED_PRESSED, 2, 1, 0)
            debug_status = "ON"
            debug_color = "#00BFFF"
        else:
            Gumps.AddButton(gd, debug_button_x, debug_button_y, config.BUTTON_DEBUG_DISABLED, config.BUTTON_DEBUG_DISABLED_PRESSED, 2, 1, 0)
            debug_status = "OFF"
            debug_color = "#888888"
        Gumps.AddTooltip(gd, f"Toggle Debug Mode (Currently {debug_status})")
        
        # Debug button label
        debug_labels = f"""
        <basefont color="{debug_color}" size="2"><b>DEBUG</b></basefont><br>
        <basefont color="#CCCCCC" size="1">{debug_status}</basefont>
        """
        Gumps.AddHtml(gd, debug_button_x - 3, debug_button_y + 15, 60, 25, debug_labels, False, False)
        
        # Send the GUMP
        Gumps.SendGump(config.GUMP_ID, Player.Serial, config.GUMP_X, config.GUMP_Y, gd.gumpDefinition, gd.gumpStrings)
        
        Logger.debug("New modular main GUMP created and displayed")

    @staticmethod
    def create_auto_heal_settings_gump():
        """Create the Auto Heal Settings GUMP with detailed configuration options"""
        config = BotConfig()
        messages = BotMessages()
        status = SystemStatus()
        
        # Create GUMP using proper Razor Enhanced pattern
        gd = Gumps.CreateGump(movable=True)
        Gumps.AddPage(gd, 0)
        
        # Background (slightly taller for more options)
        settings_height = 300
        Gumps.AddBackground(gd, 0, 0, config.GUMP_WIDTH, settings_height, 30546)
        Gumps.AddAlphaRegion(gd, 0, 0, config.GUMP_WIDTH, settings_height)
        
        # Title
        Gumps.AddHtml(gd, 50, 5, config.GUMP_WIDTH - 20, 25, f'<center><basefont color="#FFD700" size="5"><b>AUTO HEAL SETTINGS</b></basefont></center>', False, False)
        
        # Back button in upper left corner
        back_button_x = 10
        back_button_y = 5
        Gumps.AddButton(gd, back_button_x, back_button_y, config.BUTTON_BACK, config.BUTTON_BACK_PRESSED, 20, 1, 0)  # Button ID 20 for back
        Gumps.AddTooltip(gd, "Back to Main GUMP")
        
        # Close Button in upper right corner
        close_button_x = config.GUMP_WIDTH - 30
        close_button_y = 5
        Gumps.AddButton(gd, close_button_x, close_button_y, config.BUTTON_CANCEL, config.BUTTON_CANCEL_PRESSED, 4, 1, 0)
        Gumps.AddTooltip(gd, "Close Interface")
        
        # Content area
        section_x = 20
        section_width = config.GUMP_WIDTH - 40
        current_y = 40
        
        # System Status Section
        system_status = "ENABLED" if config.HEALING_ENABLED else "DISABLED"
        system_color = "#00FF00" if config.HEALING_ENABLED else "#FF0000"
        status_text = "Healing..." if status.healing_active else "Ready"
        
        status_line = f'<basefont color="#87CEEB" size="3"><b>System Status:</b></basefont> <basefont color="{system_color}" size="3"><b>{system_status}</b></basefont>'
        if config.HEALING_ENABLED:
            status_line += f' <basefont color="#CCCCCC" size="2">({status_text})</basefont>'
        
        Gumps.AddHtml(gd, section_x, current_y, section_width, 20, status_line, False, False)
        current_y += 30
        
        # Healing Methods Section
        current_y = GumpInterface.GumpSection.create_section(
            gd, "HEALING METHODS", section_x, current_y, section_width,
            title_color="#87CEEB"
        )
        current_y += 5
        
        # Bandage Healing Toggle
        bandage_toggle_x = section_x + 10
        bandage_toggle_y = current_y + 2
        if config.BANDAGE_HEALING_ENABLED:
            bandage_art = config.BUTTON_ENABLED
            bandage_pressed_art = config.BUTTON_ENABLED_PRESSED
            bandage_status = "ENABLED"
            bandage_color = "#00FF00"
        else:
            bandage_art = config.BUTTON_DISABLE
            bandage_pressed_art = config.BUTTON_DISABLE_PRESSED
            bandage_status = "DISABLED"
            bandage_color = "#FF0000"
            
        Gumps.AddButton(gd, bandage_toggle_x, bandage_toggle_y, bandage_art, bandage_pressed_art, 21, 1, 0)  # Button ID 21
        Gumps.AddTooltip(gd, f"Toggle Bandage Healing ({'ON' if config.BANDAGE_HEALING_ENABLED else 'OFF'})")
        
        bandage_count = Items.FindByID(config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
        bandage_amount = bandage_count.Amount if bandage_count else 0
        bandage_line = f'<basefont color="#FFFFFF" size="3"><b>Bandage Healing:</b></basefont> <basefont color="{bandage_color}" size="2"><b>{bandage_status}</b></basefont> <basefont color="#CCCCCC" size="2">| Available: </basefont><basefont color="#FFFFFF" size="2"><b>{bandage_amount}</b></basefont> <basefont color="#CCCCCC" size="2">| Used: </basefont><basefont color="#FFFFFF" size="2"><b>{status.bandage_count}</b></basefont>'
        
        Gumps.AddHtml(gd, section_x + 30, current_y + 4, section_width - 30, 15, bandage_line, False, False)
        current_y += 25
        
        # Potion Healing Toggle
        potion_toggle_x = section_x + 10
        potion_toggle_y = current_y + 2
        if config.POTION_HEALING_ENABLED:
            potion_art = config.BUTTON_ENABLED
            potion_pressed_art = config.BUTTON_ENABLED_PRESSED
            potion_status = "ENABLED"
            potion_color = "#00FF00"
        else:
            potion_art = config.BUTTON_DISABLE
            potion_pressed_art = config.BUTTON_DISABLE_PRESSED
            potion_status = "DISABLED"
            potion_color = "#FF0000"
            
        Gumps.AddButton(gd, potion_toggle_x, potion_toggle_y, potion_art, potion_pressed_art, 22, 1, 0)  # Button ID 22
        Gumps.AddTooltip(gd, f"Toggle Potion Healing ({'ON' if config.POTION_HEALING_ENABLED else 'OFF'})")
        
        heal_potion_count = Items.FindByID(config.HEAL_POTION_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
        heal_potion_amount = heal_potion_count.Amount if heal_potion_count else 0
        potion_line = f'<basefont color="#FFFFFF" size="3"><b>Potion Healing:</b></basefont> <basefont color="{potion_color}" size="2"><b>{potion_status}</b></basefont> <basefont color="#CCCCCC" size="2">| Available: </basefont><basefont color="#FFFFFF" size="2"><b>{heal_potion_amount}</b></basefont> <basefont color="#CCCCCC" size="2">| Used: </basefont><basefont color="#FFFFFF" size="2"><b>{status.heal_potion_count}</b></basefont>'
        
        Gumps.AddHtml(gd, section_x + 30, current_y + 4, section_width - 30, 15, potion_line, False, False)
        current_y += 35
        
        # Health Thresholds Section
        current_y = GumpInterface.GumpSection.create_section(
            gd, "HEALTH THRESHOLDS", section_x, current_y, section_width,
            content_lines=[
                {
                    'text': f'Healing Threshold: <basefont color="#FFFF00" size="3"><b>{config.HEALING_THRESHOLD_PERCENTAGE}%</b></basefont> <basefont color="#CCCCCC" size="2">(Start healing below this %)</basefont>',
                    'color': '#FFFFFF'
                },
                {
                    'text': f'Critical Health: <basefont color="#FF6B6B" size="3"><b>{config.CRITICAL_HEALTH_THRESHOLD}%</b></basefont> <basefont color="#CCCCCC" size="2">(Use potions for fast healing)</basefont>',
                    'color': '#FFFFFF'
                }
            ],
            title_color="#87CEEB"
        )
        
        # Send the GUMP
        Gumps.SendGump(config.GUMP_ID, Player.Serial, config.GUMP_X, config.GUMP_Y, gd.gumpDefinition, gd.gumpStrings)
        
        Logger.debug("Auto Heal Settings GUMP created and displayed")

def update_gump_system():
    """Update the GUMP system - handle responses and periodic updates with real-time health tracking"""
    config = BotConfig()
    status = SystemStatus()
    
    # Don't update GUMP system if it was manually closed
    if status.gump_closed:
        return
    
    # Handle any GUMP responses
    gump_active = GumpInterface.handle_gump_response()
    
    # Check if any displayed data has changed
    data_changed = status.check_gump_data_changed()
    
    # Update GUMP only if data has changed or on periodic intervals
    if gump_active:
        status.gump_update_counter += 1
        should_update = (status.gump_update_counter >= config.GUMP_UPDATE_INTERVAL_CYCLES or data_changed)
        
        if should_update and data_changed:
            # Only update if data actually changed
            GumpInterface.create_status_gump()
            status.gump_update_counter = 0
            Logger.debug("GUMP updated due to data changes")
        elif should_update and not data_changed:
            # Reset counter but don't update gump since no data changed
            status.gump_update_counter = 0
            Logger.debug("GUMP update skipped - no data changes")
    
    # Show console status every 20 cycles (~5 seconds) only when debug mode is enabled
    if config.DEBUG_MODE and status.gump_update_counter == 0 and status.runtime_cycles % 20 == 0:
        runtime_minutes = status.get_runtime_minutes()
        bandage_count = Items.FindByID(config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
        bandage_amount = bandage_count.Amount if bandage_count else 0
        health_percentage = (Player.Hits / Player.HitsMax) * 100 if Player.HitsMax > 0 else 0
        
        Logger.debug(f"[DexBot] Status - Health: {Player.Hits}/{Player.HitsMax} ({health_percentage:.0f}%) | Bandages: {bandage_amount} (Used: {status.bandage_count}) {'[ON]' if config.BANDAGE_HEALING_ENABLED else '[OFF]'} | Potions: (Used: {status.heal_potion_count}) {'[ON]' if config.POTION_HEALING_ENABLED else '[OFF]'} | Runtime: {runtime_minutes}min")

# ===========================================
# MAIN LOOP
# ===========================================

def run_dexbot():
    """
    Main bot loop that runs continuously and manages different bot systems.
    """
    config = BotConfig()
    messages = BotMessages()
    status = SystemStatus()
    
    Logger.info(messages.STARTING)
    
    # Show status of different systems
    if config.HEALING_ENABLED:
        Logger.info(messages.HEALING_ENABLED)
        # Show individual healing method status
        if config.BANDAGE_HEALING_ENABLED:
            Logger.info("[DexBot] - Bandage healing: enabled")
        else:
            Logger.info("[DexBot] - Bandage healing: disabled")
        if config.POTION_HEALING_ENABLED:
            Logger.info("[DexBot] - Potion healing: enabled")
        else:
            Logger.info("[DexBot] - Potion healing: disabled")
    else:
        Logger.info(messages.HEALING_DISABLED)
    
    if config.DEBUG_MODE:
        Logger.debug("Debug mode is enabled")
    
    Logger.info(messages.ACTIVE)
    
    # Initialize GUMP system - set initial state to show main GUMP
    status.set_gump_state(GumpState.MAIN_FULL)
    
    # Create initial status GUMP
    GumpInterface.create_status_gump()
    Logger.info("[DexBot] Status GUMP created - use buttons to control bot")
    
    # Track previous states to avoid spam messages
    was_alive = True
    
    # Main loop runs until player disconnects or manually stopped
    while Player.Connected:
        try:
            # Check if player is alive
            if Player.IsGhost:
                if was_alive:
                    Logger.info(messages.WAITING_FOR_RESURRECTION)
                    status.healing_active = False
                    was_alive = False
                
                # Wait while dead - no bot functions work while dead
                Misc.Pause(config.WAITING_DELAY)
                continue
            else:
                # Player is alive
                if not was_alive:
                    Logger.info(messages.PLAYER_RESURRECTED)
                    was_alive = True
                    Journal.Clear()  # Clear journal after resurrection
            
            # Player is connected and alive - run enabled bot systems
            
            # Update GUMP system (handle interactions and periodic updates)
            update_gump_system()
            
            # Auto Heal system (if enabled)
            if config.HEALING_ENABLED:
                process_healing_journal()
                execute_auto_heal_system()
            
            # TODO: Add other bot systems here
            # if config.COMBAT_ENABLED:
            #     run_combat_system()
            # if config.LOOTING_ENABLED:
            #     run_looting_system()
            # if config.FISHING_ENABLED:
            #     run_fishing_system()
            
            # Increment runtime counter and main loop delay
            status.increment_runtime()
            Misc.Pause(config.DEFAULT_SCRIPT_DELAY)
            
        except KeyboardInterrupt:
            # Allow manual stopping with Ctrl+C or ESC
            Gumps.CloseGump(config.GUMP_ID)  # Close GUMP on exit
            Logger.info(messages.STOPPED)
            report = status.get_status_report()
            Logger.info(f"Final stats - Bandages used: {report['bandages_used']}, Heal potions used: {report['heal_potions_used']}")
            return
        except Exception as e:
            error_msg = messages.MAIN_LOOP_ERROR.format(str(e))
            Logger.error(error_msg)
            Misc.Pause(config.ERROR_RECOVERY_DELAY)
    
    # If we get here, player disconnected
    Gumps.CloseGump(config.GUMP_ID)  # Close GUMP on disconnect
    Logger.info(messages.DISCONNECTED)
    Logger.info(messages.STOPPED)
    
    # Show final status report
    report = status.get_status_report()
    Logger.info(f"Final stats - Bandages used: {report['bandages_used']}, Heal potions used: {report['heal_potions_used']}")

# ===========================================
# SCRIPT ENTRY POINT
# ===========================================

if __name__ == "__main__":
    run_dexbot()
