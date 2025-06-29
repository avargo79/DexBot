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
    has_bandages = bool(
        Items.FindByID(config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
    )
    has_heal_potions = bool(
        Items.FindByID(config.HEAL_POTION_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE)
    )
    return has_bandages, has_heal_potions
