"""
Utility Functions for DexBot
Common helper functions used throughout the bot systems
"""

from typing import Tuple

from ..core.bot_config import BotConfig, BotMessages
from ..core.logger import Logger
from ..utils.imports import Items, Player


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

    # Use more efficient BackpackCount instead of FindByID when we only need count
    bandage_count = Items.BackpackCount(config.BANDAGE_ID, -1)
    if bandage_count > 0:
        if bandage_count <= config.LOW_BANDAGE_WARNING and log_errors:
            Logger.warning(messages.LOW_BANDAGES.format(bandage_count))
        return bandage_count
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
    # Use more efficient BackpackCount for resource checking
    has_bandages = Items.BackpackCount(config.BANDAGE_ID, -1) > 0
    has_heal_potions = Items.BackpackCount(config.HEAL_POTION_ID, -1) > 0
    return has_bandages, has_heal_potions
