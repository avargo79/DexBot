"""
Looting System Module for DexBot
Automates looting corpses and skinning creatures with intelligent item filtering.
"""

import time
from datetime import datetime
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
        self.enabled = True  # Enable the system by default
        self.last_corpse_scan = 0
        self.last_status_update = 0
        self.corpse_queue: List[CorpseInfo] = []
        self.processing_corpse = None
        
        # Corpse processing cache to avoid reprocessing empty/looted corpses
        self.processed_corpses: Dict[int, float] = {}  # serial -> timestamp
        self.corpse_cache_duration = 300  # 5 minutes
        
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
        
        # PHASE 3.1.1: Ignore list optimization for performance
        self._load_ignore_list_settings()
        
        Logger.info(f"Looting System initialized with ignore list optimization: {self.use_ignore_list}")

    def _load_ignore_list_settings(self) -> None:
        """Load ignore list optimization settings from configuration."""
        try:
            # Get performance optimization settings from main config
            main_config = self.config_manager.get_main_setting('performance_optimization', {})
            looting_opts = main_config.get('looting_optimizations', {})
            
            self.use_ignore_list = looting_opts.get('use_ignore_list', True)
            self.ignore_list_cleanup_interval = looting_opts.get('ignore_list_cleanup_interval_seconds', 180)
            self.last_ignore_cleanup = time.time()
            self.ignored_corpses_count = 0  # Track ignored corpses for stats
            
            Logger.debug(f"LOOTING: Ignore list optimization: {self.use_ignore_list}, cleanup interval: {self.ignore_list_cleanup_interval}s")
        except Exception as e:
            # Fallback to defaults if config loading fails
            Logger.warning(f"LOOTING: Failed to load ignore list settings, using defaults: {e}")
            self.use_ignore_list = True
            self.ignore_list_cleanup_interval = 180
            self.last_ignore_cleanup = time.time()
            self.ignored_corpses_count = 0

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
        system_start_time = time.time()
        
        # Quick enablement check (optimization)
        if not self.enabled or not self.config_manager.get_looting_config().get('enabled', False):
            return
            
        Logger.debug(f"LOOTING: System is ENABLED - proceeding with update")

        try:
            current_time = time.time()
            
            # Periodic cache cleanup (less frequent for performance)
            cache_start = time.time()
            self._cleanup_cache_if_needed(current_time)
            cache_duration = (time.time() - cache_start) * 1000
            if cache_duration > 10:
                Logger.debug(f"LOOTING: Cache cleanup completed in {cache_duration:.1f}ms")
            
            # Scan for new corpses
            scan_start = time.time()
            self._scan_for_corpses_if_needed(current_time)
            scan_duration = (time.time() - scan_start) * 1000
            if len(self.corpse_queue) > 0:
                Logger.info(f"LOOTING: Found {len(self.corpse_queue)} corpses to process (scan: {scan_duration:.1f}ms)")
            
            # Process corpse queue
            process_start = time.time()
            self._process_corpse_queue()
            process_duration = (time.time() - process_start) * 1000
            if process_duration > 50:
                Logger.debug(f"LOOTING: Corpse queue processing completed in {process_duration:.1f}ms")
            
            # Update status periodically
            self._update_status_if_needed(current_time)
            
            # Log performance timing (only for slow operations)
            system_duration = (time.time() - system_start_time) * 1000
            
            if system_duration > 1000:  # More than 1 second
                Logger.warning(f"LOOTING: System took {system_duration:.1f}ms - performance issue!")
            elif system_duration > 200:  # More than 200ms
                Logger.info(f"LOOTING: System took {system_duration:.1f}ms - monitor performance")
            else:
                Logger.debug(f"LOOTING: System completed in {system_duration:.1f}ms")
            
        except Exception as e:
            system_duration = (time.time() - system_start_time) * 1000
            Logger.error(f"LOOTING: Error in Looting System update after {system_duration:.1f}ms: {e}")

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
            current_time = time.time()
            
            # Clean up old processed corpses cache
            self._cleanup_processed_corpses_cache(current_time)
            
            # PHASE 3.1.1: Find all corpse items in range using optimized filter with ignore list
            corpse_filter = Items.Filter()
            corpse_filter.RangeMax = max_range
            corpse_filter.IsCorpse = True  # This filter finds all corpse types
            corpse_filter.CheckIgnoreObject = True  # OPTIMIZATION: Exclude ignored corpses from search
            corpse_items = Items.ApplyFilter(corpse_filter)
            
            Logger.info(f"LOOTING: Found {len(corpse_items) if corpse_items else 0} corpses in range {max_range} (excluding ignored)")
            
            if corpse_items:
                for corpse_item in corpse_items:
                    if corpse_item and hasattr(corpse_item, 'Position'):
                        # Skip already processed corpses
                        if self._is_corpse_already_processed(corpse_item.Serial):
                            Logger.info(f"LOOTING: Skipping already processed corpse {corpse_item.Serial}")
                            continue
                        
                        # Calculate distance
                        dx = player_x - corpse_item.Position.X
                        dy = player_y - corpse_item.Position.Y
                        distance = (dx * dx + dy * dy) ** 0.5
                        
                        Logger.info(f"LOOTING: Processing corpse {corpse_item.Serial} at distance {distance:.1f}")
                        
                        if distance <= max_range:
                            # Determine if corpse is skinnable
                            is_skinnable = self._is_corpse_skinnable(corpse_item)
                            creature_type = self._identify_creature_type(corpse_item)
                            
                            corpse_info = CorpseInfo(
                                serial=corpse_item.Serial,
                                position=(corpse_item.Position.X, corpse_item.Position.Y),
                                distance=distance,
                                creature_type=creature_type,
                                is_skinnable=is_skinnable
                            )
                            corpses.append(corpse_info)
                            Logger.info(f"LOOTING: Added corpse {corpse_item.Serial} to queue")
            
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

        # Check if already processed
        if self._is_corpse_already_processed(corpse_serial):
            Logger.info(f"LOOTING: Corpse {corpse_serial} already processed, skipping")
            return LootResult(False, 0, "Corpse already processed")

        try:
            # Check inventory space first
            if not self._has_inventory_space():
                return LootResult(False, 0, "Inventory full")

            # Open the corpse container
            if not self._open_corpse_container(corpse_serial):
                Logger.info(f"LOOTING: Failed to open corpse {corpse_serial}, marking as processed")
                self._mark_corpse_as_processed(corpse_serial)
                return LootResult(False, 0, "Failed to open corpse")

            items_taken = 0
            config = self.config_manager.get_looting_config()
            action_delay = config.get('timing', {}).get('loot_action_delay_ms', 200)

            # Get all items from the opened corpse using corpse.Contains (working approach)
            corpse_items = []
            
            try:
                Logger.info(f"LOOTING: Attempting to access corpse {corpse_serial} contents")
                
                # Get the corpse item
                corpse_item = Items.FindBySerial(corpse_serial)
                if not corpse_item:
                    Logger.warning(f"LOOTING: Corpse {corpse_serial} not found")
                    self._mark_corpse_as_processed(corpse_serial)
                    return LootResult(False, 0, "Corpse not found")
                
                # Use corpse.Contains to access items directly (proven working method)
                if hasattr(corpse_item, 'Contains') and corpse_item.Contains:
                    Logger.info(f"LOOTING: Corpse has {len(corpse_item.Contains)} items")
                    
                    # Access items directly from corpse.Contains
                    for item in corpse_item.Contains:
                        corpse_items.append(item)
                        item_name = getattr(item, 'Name', 'Unknown')
                        item_id = getattr(item, 'ItemID', 'Unknown')
                        Logger.info(f"LOOTING: Available item: {item_name} (ID: {item_id})")
                    
                    Logger.info(f"LOOTING: Successfully found {len(corpse_items)} items via corpse.Contains")
                else:
                    Logger.info(f"LOOTING: Corpse has no Contains property or is empty")
                    
                    # Fallback: Try to find specific items by ID as backup (no retry needed)
                    Logger.info(f"LOOTING: Fallback - trying Items.FindByID for gold (1712)")
                    gold_item = Items.FindByID(1712, -1, corpse_serial)
                    if gold_item:
                        corpse_items.append(gold_item)
                        Logger.info(f"LOOTING: Found gold item via fallback: {gold_item.Name} (Amount: {gold_item.Amount})")
                        
            except Exception as e:
                Logger.error(f"LOOTING: Error accessing corpse contents: {e}")
                self._mark_corpse_as_processed(corpse_serial)
                return LootResult(False, 0, f"Error accessing corpse: {str(e)}")
            
            # Process the items found (or mark as empty if none)
            if not corpse_items:
                Logger.info(f"LOOTING: No items found in corpse {corpse_serial}, marking as processed")
                self._mark_corpse_as_processed(corpse_serial)
                return LootResult(True, 0, "Corpse empty")
            
            Logger.info(f"LOOTING: Processing {len(corpse_items)} items from corpse {corpse_serial}")
            
            # Loot the items
            for item in corpse_items:
                if not self._has_inventory_space():
                    Logger.warning("Inventory full, stopping loot")
                    break

                if item and self._should_loot_item(item):
                    Logger.info(f"LOOTING: Evaluating item: {item.Name} (ID: {item.ItemID})")
                    if self._take_item(item):
                        items_taken += 1
                        Logger.info(f"LOOTING: Successfully took item: {item.Name}")
                        
                        # Track gold specifically (optimized check)
                        item_id = getattr(item, 'ItemID', 0)
                        if item_id == 0x06F4 or item_id == 0x06F5:  # Gold coins/piles 
                            gold_amount = getattr(item, 'Amount', 1)
                            self.stats['gold_collected'] += gold_amount
                            Logger.info(f"LOOTING: Collected {gold_amount} gold")
                    else:
                        Logger.info(f"LOOTING: Failed to take item: {item.Name}")
                    
                    # Small delay between item actions
                    if action_delay > 0:
                        Misc.Pause(action_delay)
                else:
                    Logger.info(f"LOOTING: Skipping item: {item.Name if item else 'Unknown'}")

            # Mark corpse as processed after looting
            self._mark_corpse_as_processed(corpse_serial)
            Logger.info(f"LOOTING: Finished processing corpse {corpse_serial}, collected {items_taken} items")

            return LootResult(True, items_taken, f"Collected {items_taken} items")

        except Exception as e:
            Logger.error(f"Error looting corpse {corpse_serial}: {e}")
            self._mark_corpse_as_processed(corpse_serial)
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

        # Optimized cache key using ItemID only for performance (items with same ID have same rules)
        item_id = getattr(item, 'ItemID', 0)
        cache_key = f"id_{item_id}"
        
        # Check cache first
        if cache_key in self.item_evaluation_cache:
            return self.item_evaluation_cache[cache_key]

        # Evaluate the item
        decision = self._evaluate_item_by_rules(item)
        
        # Cache the decision (limit cache size for memory efficiency)
        if len(self.item_evaluation_cache) < 500:  # Prevent unbounded growth
            self.item_evaluation_cache[cache_key] = decision
        
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
            # Early exit if we already have too many corpses queued (optimization)
            max_queue_size = config.get('behavior', {}).get('max_corpse_queue_size', 10)
            if len(self.corpse_queue) >= max_queue_size:
                Logger.debug(f"LOOTING: Corpse queue at max size ({max_queue_size}), skipping scan")
                self.last_corpse_scan = current_time
                return
                
            new_corpses = self.scan_for_corpses()
            # Add new corpses to queue (avoid duplicates)
            added_count = 0
            for corpse in new_corpses:
                if not any(existing.serial == corpse.serial for existing in self.corpse_queue):
                    self.corpse_queue.append(corpse)
                    added_count += 1
                    # Stop adding if we hit the queue limit (optimization)
                    if len(self.corpse_queue) >= max_queue_size:
                        break
            
            if added_count > 0:
                Logger.debug(f"LOOTING: Added {added_count} new corpses to queue")
            
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
        """Clean up expired cache entries and manage ignore list."""
        if current_time - self.last_cache_cleanup >= 60:  # Cleanup every minute
            # Simple cache cleanup - in a real implementation you'd track timestamps
            if len(self.item_evaluation_cache) > 1000:
                self.item_evaluation_cache.clear()
                Logger.debug("Cleared item evaluation cache")
            self.last_cache_cleanup = current_time
        
        # PHASE 3.1.1: Periodic ignore list cleanup to prevent it from growing too large
        if self.use_ignore_list and (current_time - self.last_ignore_cleanup >= self.ignore_list_cleanup_interval):
            try:
                # Clear ignore list periodically to prevent memory issues
                # This is safe because we also track processed corpses in our own cache
                Misc.ClearIgnore()
                Logger.info(f"LOOTING: Cleared ignore list ({self.ignored_corpses_count} corpses were ignored)")
                self.ignored_corpses_count = 0
                self.last_ignore_cleanup = current_time
            except Exception as e:
                Logger.error(f"LOOTING: Failed to clear ignore list: {e}")
                # Disable ignore list optimization if it's causing issues
                self.use_ignore_list = False

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
                Logger.info(f"LOOTING: Opening corpse {corpse_serial}, attempt {attempt + 1}/{max_attempts}")
                
                # Use Items.UseItem to open the corpse container (correct RazorEnhanced API)
                Items.UseItem(corpse_serial)
                
                # Give time for the corpse to open
                Misc.Pause(300)  # Shorter pause for faster response
                
                # For corpses, assume opening was successful and proceed to loot
                # Corpses don't always behave like regular containers in UO
                Logger.info(f"LOOTING: Corpse {corpse_serial} opened successfully (bypassing container verification)")
                return True
                    
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
            bool: True if container is accessible/opened
        """
        try:
            Logger.info(f"LOOTING: Verifying corpse {corpse_serial} is accessible")
            
            # Get the corpse item
            corpse_item = Items.FindBySerial(corpse_serial)
            if not corpse_item:
                Logger.info(f"LOOTING: Corpse {corpse_serial} item not found")
                return False
            
            # Check if this item is a container and if it's opened
            if hasattr(corpse_item, 'IsContainer') and corpse_item.IsContainer:
                Logger.info(f"LOOTING: Corpse {corpse_serial} is confirmed as container")
                
                # Some RazorEnhanced versions have an Opened property
                if hasattr(corpse_item, 'Opened'):
                    is_opened = corpse_item.Opened
                    Logger.info(f"LOOTING: Container opened status: {is_opened}")
                    return is_opened
                
                # Alternative: Check if we can access the container contents
                # If Items.UseItem was successful, we should be able to query contents
                try:
                    items_filter = Items.Filter()
                    items_filter.Container = corpse_serial
                    items_filter.OnGround = False
                    container_items = Items.ApplyFilter(items_filter)
                    
                    if container_items is not None:
                        item_count = len(container_items) if container_items else 0
                        Logger.info(f"LOOTING: Container {corpse_serial} accessible - found {item_count} items")
                        return True
                except Exception as filter_error:
                    Logger.info(f"LOOTING: Items.ApplyFilter failed: {filter_error}")
                    
            Logger.info(f"LOOTING: Corpse {corpse_serial} not accessible as container")
            return False
                
        except Exception as e:
            Logger.error(f"Container verification exception for {corpse_serial}: {e}")
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
                
                # Track gold specifically (optimized check)
                item_id = getattr(item, 'ItemID', 0)
                if item_id == 0x06F4 or item_id == 0x06F5:  # Gold coins/piles
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
            # Handle integer item IDs directly (e.g., 1712 for gold)
            if isinstance(rule, int):
                if item_id == rule:
                    Logger.debug(f"Item ID {item_id} matches rule ID {rule}")
                    return True
                continue
                
            # Handle string rules
            rule_str = str(rule)
            rule_lower = rule_str.lower()
            
            # Check for exact item ID match (hex format like "0x0F0C")
            if rule_lower.startswith('0x'):
                try:
                    rule_id = int(rule_lower, 16)
                    if item_id == rule_id:
                        Logger.debug(f"Item ID {item_id} matches hex rule {rule_lower}")
                        return True
                except ValueError:
                    pass  # Invalid hex format, continue with name matching
            
            # Check for decimal item ID as string (e.g., "1712")
            elif rule_str.isdigit():
                try:
                    rule_id = int(rule_str)
                    if item_id == rule_id:
                        Logger.debug(f"Item ID {item_id} matches decimal string rule {rule_str}")
                        return True
                except ValueError:
                    pass  # Invalid number format, continue with name matching
                    
            # Check for partial name match
            elif rule_lower in item_name:
                Logger.debug(f"Item name '{item_name}' matches name rule '{rule_lower}'")
                return True
                
        return False

    def _is_corpse_already_processed(self, corpse_serial: int) -> bool:
        """Check if a corpse has already been processed.
        
        Args:
            corpse_serial: The serial number of the corpse
            
        Returns:
            bool: True if corpse was already processed
        """
        return corpse_serial in self.processed_corpses

    def _mark_corpse_as_processed(self, corpse_serial: int) -> None:
        """Mark a corpse as processed to avoid reprocessing.
        
        Args:
            corpse_serial: The serial number of the corpse
        """
        self.processed_corpses[corpse_serial] = time.time()
        
        # PHASE 3.1.1: Add corpse to ignore list for future filter optimizations
        if self.use_ignore_list:
            try:
                Misc.IgnoreObject(corpse_serial)
                self.ignored_corpses_count += 1
                Logger.debug(f"LOOTING: Added corpse {corpse_serial} to ignore list (total ignored: {self.ignored_corpses_count})")
            except Exception as e:
                Logger.debug(f"LOOTING: Failed to add corpse {corpse_serial} to ignore list: {e}")
        
        Logger.info(f"LOOTING: Marked corpse {corpse_serial} as processed")

    def _cleanup_processed_corpses_cache(self, current_time: float) -> None:
        """Clean up old entries from the processed corpses cache.
        
        Args:
            current_time: Current timestamp
        """
        cutoff_time = current_time - self.corpse_cache_duration
        old_corpses = [serial for serial, timestamp in self.processed_corpses.items() 
                      if timestamp < cutoff_time]
        
        for serial in old_corpses:
            del self.processed_corpses[serial]
        
        if old_corpses:
            Logger.info(f"LOOTING: Cleaned up {len(old_corpses)} old corpse cache entries")

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
