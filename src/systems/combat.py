"""
Combat System Module for DexBot
Automates engaging and defeating enemies with smart target selection and combat monitoring.
"""

import math
import time
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

    def _get_distance(self, serial: int) -> float:
        """Calculate distance to a mobile."""
        try:
            mobile = Mobiles.FindBySerial(serial)
            if mobile:
                dx = Player.Position.X - mobile.Position.X
                dy = Player.Position.Y - mobile.Position.Y
                return math.sqrt(dx * dx + dy * dy)
        except:
            pass
        return float('inf')

    def _is_valid_target(self, mobile) -> bool:
        """Check if a mobile is a valid combat target."""
        try:
            # Get combat settings
            ignore_innocents = self.config_manager.get_combat_setting('target_selection.ignore_innocents')
            ignore_pets = self.config_manager.get_combat_setting('target_selection.ignore_pets')
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
            # 1 = Innocent (blue), 2 = Friend (green), 3 = Gray, 4 = Criminal (gray), 5 = Orange, 6 = Red, 7 = Invulnerable
            if ignore_innocents and mobile.Notoriety in [1, 2]:  # Skip innocents and friends
                return False
            
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
            # Check if enough time has passed since last scan (but be more aggressive when no target)
            current_time = time.time() * 1000  # Convert to milliseconds
            scan_interval = self.config_manager.get_combat_setting('timing_settings.target_scan_interval')
            
            # Use faster scanning when we don't have a current target (aggressive mode)
            if not self.current_target:
                scan_interval = scan_interval // 2  # Half the scan interval when looking for targets
            
            # Skip interval check if this is the first scan (last_target_scan == 0)
            if self.last_target_scan > 0 and current_time - self.last_target_scan < scan_interval:
                return targets
            
            self.last_target_scan = current_time
            
            max_range = self.config_manager.get_combat_setting('target_selection.max_range')
            
            # Get all mobiles using Filter (RazorEnhanced API)
            mobile_filter = Mobiles.Filter()
            mobile_filter.Enabled = True
            mobile_filter.RangeMax = max_range * 2  # Use larger range for initial filtering
            mobiles_list = Mobiles.ApplyFilter(mobile_filter)
            
            for mobile in mobiles_list:
                if self._is_valid_target(mobile):
                    distance = self._get_distance(mobile.Serial)
                    
                    # For new potential targets, ensure health bar is opened to get accurate data
                    # This helps with the UO quirk where health data isn't populated until health bar is opened
                    if not self.current_target or self.current_target['serial'] != mobile.Serial:
                        self._ensure_health_bar(mobile.Serial)
                    
                    # Handle cases where health info might not be available (even after opening health bar)
                    hits = getattr(mobile, 'Hits', 0)
                    hits_max = getattr(mobile, 'HitsMax', hits if hits > 0 else 100)  # Default to 100 if unknown
                    
                    target_info = {
                        'serial': mobile.Serial,
                        'name': getattr(mobile, 'Name', 'Unknown'),
                        'hits': hits,
                        'hits_max': hits_max,
                        'distance': distance,
                        'notoriety': mobile.Notoriety,
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
        """Select a target based on priority (e.g., closest, lowest health)."""
        if not targets:
            return None
        
        try:
            priority_mode = self.config_manager.get_combat_setting('target_selection.priority_mode')
            
            if priority_mode == 'closest':
                # Sort by distance, closest first
                targets.sort(key=lambda t: t['distance'])
                return targets[0]
            
            elif priority_mode == 'lowest_health':
                # Sort by health percentage, lowest first
                targets.sort(key=lambda t: t['hits'] / max(t['hits_max'], 1))
                return targets[0]
            
            elif priority_mode == 'highest_threat':
                # Sort by combination of closeness and health (closer + more health = higher threat)
                def threat_score(target):
                    health_ratio = target['hits'] / max(target['hits_max'], 1)
                    distance_factor = 1.0 / max(target['distance'], 0.1)  # Avoid division by zero
                    return health_ratio * distance_factor
                
                targets.sort(key=threat_score, reverse=True)
                return targets[0]
            
            else:
                # Default to closest
                targets.sort(key=lambda t: t['distance'])
                return targets[0]
                
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
            
            # Be more aggressive - allow immediate attacks in more cases
            should_attack = False
            
            if self.last_attack_time == 0:
                # First attack ever - always immediate
                should_attack = True
            elif self.current_target and self.current_target['serial'] != target['serial']:
                # Switching targets - immediate attack allowed
                should_attack = True
            elif current_time - self.last_attack_time >= attack_delay:
                # Normal attack delay has passed
                should_attack = True
            
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
        try:
            # Check if combat system is enabled
            if not self.config_manager.get_combat_setting('system_toggles.combat_system_enabled'):
                return
            
            # Safety checks
            if Player.IsGhost or not Player.Visible:
                if self.current_target:
                    self.disengage()
                return
            
            # WAR MODE CHECK: Only engage in combat when player is in war mode
            if not Player.WarMode:
                # If player exits war mode while fighting, disengage current target
                if self.current_target:
                    Logger.info("Player exited war mode - disengaging from combat")
                    self.disengage()
                return
            
            # Check if we should retreat due to low health first
            retreat_on_low_health = self.config_manager.get_combat_setting('combat_behavior.retreat_on_low_health')
            if retreat_on_low_health:
                health_threshold = self.config_manager.get_combat_setting('combat_behavior.retreat_health_threshold')
                health_percentage = (Player.Hits / Player.HitsMax) * 100
                
                if health_percentage < health_threshold:
                    if self.current_target:
                        Logger.warning(f"Health too low ({health_percentage:.1f}%), retreating from combat")
                        self.disengage()
                    return
            
            # Check Auto Target and Auto Attack settings
            auto_target_enabled = self.config_manager.get_combat_setting('system_toggles.auto_target_enabled')
            auto_attack_enabled = self.config_manager.get_combat_setting('system_toggles.auto_attack_enabled')
            
            # If we have a current target, continue monitoring
            if self.current_target:
                if not self.monitor_combat(self.current_target):
                    # Target lost, disengage already called in monitor_combat
                    return
                
                # Only continue attacking if auto attack is enabled
                if auto_attack_enabled:
                    self.engage_target(self.current_target)
                else:
                    Logger.debug("Auto attack disabled - not attacking current target")
                return
            
            # Only look for new targets if auto targeting is enabled
            if auto_target_enabled:
                targets = self.detect_targets()
                target = self.select_target(targets)
                
                if target:
                    self.current_target = target
                    Logger.info(f"Auto target selected: {target['name']} (Distance: {target['distance']:.1f})")
                    
                    # Only engage if auto attack is also enabled
                    if auto_attack_enabled:
                        if not self.engage_target(target):
                            self.disengage()
                    else:
                        Logger.debug("Auto attack disabled - target selected but not attacking")
            else:
                Logger.debug("Auto targeting disabled - not scanning for new targets")
            
        except Exception as e:
            Logger.error(f"Error in combat system run: {e}")
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

def execute_combat_system(config_manager: ConfigManager):
    """
    Execute the Combat System - main entry point for integration with main bot loop.
    """
    # Create a static instance to maintain state across calls
    if not hasattr(execute_combat_system, 'combat_system'):
        execute_combat_system.combat_system = CombatSystem(config_manager)
    
    execute_combat_system.combat_system.run()
