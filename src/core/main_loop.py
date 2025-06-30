"""
Main Bot Loop and Entry Point for DexBot
Coordinates all bot systems and handles the main execution loop
"""

import time
from datetime import datetime
from ..config.config_manager import ConfigManager
from ..core.bot_config import BotConfig, BotMessages, GumpState
from ..core.logger import Logger, SystemStatus
from ..systems.auto_heal import execute_auto_heal_system, process_healing_journal
from ..systems.combat import CombatSystem
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
    
    # Initialize systems
    looting_system = LootingSystem(config_manager)
    combat_system = CombatSystem(config_manager)

    # Display version and build information prominently
    version_info = config.get_version_info()
    Logger.info("=" * 60)
    Logger.info(f"🤖 {version_info}")
    Logger.info("=" * 60)
    
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
    combat_enabled = config_manager.get_combat_setting('system_toggles.combat_system_enabled')
    auto_target = config_manager.get_combat_setting('system_toggles.auto_target_enabled')
    auto_attack = config_manager.get_combat_setting('system_toggles.auto_attack_enabled')
    
    if combat_enabled:
        Logger.info("[DexBot] Combat system: enabled")
        Logger.info(f"[DexBot] - Auto target: {'enabled' if auto_target else 'disabled'}")
        Logger.info(f"[DexBot] - Auto attack: {'enabled' if auto_attack else 'disabled'}")
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
    Logger.info("[DexBot] Click the Close button to stop the script completely")

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
            loop_start_time = time.time()
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Include milliseconds
            Logger.info(f"MAIN LOOP: ===== Phase 3.1 Optimized - System Updates [{timestamp}] =====")

            # Check for shutdown requests (e.g., from GUMP close button)
            if status.is_shutdown_requested():
                Logger.info("[DexBot] Shutdown requested - stopping script")
                break

            # Update GUMP system (handle interactions and periodic updates)
            gump_start_time = time.time()
            update_gump_system()
            gump_duration = (time.time() - gump_start_time) * 1000  # Convert to milliseconds
            Logger.debug(f"MAIN LOOP: GUMP update completed in {gump_duration:.1f}ms")

            # PHASE 3.1 OPTIMIZATION: Run systems in priority order with minimal overhead
            # Priority: Healing > Combat > Looting
            
            # 1. Auto Heal system (highest priority - survival)
            if config.HEALING_ENABLED:
                heal_start_time = time.time()
                Logger.debug(f"MAIN LOOP: Processing healing system...")
                process_healing_journal()
                execute_auto_heal_system()
                heal_duration = (time.time() - heal_start_time) * 1000
                if heal_duration > 200:  # Only log if significant time spent
                    Logger.info(f"MAIN LOOP: Healing system completed in {heal_duration:.1f}ms")

            # 2. Combat system (medium priority - engagement)
            combat_start_time = time.time()
            Logger.debug(f"MAIN LOOP: Processing combat system...")
            try:
                combat_system.run()
                combat_duration = (time.time() - combat_start_time) * 1000
                if combat_duration > 200:  # Only log if significant time spent
                    Logger.info(f"MAIN LOOP: Combat system completed in {combat_duration:.1f}ms")
            except Exception as e:
                combat_duration = (time.time() - combat_start_time) * 1000
                Logger.error(f"MAIN LOOP: Error in combat system after {combat_duration:.1f}ms: {e}")

            # 3. Looting system (lowest priority - cleanup)
            loot_start_time = time.time()
            Logger.debug(f"MAIN LOOP: Processing looting system...")
            try:
                looting_system.update()
                loot_duration = (time.time() - loot_start_time) * 1000
                if loot_duration > 200:  # Only log if significant time spent
                    Logger.info(f"MAIN LOOP: Looting system completed in {loot_duration:.1f}ms")
            except Exception as e:
                loot_duration = (time.time() - loot_start_time) * 1000
                Logger.error(f"MAIN LOOP: Error in looting system after {loot_duration:.1f}ms: {e}")

            # Calculate total loop time
            loop_duration = (time.time() - loop_start_time) * 1000
            end_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            # Optimized logging: only show detailed timing for slow loops
            if loop_duration > 1000:  # More than 1 second
                Logger.warning(f"PERFORMANCE: Main loop took {loop_duration:.1f}ms - potential issue! [{end_timestamp}]")
            elif loop_duration > 500:  # More than 500ms  
                Logger.info(f"MAIN LOOP: All systems completed in {loop_duration:.1f}ms [{end_timestamp}]")
            else:
                Logger.debug(f"MAIN LOOP: All systems completed in {loop_duration:.1f}ms [{end_timestamp}]")
            
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

    # Check if shutdown was requested (e.g., via GUMP close button)
    if status.is_shutdown_requested():
        from ..utils.imports import Gumps
        Gumps.CloseGump(config.GUMP_ID)  # Close GUMP on shutdown
        Logger.info(messages.STOPPED)
        report = status.get_status_report()
        Logger.info(
            f"Final stats - Bandages used: {report['bandages_used']}, Heal potions used: {report['heal_potions_used']}"
        )
        return

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




