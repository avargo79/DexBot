"""
Logging and Status Management System for DexBot
Provides standardized logging and runtime status tracking
"""

from typing import Dict, Optional, Union

from ..utils.imports import Items, Player


class Logger:
    """Simple logging system with different levels

    Provides standardized logging functionality with debug, info, error, and warning levels.
    Debug messages are only shown when DEBUG_MODE is enabled.
    """

    @staticmethod
    def debug(message: str) -> None:
        """Log debug message (only shown when DEBUG_MODE is enabled)"""
        from ..core.bot_config import BotConfig

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

    _instance: Optional["SystemStatus"] = None

    def __new__(cls) -> "SystemStatus":
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
            cls._instance.health_change_threshold = (
                5  # Update GUMP if health changes by this amount
            )
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
            cls._instance.shutdown_requested = False  # Flag to request script shutdown
            cls._instance.current_gump_state = (
                "closed"  # Import GumpState later to avoid circular imports
            )
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
            "healing": "Active" if self.healing_active else "Inactive",
            "bandages_used": self.bandage_count,
            "heal_potions_used": self.heal_potion_count,
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
        return self.current_gump_state != "closed"

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
        from ..core.bot_config import BotConfig

        config = BotConfig()

        # Get current values
        current_health = Player.Hits
        current_max_health = Player.HitsMax
        bandage_count = Items.FindByID(
            config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE
        )
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
            current_health != self.last_displayed_health
            or current_max_health != self.last_displayed_max_health
            or current_bandages != self.last_displayed_bandages
            or current_runtime != self.last_displayed_runtime
            or current_healing_enabled != self.last_displayed_healing_enabled
            or current_debug_enabled != self.last_displayed_debug_enabled
            or current_bandage_healing_enabled != self.last_displayed_bandage_healing_enabled
            or current_potion_healing_enabled != self.last_displayed_potion_healing_enabled
            or current_bandages_used != self.last_displayed_bandages_used
            or current_heal_potions_used != self.last_displayed_heal_potions_used
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

    def request_shutdown(self) -> None:
        """Request that the script shuts down gracefully"""
        self.shutdown_requested = True
        Logger.info("[DexBot] Shutdown requested via GUMP close button")

    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested"""
        return self.shutdown_requested
