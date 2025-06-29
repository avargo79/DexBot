"""
Looting System Module for DexBot
Automates looting corpses and skinning creatures with intelligent item filtering.
"""

import time
from typing import List, Optional, Dict, Tuple, Any
from enum import Enum

from ..config.config_manager import ConfigManager
from ..core.logger import Logger, SystemStatus
from ..utils.imports import Items, Misc, Mobiles, Player, Target, Timer


class LootDecision(Enum):
    """Enumeration for item looting decisions."""
    ALWAYS_TAKE = "always_take"
    TAKE_IF_SPACE = "take_if_space"
    NEVER_TAKE = "never_take"
    UNKNOWN = "unknown"


class LootResult:
    """Result of a looting operation."""
    def __init__(self, success: bool, items_taken: int = 0, message: str = ""):
        self.success = success
        self.items_taken = items_taken
        self.message = message
        self.timestamp = time.time()


class SkinResult:
    """Result of a skinning operation."""
    def __init__(self, success: bool, materials_gained: int = 0, message: str = ""):
        self.success = success
        self.materials_gained = materials_gained
        self.message = message
        self.timestamp = time.time()


class CorpseInfo:
    """Information about a discovered corpse."""
    def __init__(self, serial: int, position: Tuple[int, int], distance: float, 
                 creature_type: str = "Unknown", is_skinnable: bool = False):
        self.serial = serial
        self.position = position
        self.distance = distance
        self.creature_type = creature_type
        self.is_skinnable = is_skinnable
        self.discovered_time = time.time()
        self.looted = False
        self.skinned = False


