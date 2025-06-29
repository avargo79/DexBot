"""
Main Bot Loop and Entry Point for DexBot
Coordinates all bot systems and handles the main execution loop
"""

from ..config.config_manager import ConfigManager
from ..core.bot_config import BotConfig, BotMessages, GumpState
from ..core.logger import Logger, SystemStatus
from ..systems.auto_heal import execute_auto_heal_system, process_healing_journal
from ..systems.combat import execute_combat_system
from ..systems.looting import LootingSystem
from ..ui.gump_interface import GumpInterface, update_gump_system
from ..utils.imports import Misc, Player


def run_dexbot():
    """
    Main bot loop that runs continuously and manages different bot systems.
    """
    config = BotConfig()
    messages = BotMessages()
    status = SystemStatus()
    config_manager = ConfigManager()
    
    # Initialize looting system
    looting_system = LootingSystem(config_manager)

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

    # Show combat system status
    if config_manager.get_combat_setting('system_toggles.combat_system_enabled'):
        Logger.info("[DexBot] Combat system: enabled")
    else:
        Logger.info("[DexBot] Combat system: disabled")

    # Show looting system status
    if looting_system.is_enabled():
        Logger.info("[DexBot] Looting system: enabled")
    else:
        Logger.info("[DexBot] Looting system: disabled")

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
                    # Clear journal after resurrection - import here to avoid circular imports
                    from ..utils.imports import Journal

                    Journal.Clear()

            # Player is connected and alive - run enabled bot systems

            # Update GUMP system (handle interactions and periodic updates)
            update_gump_system()

            # Auto Heal system (if enabled)
            if config.HEALING_ENABLED:
                process_healing_journal()
                execute_auto_heal_system()

            # Combat system (if enabled)
            execute_combat_system(config_manager)

            # Looting system (if enabled)
            looting_system.update()

            # Increment runtime counter and main loop delay
            status.increment_runtime()
            Misc.Pause(config.DEFAULT_SCRIPT_DELAY)

        except KeyboardInterrupt:
            # Allow manual stopping with Ctrl+C or ESC
            from ..utils.imports import Gumps

            Gumps.CloseGump(config.GUMP_ID)  # Close GUMP on exit
            Logger.info(messages.STOPPED)
            report = status.get_status_report()
            Logger.info(
                f"Final stats - Bandages used: {report['bandages_used']}, Heal potions used: {report['heal_potions_used']}"
            )
            return
        except Exception as e:
            error_msg = messages.MAIN_LOOP_ERROR.format(str(e))
            Logger.error(error_msg)
            Misc.Pause(config.ERROR_RECOVERY_DELAY)

    # If we get here, player disconnected
    from ..utils.imports import Gumps

    Gumps.CloseGump(config.GUMP_ID)  # Close GUMP on disconnect
    Logger.info(messages.DISCONNECTED)
    Logger.info(messages.STOPPED)

    # Show final status report
    report = status.get_status_report()
    Logger.info(
        f"Final stats - Bandages used: {report['bandages_used']}, Heal potions used: {report['heal_potions_used']}"
    )
