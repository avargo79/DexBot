"""
Combat System Module for DexBot
Automates engaging and defeating enemies with smart target selection and combat monitoring.
"""

import math
import time
from datetime import datetime
from typing import List, Optional, Dict

from ..config.config_manager import ConfigManager
from ..core.logger import Logger, SystemStatus
from ..utils.imports import Items, Misc, Mobiles, Player, Target, Timer


class CombatSystem:
    """Handles automated combat logic for DexBot."""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.current_target = None
        self.combat_start_time = None
        self.last_target_scan = 0
        self.last_attack_time = 0
        self.last_target_name_display = 0  # Track when we last displayed target name
        
        # Performance optimization: Mobile data caching
        self.mobile_cache = {}  # Cache mobile data with timestamps
        self.cache_duration = 500  # 500ms cache duration
        self.health_bar_opened = {}  # Track which mobiles we've opened health bars for

    def _get_distance(self, serial: int) -> float:
        """Calculate distance to a mobile."""
        try:
            # Check cache first
            cached_data = self._get_cached_mobile_data(serial)
            if cached_data and 'distance' in cached_data:
                return cached_data['distance']
            
            mobile = Mobiles.FindBySerial(serial)
            if mobile and hasattr(mobile, 'Position'):
                dx = Player.Position.X - mobile.Position.X
                dy = Player.Position.Y - mobile.Position.Y
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Cache the result
                self._cache_mobile_data(serial, {'distance': distance})
                return distance
        except AttributeError as e:
            Logger.debug(f"Position data unavailable for mobile {serial}: {e}")
        except Exception as e:
            Logger.debug(f"Error calculating distance to {serial}: {e}")
        return float('inf')

    def _is_valid_target(self, mobile) -> bool:
        """Check if a mobile is a valid combat target."""
        try:
            # Get combat settings
            ignore_innocents = self.config_manager.get_combat_setting('target_selection.ignore_innocents')
            ignore_pets = self.config_manager.get_combat_setting('target_selection.ignore_pets')
            allow_target_blues = self.config_manager.get_combat_setting('target_selection.allow_target_blues')
            max_range = self.config_manager.get_combat_setting('target_selection.max_range')
            
            # Basic checks
            if not mobile or mobile.Serial == Player.Serial:
                return False
            
            # UO Health Data Quirk Handling:
            # Many mobiles don't populate .Hits until health bar is opened
            # We should NOT reject targets with unpopulated health data (Hits = 0 or missing)
            # Only reject if we're confident the mobile is actually dead
            
            # Don't be too strict about health - many alive mobs show 0 hits until health bar is opened
            # Only reject if we have strong evidence the mobile is actually dead
            if hasattr(mobile, 'Hits') and mobile.Hits < 0:
                # Negative health definitely means dead
                return False
            
            # Check distance
            distance = self._get_distance(mobile.Serial)
            if distance > max_range:
                return False
            
            # Check notoriety (color coding in UO)
            # 1 = Innocent (blue), 2 = Friend (green), 3 = Gray (can be attacked), 
            # 4 = Criminal (gray), 5 = Orange (aggressive), 6 = Red (murderer), 7 = Invulnerable
            
            # Handle blue (innocent) targets based on configuration
            if mobile.Notoriety == 1:  # Blue (innocent)
                if not allow_target_blues:
                    Logger.debug(f"Skipping blue mobile {mobile.Serial} - allow_target_blues is disabled")
                    return False
                else:
                    Logger.debug(f"Allowing blue mobile {mobile.Serial} - allow_target_blues is enabled")
            
            # Always skip friends (green) - these are typically player allies
            if mobile.Notoriety == 2:  # Green (friend)
                Logger.debug(f"Skipping friend mobile {mobile.Serial} with notoriety {mobile.Notoriety}")
                return False
            
            # Skip yellow (5) - these are often neutral NPCs that shouldn't be targeted
            if mobile.Notoriety == 5:  # Yellow (orange/aggressive but often neutral)
                Logger.debug(f"Skipping yellow mobile {mobile.Serial} with notoriety {mobile.Notoriety} (neutral NPC)")
                return False
                
            # Skip invulnerable (7) - can't be attacked anyway
            if mobile.Notoriety == 7:  # Invulnerable
                Logger.debug(f"Skipping invulnerable mobile {mobile.Serial} with notoriety {mobile.Notoriety}")
                return False
            
            # Allow gray (3), criminal (4), and red (6) - these are always valid targets
            if mobile.Notoriety in [3, 4, 6]:
                Logger.debug(f"Valid target mobile {mobile.Serial} with notoriety {mobile.Notoriety}")
            
            # Basic pet check - pets usually have certain naming patterns or are controlled
            if ignore_pets:
                # This is a simplified check - in practice you might need more sophisticated pet detection
                name = getattr(mobile, 'Name', '').lower()
                if any(pet_word in name for pet_word in ['pet', 'follower', 'companion']):
                    return False
            
            return True
            
        except Exception as e:
            Logger.debug(f"Error validating target {mobile.Serial}: {e}")
            return False

    def detect_targets(self) -> List[Dict]:
        """Detect nearby hostile targets. Returns a list of target info dicts."""
        targets = []
        
        try:
            # Check if enough time has passed since last scan using adaptive timing
            current_time = time.time() * 1000  # Convert to milliseconds
            scan_interval = self._get_adaptive_scan_interval()
            
            # Skip interval check if this is the first scan (last_target_scan == 0)
            if self.last_target_scan > 0 and current_time - self.last_target_scan < scan_interval:
                Logger.debug(f"Target scan on cooldown - {scan_interval - (current_time - self.last_target_scan):.0f}ms remaining")
                return targets
            
            self.last_target_scan = current_time
            
            max_range = self.config_manager.get_combat_setting('target_selection.max_range')
            Logger.debug(f"Scanning for targets within {max_range} tiles...")
            
            # Get all mobiles using Filter (RazorEnhanced API)
            mobile_filter = Mobiles.Filter()
            mobile_filter.Enabled = True
            mobile_filter.RangeMax = max_range * 2  # Use larger range for initial filtering
            mobiles_list = Mobiles.ApplyFilter(mobile_filter)
            
            for mobile in mobiles_list:
                if self._is_valid_target(mobile):
                    distance = self._get_distance(mobile.Serial)
                    
                    # PERFORMANCE OPTIMIZATION: Don't open health bars for all targets during scanning
                    # Only get basic info here - we'll open health bar when we actually select a target
                    hits = getattr(mobile, 'Hits', 0)
                    hits_max = getattr(mobile, 'HitsMax', hits if hits > 0 else 100)  # Default to 100 if unknown
                    
                    target_info = {
                        'serial': mobile.Serial,
                        'name': getattr(mobile, 'Name', 'Unknown'),
                        'hits': hits,
                        'hits_max': hits_max,
                        'distance': distance,
                        'notoriety': mobile.Notoriety,
                        'health_bar_opened': False,  # Track if we've opened the health bar
                        'position': {
                            'x': mobile.Position.X,
                            'y': mobile.Position.Y,
                            'z': mobile.Position.Z
                        }
                    }
                    targets.append(target_info)
            
            if targets:
                Logger.debug(f"Found {len(targets)} valid targets")
            
        except Exception as e:
            Logger.error(f"Error detecting targets: {e}")
        
        return targets

    def select_target(self, targets: List[Dict]) -> Optional[Dict]:
        """Select a target based on priority with smart engagement logic."""
        if not targets:
            return None
        
        try:
            priority_mode = self.config_manager.get_combat_setting('target_selection.priority_mode')
            
            # ENHANCED TARGET SELECTION: Prioritize currently engaged target
            # If we have a current target and it's still valid, keep fighting it unless there's a much better option
            if self.current_target:
                current_serial = self.current_target['serial']
                # Check if current target is still in the available targets list
                current_target_updated = None
                for target in targets:
                    if target['serial'] == current_serial:
                        current_target_updated = target
                        break
                
                if current_target_updated:
                    # Current target is still valid and in range
                    Logger.debug(f"Continuing engagement with current target: {current_target_updated['name']}")
                    
                    # Only switch if there's a SIGNIFICANTLY better target (much closer)
                    # This prevents target bouncing and improves combat efficiency
                    if len(targets) > 1:
                        other_targets = [t for t in targets if t['serial'] != current_serial]
                        if other_targets:
                            closest_other = min(other_targets, key=lambda t: t['distance'])
                            current_distance = current_target_updated['distance']
                            closest_distance = closest_other['distance']
                            
                            # Only switch if the other target is MUCH closer (more than 3 tiles difference)
                            switch_threshold = 3.0
                            if current_distance - closest_distance > switch_threshold:
                                Logger.info(f"Switching target: {closest_other['name']} is {current_distance - closest_distance:.1f} tiles closer")
                                return closest_other
                    
                    return current_target_updated
                else:
                    Logger.debug("Current target no longer available, selecting new target")
            
            # No current target or current target lost - select best available target
            if priority_mode == 'closest':
                # Sort by distance, closest first
                targets.sort(key=lambda t: t['distance'])
                selected = targets[0]
                Logger.debug(f"Selected closest target: {selected['name']} at {selected['distance']:.1f} tiles")
                return selected
            
            elif priority_mode == 'lowest_health':
                # Sort by health percentage, lowest first
                targets.sort(key=lambda t: t['hits'] / max(t['hits_max'], 1))
                selected = targets[0]
                health_pct = (selected['hits'] / max(selected['hits_max'], 1)) * 100
                Logger.debug(f"Selected lowest health target: {selected['name']} at {health_pct:.1f}% health")
                return selected
            
            elif priority_mode == 'highest_threat':
                # Sort by combination of closeness and health (closer + more health = higher threat)
                def threat_score(target):
                    health_ratio = target['hits'] / max(target['hits_max'], 1)
                    distance_factor = 1.0 / max(target['distance'], 0.1)  # Avoid division by zero
                    return health_ratio * distance_factor
                
                targets.sort(key=threat_score, reverse=True)
                selected = targets[0]
                Logger.debug(f"Selected highest threat target: {selected['name']}")
                return selected
            
            else:
                # Default to closest
                targets.sort(key=lambda t: t['distance'])
                selected = targets[0]
                Logger.debug(f"Selected target (default closest): {selected['name']} at {selected['distance']:.1f} tiles")
                return selected
                
        except Exception as e:
            Logger.error(f"Error selecting target: {e}")
            return targets[0] if targets else None

    def engage_target(self, target: Dict) -> bool:
        """Engage the selected target with the currently equipped weapon."""
        try:
            # Check if auto attack is enabled
            auto_attack_enabled = self.config_manager.get_combat_setting('system_toggles.auto_attack_enabled')
            if not auto_attack_enabled:
                Logger.debug("Auto attack disabled - setting target but not attacking")
                # Still set the target for manual combat
                Target.SetLast(target['serial'])
                return True
            
            current_time = time.time() * 1000  # Convert to milliseconds
            attack_delay = self.config_manager.get_combat_setting('combat_behavior.attack_delay_ms')
            
            Logger.debug(f"Engage target - Current time: {current_time:.0f}, Last attack: {self.last_attack_time:.0f}, Attack delay: {attack_delay}ms")
            
            # Be more aggressive - allow immediate attacks in more cases
            should_attack = False
            
            if self.last_attack_time == 0:
                # First attack ever - always immediate
                should_attack = True
                Logger.debug("First attack - immediate engagement allowed")
            elif self.current_target and self.current_target['serial'] != target['serial']:
                # Switching targets - immediate attack allowed
                should_attack = True
                Logger.debug("Target switch - immediate engagement allowed")
            elif current_time - self.last_attack_time >= attack_delay:
                # Normal attack delay has passed
                should_attack = True
                Logger.debug(f"Attack delay passed ({current_time - self.last_attack_time:.0f}ms >= {attack_delay}ms)")
            else:
                Logger.debug(f"Attack on cooldown - {attack_delay - (current_time - self.last_attack_time):.0f}ms remaining")
            
            if not should_attack:
                # Still set target even if we're not attacking yet
                Target.SetLast(target['serial'])
                return False
            
            # Set the target and attack
            Target.SetLast(target['serial'])
            
            # Ensure health bar is open for accurate health tracking
            if self.last_attack_time == 0 or (self.current_target and self.current_target['serial'] != target['serial']):
                self._ensure_health_bar(target['serial'])
            
            # Start combat if not already in combat or switching targets
            if not self.combat_start_time or (self.current_target and self.current_target['serial'] != target['serial']):
                self.combat_start_time = current_time
                Logger.info(f"Engaging target: {target['name']} (Distance: {target['distance']:.1f})")
            
            # Attack the target (only if auto attack is enabled)
            Player.Attack(target['serial'])
            self.last_attack_time = current_time
            
            return True
            
        except Exception as e:
            Logger.error(f"Error engaging target {target.get('name', 'Unknown')}: {e}")
            return False

    def monitor_combat(self, target: Dict) -> bool:
        """Monitor combat status (target dead, player attacked, etc.)."""
        try:
            # Check if target still exists and is alive
            mobile = Mobiles.FindBySerial(target['serial'])
            if not mobile or mobile.Hits <= 0:
                Logger.info(f"Target {target['name']} is dead or gone")
                self.disengage()
                return False
            
            # Display target name overhead if enabled and player is in war mode
            if Player.WarMode:
                # Update target health info for display
                hits = getattr(mobile, 'Hits', target.get('hits', 0))
                hits_max = getattr(mobile, 'HitsMax', target.get('hits_max', hits if hits > 0 else 100))
                
                # Update target info with current health
                target['hits'] = hits
                target['hits_max'] = hits_max
                
                # Show target name overhead
                self._display_target_name_overhead(target)
            
            # Check combat timeout
            if self.combat_start_time:
                current_time = time.time() * 1000  # Convert to milliseconds
                timeout = self.config_manager.get_combat_setting('combat_behavior.combat_timeout_ms')
                if current_time - self.combat_start_time > timeout:
                    Logger.warning(f"Combat timeout reached for {target['name']}")
                    self.disengage()
                    return False
            
            # Check if we should retreat due to low health
            retreat_on_low_health = self.config_manager.get_combat_setting('combat_behavior.retreat_on_low_health')
            if retreat_on_low_health:
                health_threshold = self.config_manager.get_combat_setting('combat_behavior.retreat_health_threshold')
                health_percentage = (Player.Hits / Player.HitsMax) * 100
                
                if health_percentage < health_threshold:
                    Logger.warning(f"Health too low ({health_percentage:.1f}%), retreating from combat")
                    self.disengage()
                    return False
            
            # Check if target is still in range
            distance = self._get_distance(target['serial'])
            max_range = self.config_manager.get_combat_setting('target_selection.max_range')
            if distance > max_range * 1.5:  # Allow some buffer
                Logger.info(f"Target {target['name']} moved out of range")
                self.disengage()
                return False
            
            return True
            
        except Exception as e:
            Logger.error(f"Error monitoring combat: {e}")
            return False

    def disengage(self):
        """Disengage or switch targets as needed."""
        try:
            if self.current_target:
                Logger.debug(f"Disengaging from {self.current_target.get('name', 'Unknown')}")
            
            self.current_target = None
            self.combat_start_time = None
            
            # Clear target
            Target.Cancel()
            
        except Exception as e:
            Logger.error(f"Error disengaging: {e}")

    def run(self):
        """Main entry point for the combat system (to be called in main loop)."""
        system_start_time = time.time()
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        try:
            # Check if combat system is enabled
            if not self.config_manager.get_combat_setting('system_toggles.combat_system_enabled'):
                Logger.debug(f"COMBAT [{timestamp}]: System disabled - skipping combat logic")
                return
            
            # Safety checks
            if Player.IsGhost or not Player.Visible:
                if self.current_target:
                    Logger.debug(f"COMBAT [{timestamp}]: Player is ghost or invisible - disengaging from combat")
                    self.disengage()
                return
            
            # WAR MODE CHECK: Only engage in combat when player is in war mode
            if not Player.WarMode:
                # If player exits war mode while fighting, disengage current target
                if self.current_target:
                    Logger.info(f"COMBAT [{timestamp}]: Player exited war mode - disengaging from combat")
                    self.disengage()
                else:
                    Logger.debug(f"COMBAT [{timestamp}]: Player not in war mode - combat system inactive")
                return
            
            # Check if we should retreat due to low health first
            health_check_start = time.time()
            retreat_on_low_health = self.config_manager.get_combat_setting('combat_behavior.retreat_on_low_health')
            if retreat_on_low_health:
                health_threshold = self.config_manager.get_combat_setting('combat_behavior.retreat_health_threshold')
                health_percentage = (Player.Hits / Player.HitsMax) * 100
                
                Logger.debug(f"COMBAT [{timestamp}]: Health check: {health_percentage:.1f}% (retreat threshold: {health_threshold}%)")
                
                if health_percentage < health_threshold:
                    if self.current_target:
                        Logger.warning(f"COMBAT [{timestamp}]: Health too low ({health_percentage:.1f}%), retreating from combat")
                        self.disengage()
                    return
            health_check_duration = (time.time() - health_check_start) * 1000
            
            # Check Auto Target and Auto Attack settings
            settings_check_start = time.time()
            auto_target_enabled = self.config_manager.get_combat_setting('system_toggles.auto_target_enabled')
            auto_attack_enabled = self.config_manager.get_combat_setting('system_toggles.auto_attack_enabled')
            settings_check_duration = (time.time() - settings_check_start) * 1000
            
            Logger.debug(f"COMBAT [{timestamp}]: Settings - Auto Target: {auto_target_enabled}, Auto Attack: {auto_attack_enabled}")
            
            # If we have a current target, continue monitoring
            if self.current_target:
                monitor_start = time.time()
                Logger.debug(f"COMBAT [{timestamp}]: Monitoring current target: {self.current_target.get('name', 'Unknown')} ({self.current_target.get('serial', 'N/A')})")
                if not self.monitor_combat(self.current_target):
                    # Target lost, disengage already called in monitor_combat
                    monitor_duration = (time.time() - monitor_start) * 1000
                    Logger.debug(f"COMBAT [{timestamp}]: Target monitoring completed in {monitor_duration:.1f}ms (target lost)")
                    return
                monitor_duration = (time.time() - monitor_start) * 1000
                Logger.debug(f"COMBAT [{timestamp}]: Target monitoring completed in {monitor_duration:.1f}ms")
                
                # Only continue attacking if auto attack is enabled
                if auto_attack_enabled:
                    self.engage_target(self.current_target)
                else:
                    Logger.debug("Auto attack disabled - not attacking current target")
                return
            
            # Only look for new targets if auto targeting is enabled
            if auto_target_enabled:
                Logger.debug("Scanning for new targets...")
                targets = self.detect_targets()
                target = self.select_target(targets)
                
                if target:
                    self.current_target = target
                    Logger.info(f"Auto target selected: {target['name']} (Distance: {target['distance']:.1f})")
                    Logger.debug(f"Target details - Serial: {target['serial']}, Health: {target.get('hits', 'Unknown')}/{target.get('hits_max', 'Unknown')}, Notoriety: {target.get('notoriety', 'Unknown')}")
                    
                    # Only engage if auto attack is also enabled
                    if auto_attack_enabled:
                        if not self.engage_target(target):
                            self.disengage()
                    else:
                        Logger.debug("Auto attack disabled - target selected but not attacking")
                else:
                    Logger.debug("No valid targets found")
            else:
                Logger.debug("Auto targeting disabled - not scanning for new targets")
            
            # Log performance timing
            system_duration = (time.time() - system_start_time) * 1000
            end_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            if system_duration > 500:  # More than 500ms
                Logger.warning(f"COMBAT [{end_timestamp}]: System took {system_duration:.1f}ms - performance issue!")
            elif system_duration > 200:  # More than 200ms
                Logger.debug(f"COMBAT [{end_timestamp}]: System took {system_duration:.1f}ms - monitor performance")
            else:
                Logger.debug(f"COMBAT [{end_timestamp}]: System completed in {system_duration:.1f}ms")
            
        except Exception as e:
            system_duration = (time.time() - system_start_time) * 1000
            Logger.error(f"COMBAT: Error in combat system run after {system_duration:.1f}ms: {e}")
            self.disengage()

    def _ensure_health_bar(self, mobile_serial: int) -> None:
        """Ensure health bar is open for a mobile to get accurate health data."""
        try:
            # Open health bar to get accurate health information
            # This is needed because many mobiles don't populate health data until their bar is opened
            mobile = Mobiles.FindBySerial(mobile_serial)
            if mobile:
                # The most reliable way to populate health data is to single-click the mobile
                # This opens their health bar and populates the health information
                Target.SetLast(mobile_serial)
                # Give a small pause to let the data populate
                Misc.Pause(50)  # Slightly longer pause to ensure data updates
                Logger.debug(f"Opened health bar for {getattr(mobile, 'Name', 'Unknown')} ({mobile_serial})")
        except Exception as e:
            Logger.debug(f"Error opening health bar for {mobile_serial}: {e}")

    def _display_target_name_overhead(self, target: Dict) -> None:
        """Display the target's name above its head."""
        try:
            # Check if target name display is enabled
            show_target_name = self.config_manager.get_combat_setting('display_settings.show_target_name_overhead')
            if not show_target_name:
                return
            
            current_time = time.time() * 1000  # Convert to milliseconds
            display_interval = self.config_manager.get_combat_setting('display_settings.target_name_display_interval_ms')
            
            # Check if enough time has passed since last display
            if current_time - self.last_target_name_display < display_interval:
                return
            
            self.last_target_name_display = current_time
            
            # Get display color setting
            display_color = self.config_manager.get_combat_setting('display_settings.target_name_display_color')
            
            # Find the mobile to display the name over
            mobile = Mobiles.FindBySerial(target['serial'])
            if mobile:
                target_name = target.get('name', 'Unknown')
                
                # Format as [NAME - HP PERCENT]
                if target.get('hits', 0) > 0 and target.get('hits_max', 0) > 0:
                    health_percentage = (target['hits'] / target['hits_max']) * 100
                    display_text = f"[{target_name} - {health_percentage:.0f}%]"
                else:
                    # If health data unavailable, show just the name
                    display_text = f"[{target_name}]"
                
                # Use Mobiles.Message to display text overhead the target
                # This is the proper RazorEnhanced API method for overhead messages on mobiles
                try:
                    # Display message above the target mobile
                    Mobiles.Message(target['serial'], display_color, display_text)
                    Logger.debug(f"Displayed target name overhead: {display_text}")
                except Exception as msg_error:
                    # Fallback to player message if overhead message fails
                    try:
                        Misc.SendMessage(f"Current Target: {display_text}", display_color)
                        Logger.debug(f"Displayed target name to player: {display_text}")
                    except Exception as fallback_error:
                        Logger.debug(f"Failed to display target message: {fallback_error}")
            
        except Exception as e:
            Logger.debug(f"Error displaying target name overhead: {e}")

    def _get_cached_mobile_data(self, serial: int) -> Optional[Dict]:
        """Get cached mobile data if still valid."""
        current_time = time.time() * 1000
        if serial in self.mobile_cache:
            cache_entry = self.mobile_cache[serial]
            if current_time - cache_entry['timestamp'] < self.cache_duration:
                return cache_entry['data']
            else:
                # Clean up expired cache entry
                del self.mobile_cache[serial]
        return None

    def _cache_mobile_data(self, serial: int, data: Dict) -> None:
        """Cache mobile data with timestamp."""
        current_time = time.time() * 1000
        if serial not in self.mobile_cache:
            self.mobile_cache[serial] = {'data': {}, 'timestamp': current_time}
        
        # Update data while preserving existing cached data
        self.mobile_cache[serial]['data'].update(data)
        self.mobile_cache[serial]['timestamp'] = current_time

    def _get_adaptive_scan_interval(self) -> int:
        """Get adaptive scan interval based on combat state."""
        base_interval = self.config_manager.get_combat_setting('timing_settings.target_scan_interval')
        if not self.current_target:
            return max(base_interval // 3, 100)  # Minimum 100ms when looking for targets
        elif self.current_target and self.current_target.get('hits', 0) > self.current_target.get('hits_max', 1) * 0.8:
            return base_interval * 2  # Slower when target is healthy
        return base_interval

def execute_combat_system(config_manager: ConfigManager):
    """
    Execute the Combat System - main entry point for integration with main bot loop.
    """
    # Create a static instance to maintain state across calls
    if not hasattr(execute_combat_system, 'combat_system'):
        execute_combat_system.combat_system = CombatSystem(config_manager)
    
    execute_combat_system.combat_system.run()
