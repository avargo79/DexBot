"""
Auto Heal System for DexBot
Handles automatic healing using bandages and potions based on Dexxor.py
"""

from ..core.bot_config import BotConfig, BotMessages
from ..core.logger import Logger, SystemStatus
from ..utils.helpers import check_bandage_supply, has_healing_resources
from ..utils.imports import Items, Journal, Misc, Player, Target, Timer


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
    needs_healing = (
        health_missing > config.BANDAGE_THRESHOLD
        or Player.Poisoned
        or health_percentage < config.HEALING_THRESHOLD_PERCENTAGE
    )

    if needs_healing:
        Logger.debug(
            f"Auto Heal needed - Health: {Player.Hits}/{Player.HitsMax} ({health_percentage:.1f}%)"
        )

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
                        Misc.Pause(config.BANDAGE_RETRY_DELAY)
                    else:
                        status.healing_active = False
                        return False
        elif config.BANDAGE_HEALING_ENABLED:
            # Only show "no bandages" error if bandage healing is enabled
            Logger.error(messages.NO_BANDAGES)
            return False

    status.healing_active = False
    return False
