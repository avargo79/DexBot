"""
Combat System Module for DexBot
Automates engaging and defeating enemies with smart target selection and combat monitoring.
"""

import math
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
            
            # Check if mobile is dead
            if mobile.Hits <= 0:
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
            # Check if enough time has passed since last scan
            current_time = Timer.Get()
            scan_interval = self.config_manager.get_combat_setting('timing_settings.target_scan_interval')
            
            if current_time - self.last_target_scan < scan_interval:
                return targets
            
            self.last_target_scan = current_time
            
            max_range = self.config_manager.get_combat_setting('target_selection.max_range')
            
            # Get all mobiles in range
            mobiles_list = Mobiles.Filter()
            
            for mobile in mobiles_list:
                if self._is_valid_target(mobile):
                    distance = self._get_distance(mobile.Serial)
                    
                    target_info = {
                        'serial': mobile.Serial,
                        'name': getattr(mobile, 'Name', 'Unknown'),
                        'hits': mobile.Hits,
                        'hits_max': getattr(mobile, 'HitsMax', mobile.Hits),
                        'distance': distance,
                        'notoriety': mobile.Notoriety,
                        'position': {
                            'x': mobile.Position.X,
                            'y': mobile.Position.Y,
                            'z': mobile.Position.Z
                        }
                    }
                    targets.append(target_info)
            
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
            current_time = Timer.Get()
            attack_delay = self.config_manager.get_combat_setting('combat_behavior.attack_delay_ms')
            
            # Check attack delay
            if current_time - self.last_attack_time < attack_delay:
                return False
            
            # Set the target and attack
            Target.SetLast(target['serial'])
            
            # Start combat if not already in combat
            if not self.combat_start_time:
                self.combat_start_time = current_time
                Logger.info(f"Engaging target: {target['name']} (Distance: {target['distance']:.1f})")
            
            # Attack the target
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
            
            # Check combat timeout
            if self.combat_start_time:
                current_time = Timer.Get()
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
            
            # If we have a current target, continue monitoring
            if self.current_target:
                if not self.monitor_combat(self.current_target):
                    # Target lost, disengage already called in monitor_combat
                    return
                
                # Continue attacking current target
                self.engage_target(self.current_target)
                return
            
            # No current target, look for new ones
            targets = self.detect_targets()
            target = self.select_target(targets)
            
            if target:
                self.current_target = target
                if not self.engage_target(target):
                    self.disengage()
            
        except Exception as e:
            Logger.error(f"Error in combat system run: {e}")
            self.disengage()


def execute_combat_system(config_manager: ConfigManager):
    """
    Execute the Combat System - main entry point for integration with main bot loop.
    """
    # Create a static instance to maintain state across calls
    if not hasattr(execute_combat_system, 'combat_system'):
        execute_combat_system.combat_system = CombatSystem(config_manager)
    
    execute_combat_system.combat_system.run()