class LootingSystem:
    """Handles automated looting and skinning logic for DexBot."""

    def __init__(self, config_manager: ConfigManager):
        """Initialize the Looting System.
        
        Args:
            config_manager: The configuration manager instance
        """
        self.config_manager = config_manager
        self.enabled = False
        self.last_corpse_scan = 0
        self.last_status_update = 0
        self.corpse_queue: List[CorpseInfo] = []
        self.processing_corpse = None
        
        # Performance tracking
        self.stats = {
            'corpses_processed': 0,
            'items_collected': 0,
            'gold_collected': 0,
            'creatures_skinned': 0,
            'total_runtime': 0,
            'last_reset': time.time()
        }
        
        # Cache for item evaluation to improve performance
        self.item_evaluation_cache: Dict[str, LootDecision] = {}
        self.cache_expiry = 300  # 5 minutes
        self.last_cache_cleanup = time.time()
        
        Logger.info("Looting System initialized")

    def is_enabled(self) -> bool:
        """Check if the looting system is enabled.
        
        Returns:
            bool: True if enabled, False otherwise
        """
        return self.enabled and self.config_manager.get_looting_config().get('enabled', False)

    def toggle_enabled(self) -> None:
        """Toggle the looting system enabled state."""
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        Logger.info(f"Looting System {status}")
        
        # Save state to configuration
        config = self.config_manager.get_looting_config()
        config['enabled'] = self.enabled
        self.config_manager.save_looting_config(config)

    def update(self) -> None:
        """Main update loop for the looting system.
        
        This method should be called regularly from the main bot loop.
        """
        if not self.is_enabled():
            return

        try:
            current_time = time.time()
            
            # Periodic cache cleanup
            self._cleanup_cache_if_needed(current_time)
            
            # Scan for new corpses
            self._scan_for_corpses_if_needed(current_time)
            
            # Process corpse queue
            self._process_corpse_queue()
            
            # Update status periodically
            self._update_status_if_needed(current_time)
            
        except Exception as e:
            Logger.error(f"Error in Looting System update: {e}")

    def scan_for_corpses(self) -> List[CorpseInfo]:
        """Scan for nearby corpses within configured range.
        
        Returns:
            List[CorpseInfo]: List of discovered corpses
        """
        if not self.is_enabled():
            return []

        try:
            config = self.config_manager.get_looting_config()
            max_range = config.get('behavior', {}).get('max_looting_range', 2)
            
            corpses = []
            player_x, player_y = Player.Position.X, Player.Position.Y
            
            # Find all corpse items in range
            corpse_items = Items.FindByID(0x2006, -1, Player.Backpack.Serial, -1, max_range)
            if corpse_items:
                for corpse_serial in corpse_items:
                    corpse_item = Items.FindBySerial(corpse_serial)
                    if corpse_item and hasattr(corpse_item, 'Position'):
                        # Calculate distance
                        dx = player_x - corpse_item.Position.X
                        dy = player_y - corpse_item.Position.Y
                        distance = (dx * dx + dy * dy) ** 0.5
                        
                        if distance <= max_range:
                            # Determine if corpse is skinnable
                            is_skinnable = self._is_corpse_skinnable(corpse_item)
                            creature_type = self._identify_creature_type(corpse_item)
                            
                            corpse_info = CorpseInfo(
                                serial=corpse_serial,
                                position=(corpse_item.Position.X, corpse_item.Position.Y),
                                distance=distance,
                                creature_type=creature_type,
                                is_skinnable=is_skinnable
                            )
                            corpses.append(corpse_info)
            
            Logger.debug(f"Found {len(corpses)} corpses in range")
            return corpses
            
        except Exception as e:
            Logger.error(f"Error scanning for corpses: {e}")
            return []

    def process_corpse_queue(self) -> None:
        """Process the queue of corpses to loot."""
        if not self.corpse_queue or self.processing_corpse:
            return

        # Get the next corpse to process
        next_corpse = self._get_next_corpse_to_process()
        if not next_corpse:
            return

        self.processing_corpse = next_corpse
        Logger.debug(f"Processing corpse: {next_corpse.creature_type} at distance {next_corpse.distance:.1f}")

        try:
            # Skin first if applicable
            if next_corpse.is_skinnable and not next_corpse.skinned:
                skin_result = self.skin_creature(next_corpse.serial)
                next_corpse.skinned = True
                if skin_result.success:
                    self.stats['creatures_skinned'] += 1
                    Logger.info(f"Skinned {next_corpse.creature_type}: {skin_result.message}")

            # Then loot the corpse
            if not next_corpse.looted:
                loot_result = self.loot_corpse(next_corpse.serial)
                next_corpse.looted = True
                if loot_result.success:
                    self.stats['corpses_processed'] += 1
                    self.stats['items_collected'] += loot_result.items_taken
                    Logger.info(f"Looted {next_corpse.creature_type}: {loot_result.message}")

            # Remove from queue when complete
            self.corpse_queue.remove(next_corpse)
            
        except Exception as e:
            Logger.error(f"Error processing corpse {next_corpse.serial}: {e}")
            # Remove problematic corpse from queue
            if next_corpse in self.corpse_queue:
                self.corpse_queue.remove(next_corpse)
        finally:
            self.processing_corpse = None

    def loot_corpse(self, corpse_serial: int) -> LootResult:
        """Loot a specific corpse.
        
        Args:
            corpse_serial: Serial number of the corpse to loot
            
        Returns:
            LootResult: Result of the looting operation
        """
        if not self.is_enabled():
            return LootResult(False, 0, "Looting system disabled")

        try:
            # Check inventory space first
            if not self._has_inventory_space():
                return LootResult(False, 0, "Inventory full")

            # Open the corpse container
            if not self._open_corpse_container(corpse_serial):
                return LootResult(False, 0, "Failed to open corpse")

            items_taken = 0
            config = self.config_manager.get_looting_config()
            action_delay = config.get('timing', {}).get('loot_action_delay_ms', 200)

            # Get all items in the corpse
            corpse_items = Items.FindAllBySerial(corpse_serial)
            if corpse_items:
                for item_serial in corpse_items:
                    if not self._has_inventory_space():
                        Logger.warning("Inventory full, stopping loot")
                        break

                    item = Items.FindBySerial(item_serial)
                    if item and self._should_loot_item(item):
                        if self._take_item(item):
                            items_taken += 1
                            Logger.debug(f"Took item: {item.Name}")
                        
                        # Delay between item actions
                        Misc.Pause(action_delay)

            return LootResult(True, items_taken, f"Collected {items_taken} items")

        except Exception as e:
            Logger.error(f"Error looting corpse {corpse_serial}: {e}")
            return LootResult(False, 0, f"Error: {str(e)}")

    def skin_creature(self, corpse_serial: int) -> SkinResult:
        """Skin a creature corpse.
        
        Args:
            corpse_serial: Serial number of the corpse to skin
            
        Returns:
            SkinResult: Result of the skinning operation
        """
        if not self.is_enabled():
            return SkinResult(False, 0, "Looting system disabled")

        try:
            config = self.config_manager.get_looting_config()
            if not config.get('behavior', {}).get('auto_skinning_enabled', True):
                return SkinResult(False, 0, "Skinning disabled")

            # Find skinning knife
            skinning_knife = self._find_skinning_knife()
            if not skinning_knife:
                return SkinResult(False, 0, "No skinning knife found")

            # Use the skinning knife on the corpse
            Items.UseItem(skinning_knife.Serial)
            Misc.Pause(500)  # Wait for targeting cursor
            
            Target.TargetExecute(corpse_serial)
            Misc.Pause(1000)  # Wait for skinning to complete

            # Check for skinning success (simplified)
            # In a real implementation, you'd check journal messages
            return SkinResult(True, 1, "Skinning completed")

        except Exception as e:
            Logger.error(f"Error skinning creature {corpse_serial}: {e}")
            return SkinResult(False, 0, f"Error: {str(e)}")

    def evaluate_item(self, item: Any) -> LootDecision:
        """Evaluate whether an item should be looted.
        
        Args:
            item: The item to evaluate
            
        Returns:
            LootDecision: The decision for this item
        """
        if not item or not hasattr(item, 'Name'):
            return LootDecision.NEVER_TAKE

        # Check cache first
        item_key = f"{item.ItemID}_{item.Name}"
        if item_key in self.item_evaluation_cache:
            return self.item_evaluation_cache[item_key]

        # Evaluate the item
        decision = self._evaluate_item_by_rules(item)
        
        # Cache the decision
        self.item_evaluation_cache[item_key] = decision
        return decision

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the looting system.
        
        Returns:
            Dict containing status information
        """
        return {
            'enabled': self.is_enabled(),
            'corpses_in_queue': len(self.corpse_queue),
            'processing_corpse': self.processing_corpse is not None,
            'stats': self.stats.copy(),
            'inventory_space': self._get_inventory_space_info()
        }

    def reset_stats(self) -> None:
        """Reset the statistics counters."""
        self.stats = {
            'corpses_processed': 0,
            'items_collected': 0,
            'gold_collected': 0,
            'creatures_skinned': 0,
            'total_runtime': 0,
            'last_reset': time.time()
        }
        Logger.info("Looting system statistics reset")

    # Private helper methods

    def _scan_for_corpses_if_needed(self, current_time: float) -> None:
        """Scan for corpses if enough time has passed."""
        config = self.config_manager.get_looting_config()
        scan_interval = config.get('timing', {}).get('corpse_scan_interval_ms', 1000) / 1000.0
        
        if current_time - self.last_corpse_scan >= scan_interval:
            new_corpses = self.scan_for_corpses()
            # Add new corpses to queue (avoid duplicates)
            for corpse in new_corpses:
                if not any(existing.serial == corpse.serial for existing in self.corpse_queue):
                    self.corpse_queue.append(corpse)
            
            self.last_corpse_scan = current_time

    def _process_corpse_queue(self) -> None:
        """Process the corpse queue."""
        if self.corpse_queue and not self.processing_corpse:
            self.process_corpse_queue()

    def _update_status_if_needed(self, current_time: float) -> None:
        """Update status if needed."""
        if current_time - self.last_status_update >= 1.0:  # Update every second
            self.last_status_update = current_time

    def _cleanup_cache_if_needed(self, current_time: float) -> None:
        """Clean up expired cache entries."""
        if current_time - self.last_cache_cleanup >= 60:  # Cleanup every minute
            # Simple cache cleanup - in a real implementation you'd track timestamps
            if len(self.item_evaluation_cache) > 1000:
                self.item_evaluation_cache.clear()
                Logger.debug("Cleared item evaluation cache")
            self.last_cache_cleanup = current_time

    def _get_next_corpse_to_process(self) -> Optional[CorpseInfo]:
        """Get the next corpse to process from the queue."""
        if not self.corpse_queue:
            return None
        
        # Sort by distance (closest first)
        self.corpse_queue.sort(key=lambda c: c.distance)
        return self.corpse_queue[0]

    def _has_inventory_space(self) -> bool:
        """Check if there's enough inventory space for looting.
        
        Returns:
            bool: True if there's adequate space, False otherwise
        """
        config = self.config_manager.get_looting_config()
        weight_limit = config.get('behavior', {}).get('inventory_weight_limit_percent', 80)
        item_limit = config.get('behavior', {}).get('inventory_item_limit', 120)
        
        # Check weight limit
        current_weight = Player.Weight
        max_weight = Player.MaxWeight
        
        if max_weight <= 0:
            Logger.warning("Max weight is 0, assuming inventory full")
            return False
            
        weight_percent = (current_weight / max_weight) * 100
        
        if weight_percent >= weight_limit:
            Logger.debug(f"Weight limit exceeded: {weight_percent:.1f}% >= {weight_limit}%")
            return False
        
        # Check item count limit
        current_item_count = self._count_backpack_items()
        if current_item_count >= item_limit:
            Logger.debug(f"Item count limit exceeded: {current_item_count} >= {item_limit}")
            return False
            
        Logger.debug(f"Inventory space available: {weight_percent:.1f}% weight, {current_item_count}/{item_limit} items")
        return True
        
    def _count_backpack_items(self) -> int:
        """Count the number of items in the player's backpack.
        
        Returns:
            int: Number of items in backpack
        """
        try:
            backpack_items = Items.FindAllBySerial(Player.Backpack.Serial)
            if backpack_items:
                return len(backpack_items)
            return 0
        except Exception as e:
            Logger.debug(f"Error counting backpack items: {e}")
            return 0  # Assume empty on error

    def _open_corpse_container(self, corpse_serial: int) -> bool:
        """Open a corpse container with retry logic.
        
        Args:
            corpse_serial: Serial number of the corpse to open
            
        Returns:
            bool: True if successfully opened, False otherwise
        """
        config = self.config_manager.get_looting_config()
        timeout_ms = config.get('timing', {}).get('container_open_timeout_ms', 2000)
        max_attempts = 3
        retry_delay_ms = 250
        
        for attempt in range(max_attempts):
            try:
                Logger.debug(f"Opening corpse {corpse_serial}, attempt {attempt + 1}/{max_attempts}")
                
                # Use the corpse to open it
                Items.UseItem(corpse_serial)
                Misc.Pause(timeout_ms)
                
                # Verify the container is accessible
                if self._verify_container_opened(corpse_serial):
                    Logger.debug(f"Successfully opened corpse {corpse_serial}")
                    return True
                    
                # If not opened and not last attempt, wait and retry
                if attempt < max_attempts - 1:
                    Logger.debug(f"Container not opened, retrying in {retry_delay_ms}ms")
                    Misc.Pause(retry_delay_ms)
                    
            except Exception as e:
                Logger.error(f"Exception opening corpse {corpse_serial} on attempt {attempt + 1}: {e}")
                if attempt < max_attempts - 1:
                    Misc.Pause(retry_delay_ms)
        
        Logger.warning(f"Failed to open corpse {corpse_serial} after {max_attempts} attempts")
        return False
        
    def _verify_container_opened(self, corpse_serial: int) -> bool:
        """Verify that a container was successfully opened.
        
        Args:
            corpse_serial: Serial number of the container to verify
            
        Returns:
            bool: True if container is accessible
        """
        try:
            # Try to get items from the container
            items = Items.FindAllBySerial(corpse_serial)
            return items is not None  # If we can get items list, container is open
        except Exception as e:
            Logger.debug(f"Container verification failed for {corpse_serial}: {e}")
            return False

    def _should_loot_item(self, item: Any) -> bool:
        """Determine if an item should be looted based on decision logic.
        
        Args:
            item: The item to evaluate
            
        Returns:
            bool: True if item should be looted
        """
        decision = self.evaluate_item(item)
        
        if decision == LootDecision.ALWAYS_TAKE:
            return True
        elif decision == LootDecision.NEVER_TAKE:
            return False
        elif decision == LootDecision.TAKE_IF_SPACE:
            # Only take if we have adequate inventory space
            return self._has_inventory_space()
        elif decision == LootDecision.UNKNOWN:
            # For unknown items, check if configured to take unknowns
            config = self.config_manager.get_looting_config()
            take_unknowns = config.get('behavior', {}).get('take_unknown_items', False)
            
            if take_unknowns and self._has_inventory_space():
                Logger.debug(f"Taking unknown item: {getattr(item, 'Name', 'Unknown')}")
                return True
            else:
                Logger.debug(f"Skipping unknown item: {getattr(item, 'Name', 'Unknown')}")
                return False
        
        return False

    def _take_item(self, item: Any) -> bool:
        """Take an item from a container with error handling.
        
        Args:
            item: The item to take
            
        Returns:
            bool: True if item was successfully taken
        """
        if not item or not hasattr(item, 'Serial'):
            Logger.debug("Invalid item provided to _take_item")
            return False
            
        try:
            item_name = getattr(item, 'Name', 'Unknown')
            item_amount = getattr(item, 'Amount', 1)
            
            Logger.debug(f"Attempting to take item: {item_name} (Amount: {item_amount})")
            
            # Check if we have space before attempting to move
            if not self._has_inventory_space():
                Logger.debug(f"No inventory space for {item_name}")
                return False
            
            # Move the item to player's backpack
            Items.Move(item.Serial, Player.Backpack.Serial, item_amount)
            
            # Wait for the move to process
            config = self.config_manager.get_looting_config()
            action_delay = config.get('timing', {}).get('loot_action_delay_ms', 200)
            Misc.Pause(action_delay)
            
            # Verify the item was moved successfully
            if self._verify_item_moved(item.Serial):
                Logger.debug(f"Successfully took {item_name}")
                self.stats['items_collected'] += 1
                
                # Track gold specifically
                if 'gold' in item_name.lower() or item.ItemID in [0x0EED, 0x0EEF]:  # Gold pile IDs
                    self.stats['gold_collected'] += item_amount
                    
                return True
            else:
                Logger.debug(f"Failed to verify {item_name} was moved")
                return False
                
        except Exception as e:
            Logger.error(f"Exception taking item {getattr(item, 'Name', 'Unknown')}: {e}")
            return False
            
    def _verify_item_moved(self, item_serial: int) -> bool:
        """Verify that an item was successfully moved to backpack.
        
        Args:
            item_serial: Serial number of the item to verify
            
        Returns:
            bool: True if item is now in backpack
        """
        try:
            # Check if item is now in the player's backpack
            item_in_backpack = Items.FindBySerial(item_serial)
            if item_in_backpack and hasattr(item_in_backpack, 'Container'):
                return item_in_backpack.Container == Player.Backpack.Serial
            return False
        except Exception as e:
            Logger.debug(f"Error verifying item move for {item_serial}: {e}")
            return False

    def _evaluate_item_by_rules(self, item: Any) -> LootDecision:
        """Evaluate an item based on configured rules.
        
        Args:
            item: The item to evaluate
            
        Returns:
            LootDecision: The looting decision for this item
        """
        if not item or not hasattr(item, 'Name'):
            return LootDecision.NEVER_TAKE
            
        config = self.config_manager.get_looting_config()
        loot_lists = config.get('loot_lists', {})
        
        item_name = item.Name.lower() if item.Name else ""
        item_id = getattr(item, 'ItemID', 0)
        
        # Check never take list first (highest priority)
        never_take = loot_lists.get('never_take', [])
        if self._matches_loot_rules(item_name, item_id, never_take):
            Logger.debug(f"Item {item_name} matches never_take rules")
            return LootDecision.NEVER_TAKE
        
        # Check always take list (second priority) 
        always_take = loot_lists.get('always_take', [])
        if self._matches_loot_rules(item_name, item_id, always_take):
            Logger.debug(f"Item {item_name} matches always_take rules")
            return LootDecision.ALWAYS_TAKE
        
        # Check take if space list (third priority)
        take_if_space = loot_lists.get('take_if_space', [])
        if self._matches_loot_rules(item_name, item_id, take_if_space):
            Logger.debug(f"Item {item_name} matches take_if_space rules")
            return LootDecision.TAKE_IF_SPACE
        
        # Default: unknown items are not taken unless explicitly configured
        Logger.debug(f"Item {item_name} (ID: {item_id}) not in any loot list - marked as unknown")
        return LootDecision.UNKNOWN
        
    def _matches_loot_rules(self, item_name: str, item_id: int, rule_list: List[str]) -> bool:
        """Check if an item matches any rule in a loot list.
        
        Args:
            item_name: The item name (lowercase)
            item_id: The item ID
            rule_list: List of rules to check against
            
        Returns:
            bool: True if item matches any rule
        """
        for rule in rule_list:
            rule_lower = rule.lower()
            
            # Check for exact item ID match (hex format like "0x0F0C")
            if rule_lower.startswith('0x'):
                try:
                    rule_id = int(rule_lower, 16)
                    if item_id == rule_id:
                        return True
                except ValueError:
                    pass  # Invalid hex format, continue with name matching
            
            # Check for partial name match
            elif rule_lower in item_name:
                return True
                
        return False

    def _is_corpse_skinnable(self, corpse_item: Any) -> bool:
        """Determine if a corpse can be skinned."""
        # Simplified implementation - would check creature body types
        return True  # Assume all corpses are skinnable for now

    def _identify_creature_type(self, corpse_item: Any) -> str:
        """Identify the type of creature from its corpse."""
        # Simplified implementation - would use body type or other indicators
        return "Unknown Creature"

    def _find_skinning_knife(self) -> Optional[Any]:
        """Find a skinning knife in inventory."""
        # Look for skinning knife item ID (0x0EC4)
        knives = Items.FindByID(0x0EC4, -1, Player.Backpack.Serial)
        if knives:
            return Items.FindBySerial(knives[0])
        return None

    def _get_inventory_space_info(self) -> Dict[str, Any]:
        """Get information about inventory space."""
        return {
            'current_weight': Player.Weight,
            'max_weight': Player.MaxWeight,
            'weight_percent': (Player.Weight / Player.MaxWeight) * 100 if Player.MaxWeight > 0 else 0
        }
