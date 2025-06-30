"""
Core Bot Configuration System
Manages all configuration constants using the Singleton pattern and ConfigManager
"""

import datetime
from typing import Optional

from ..config.config_manager import ConfigManager


class BotConfig:
    """Configuration constants for DexBot - now loads from JSON config files

    This class manages all configuration constants using the Singleton pattern
    and ConfigManager for persistent storage.
    """

    # Version Information
    VERSION = "3.0.0"
    VERSION_NAME = "Phase 3 - Integration Testing"
    BUILD_DATE = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    _instance: Optional["BotConfig"] = None

    def __new__(cls) -> "BotConfig":
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

    def get_version_info(self) -> str:
        """Get formatted version information for display"""
        return f"DexBot v{self.VERSION} ({self.VERSION_NAME}) - Build: {self.BUILD_DATE}"

    def _load_settings(self) -> None:
        """Load all settings from configuration files"""
        # System toggles from main config
        self.HEALING_ENABLED = self.config_manager.get_main_setting(
            "system_toggles.healing_system_enabled", True
        )
        self.DEBUG_MODE = self.config_manager.get_main_setting("global_settings.debug_mode", False)

        # Auto Heal specific toggles
        self.BANDAGE_HEALING_ENABLED = self.config_manager.get_auto_heal_setting(
            "healing_toggles.bandage_healing_enabled", True
        )
        self.POTION_HEALING_ENABLED = self.config_manager.get_auto_heal_setting(
            "healing_toggles.potion_healing_enabled", True
        )

        # Item IDs (convert hex strings to integers)
        bandage_id_str = self.config_manager.get_auto_heal_setting("item_ids.bandage_id", "0x0E21")
        self.BANDAGE_ID = (
            int(bandage_id_str, 16) if isinstance(bandage_id_str, str) else bandage_id_str
        )

        heal_potion_id_str = self.config_manager.get_auto_heal_setting(
            "item_ids.heal_potion_id", "0x0F0C"
        )
        self.HEAL_POTION_ID = (
            int(heal_potion_id_str, 16)
            if isinstance(heal_potion_id_str, str)
            else heal_potion_id_str
        )

        # Timer names (constants)
        self.HEALING_TIMER = "HEALING"

        # Timing settings from configs
        self.HEALING_TIMER_DURATION = self.config_manager.get_auto_heal_setting(
            "timing_settings.healing_timer_duration_ms", 11000
        )
        self.HEALING_CHECK_INTERVAL = self.config_manager.get_auto_heal_setting(
            "timing_settings.healing_check_interval", 1
        )
        self.POTION_COOLDOWN_MS = self.config_manager.get_auto_heal_setting(
            "timing_settings.potion_cooldown_ms", 10000
        )
        self.BANDAGE_RETRY_DELAY = self.config_manager.get_auto_heal_setting(
            "timing_settings.bandage_retry_delay_ms", 500
        )

        # Global timing settings
        self.DEFAULT_SCRIPT_DELAY = self.config_manager.get_main_setting(
            "global_settings.main_loop_delay_ms", 250
        )
        self.TARGET_WAIT_TIMEOUT = self.config_manager.get_main_setting(
            "global_settings.target_wait_timeout_ms", 1000
        )
        self.ERROR_RECOVERY_DELAY = self.config_manager.get_main_setting(
            "global_settings.error_recovery_delay_ms", 1000
        )
        self.WAITING_DELAY = 1000  # Static constant

        # Resource management settings
        self.SEARCH_RANGE = self.config_manager.get_auto_heal_setting(
            "resource_management.search_range", 2
        )
        self.BANDAGE_RETRY_ATTEMPTS = self.config_manager.get_auto_heal_setting(
            "resource_management.bandage_retry_attempts", 3
        )
        self.LOW_BANDAGE_WARNING = self.config_manager.get_auto_heal_setting(
            "resource_management.low_bandage_warning", 10
        )
        self.BANDAGE_CHECK_INTERVAL_CYCLES = self.config_manager.get_auto_heal_setting(
            "resource_management.bandage_check_interval_cycles", 120
        )

        # Health thresholds
        self.BANDAGE_THRESHOLD = self.config_manager.get_auto_heal_setting(
            "health_thresholds.bandage_threshold_hp", 1
        )
        self.HEALING_THRESHOLD_PERCENTAGE = self.config_manager.get_auto_heal_setting(
            "health_thresholds.healing_threshold_percentage", 95
        )
        self.CRITICAL_HEALTH_THRESHOLD = self.config_manager.get_auto_heal_setting(
            "health_thresholds.critical_health_threshold", 50
        )

        # Journal monitoring settings
        self.HEALING_SUCCESS_MSG = self.config_manager.get_auto_heal_setting(
            "journal_monitoring.healing_success_msg", "You finish applying the bandages."
        )
        self.HEALING_PARTIAL_MSG = self.config_manager.get_auto_heal_setting(
            "journal_monitoring.healing_partial_msg",
            "You apply the bandages, but they barely help.",
        )
        self.JOURNAL_MESSAGE_TYPE = self.config_manager.get_auto_heal_setting(
            "journal_monitoring.journal_message_type", "System"
        )

        # GUMP settings
        self.GUMP_ID = 12345  # Static constant
        self.GUMP_UPDATE_INTERVAL_CYCLES = self.config_manager.get_main_setting(
            "gump_interface.main_gump.update_interval_cycles", 8
        )
        self.GUMP_WIDTH = self.config_manager.get_main_setting(
            "gump_interface.main_gump.width", 320
        )
        self.GUMP_HEIGHT = self.config_manager.get_main_setting(
            "gump_interface.main_gump.height", 240
        )
        self.GUMP_X = self.config_manager.get_main_setting(
            "gump_interface.main_gump.x_position", 100
        )
        self.GUMP_Y = self.config_manager.get_main_setting(
            "gump_interface.main_gump.y_position", 100
        )
        self.GUMP_MIN_WIDTH = self.config_manager.get_main_setting(
            "gump_interface.minimized_gump.width", 100
        )
        self.GUMP_MIN_HEIGHT = self.config_manager.get_main_setting(
            "gump_interface.minimized_gump.height", 30
        )

        # Color thresholds
        self.BANDAGE_HIGH_THRESHOLD = self.config_manager.get_auto_heal_setting(
            "color_thresholds.bandage_high_threshold", 20
        )
        self.BANDAGE_MEDIUM_THRESHOLD = self.config_manager.get_auto_heal_setting(
            "color_thresholds.bandage_medium_threshold", 10
        )
        self.POTION_HIGH_THRESHOLD = self.config_manager.get_auto_heal_setting(
            "color_thresholds.potion_high_threshold", 10
        )
        self.POTION_MEDIUM_THRESHOLD = self.config_manager.get_auto_heal_setting(
            "color_thresholds.potion_medium_threshold", 5
        )
        self.HEALTH_HIGH_THRESHOLD = self.config_manager.get_auto_heal_setting(
            "color_thresholds.health_high_threshold", 75
        )
        self.HEALTH_MEDIUM_THRESHOLD = self.config_manager.get_auto_heal_setting(
            "color_thresholds.health_medium_threshold", 50
        )

        # GUMP Background ID
        self.BACKGROUND_ID = 9200  # Standard UO GUMP background

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
        
        # Healing-specific button icons (combat system uses these for consistency)
        self.BUTTON_HEAL_ENABLED = 4017
        self.BUTTON_HEAL_ENABLED_PRESSED = 4019
        self.BUTTON_HEAL_DISABLED = 4005
        self.BUTTON_HEAL_DISABLED_PRESSED = 4007

    def save_settings(self) -> bool:
        """Save current settings back to configuration files"""
        try:
            # Update main config values
            self.config_manager.set_main_setting(
                "system_toggles.healing_system_enabled", self.HEALING_ENABLED
            )
            self.config_manager.set_main_setting("global_settings.debug_mode", self.DEBUG_MODE)

            # Update auto heal config values
            self.config_manager.set_auto_heal_setting(
                "healing_toggles.bandage_healing_enabled", self.BANDAGE_HEALING_ENABLED
            )
            self.config_manager.set_auto_heal_setting(
                "healing_toggles.potion_healing_enabled", self.POTION_HEALING_ENABLED
            )

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

    _instance: Optional["BotMessages"] = None

    def __new__(cls) -> "BotMessages":
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


class GumpState:
    """Simple enumeration of possible GUMP states (using class constants for compatibility)"""

    CLOSED = "closed"
    MAIN_FULL = "main_full"
    MAIN_MINIMIZED = "main_minimized"
    BOT_SETTINGS = "bot_settings"
    COMBAT_SETTINGS = "combat_settings"
    LOOTING_SETTINGS = "looting_settings"
