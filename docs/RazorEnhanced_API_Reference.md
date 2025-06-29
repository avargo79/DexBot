# RazorEnhanced API Reference Guide

> **Generated on**: 2025-06-29 12:32:25
> 
> This comprehensive API reference guide was automatically generated from the official
> RazorEnhanced documentation. It provides detailed information about modules, methods,
> parameters, and usage examples for developers.
> 
> **Official Documentation**: [https://razorenhanced.github.io/doc/api/](https://razorenhanced.github.io/doc/api/)

## Overview

RazorEnhanced is a powerful scripting framework for Ultima Online that provides extensive
APIs for automating gameplay, creating tools, and enhancing the user experience.

This guide includes:
- **Complete API coverage** - Core modules and their methods/properties
- **Method signatures** - Parameter details and return types
- **Usage examples** - Practical code examples for each API
- **Best practices** - Error handling and implementation patterns
- **Quick reference** - Common patterns and imports

## Table of Contents

- [Quick Reference](#quick-reference)
- [Player](#player)
- [Items](#items)
- [Target](#target)
- [Journal](#journal)
- [Misc](#misc)
- [Best Practices](#best-practices)
- [Additional Resources](#additional-resources)

## Quick Reference

### Import RazorEnhanced
```python
# Method 1: Import specific modules
from RazorEnhanced import Player, Items, Target, Journal

# Method 2: Import with CLR (recommended for stability)
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Player, Items, Target

# Method 3: Import with alias
import RazorEnhanced as RE
# Usage: RE.Player.Name, RE.Items.FindBySerial(), etc.
```

### Essential Patterns

#### Basic Script Structure
```python
from RazorEnhanced import Player, Items, Misc

def main():
    try:
        # Your script logic here
        Misc.SendMessage("Script started", 0x40)
        
        # Check player status
        if Player.IsGhost:
            Misc.SendMessage("Player is dead, stopping script", 0x20)
            return
            
        # Your automation logic here
        
    except Exception as e:
        Misc.SendMessage(f"Script error: {e}", 0x20)

if __name__ == "__main__":
    main()
```

#### Error Handling Template
```python
def safe_operation():
    try:
        # Potentially risky operation
        item = Items.FindBySerial(0x12345678)
        if item is None:
            raise ValueError("Item not found")
            
        # Process the item
        Items.Move(item.Serial, Player.Backpack.Serial, 1)
        
        return True
        
    except Exception as e:
        Misc.SendMessage(f"Operation failed: {e}", 0x20)
        return False
```

## Items

> **Import**: `from RazorEnhanced import Items`

Handles item manipulation, searching, and container operations.

### Properties

#### `Items.Name`

Gets the name value

**Example**:
```python
from RazorEnhanced import Items

# Get name value
value = Items.Name
print(f"Name: {value}")
```
#### `Items.Serial`

Gets the serial value

**Example**:
```python
from RazorEnhanced import Items

# Get serial value
value = Items.Serial
print(f"Serial: {value}")
```
### Methods

#### `Items.ApplyFilter`

**Signature**: `ApplyFilter(filter)`

Method for ApplyFilter operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use ApplyFilter method
try:
    result = Items.ApplyFilter(filter)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.ApplyFilter`

**Signature**: `ApplyFilter(filter)`

Method for ApplyFilter operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use ApplyFilter method
try:
    result = Items.ApplyFilter(filter)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.BackpackCount`

**Signature**: `BackpackCount(itemid, color)`

Method for BackpackCount operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use BackpackCount method
try:
    result = Items.BackpackCount(itemid, color)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.BackpackCount`

**Signature**: `BackpackCount(itemid, color)`

Method for BackpackCount operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use BackpackCount method
try:
    result = Items.BackpackCount(itemid, color)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.ChangeDyeingTubColor`

**Signature**: `ChangeDyeingTubColor(dyes, dyeingTub, color)`

Method for ChangeDyeingTubColor operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use ChangeDyeingTubColor method
try:
    result = Items.ChangeDyeingTubColor(dyes, dyeingTub, color)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.ChangeDyeingTubColor`

**Signature**: `ChangeDyeingTubColor(dyes, dyeingTub, color)`

Method for ChangeDyeingTubColor operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use ChangeDyeingTubColor method
try:
    result = Items.ChangeDyeingTubColor(dyes, dyeingTub, color)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.Close`

**Signature**: `Close(serial)`

Method for Close operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use Close method
try:
    result = Items.Close(serial)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.Close`

**Signature**: `Close(serial)`

Method for Close operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use Close method
try:
    result = Items.Close(serial)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.ContainerCount`

**Signature**: `ContainerCount(container, itemid, color, recursive)`

Method for ContainerCount operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use ContainerCount method
try:
    result = Items.ContainerCount(container, itemid, color, recursive)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Items.ContainerCount`

**Signature**: `ContainerCount(container, itemid, color, recursive)`

Method for ContainerCount operations

**Example**:
```python
from RazorEnhanced import Items, Misc

# Use ContainerCount method
try:
    result = Items.ContainerCount(container, itemid, color, recursive)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
---

## Journal

> **Import**: `from RazorEnhanced import Journal`

Monitors and searches game messages and journal entries.

### Properties

#### `Journal.Name`

Gets the name value

**Example**:
```python
from RazorEnhanced import Journal

# Get name value
value = Journal.Name
print(f"Name: {value}")
```
#### `Journal.Serial`

Gets the serial value

**Example**:
```python
from RazorEnhanced import Journal

# Get serial value
value = Journal.Serial
print(f"Serial: {value}")
```
### Methods

#### `Journal.Clear`

**Signature**: `Clear(toBeRemoved)`

Method for Clear operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use Clear method
try:
    result = Journal.Clear(toBeRemoved)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.Clear`

**Signature**: `Clear(toBeRemoved)`

Method for Clear operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use Clear method
try:
    result = Journal.Clear(toBeRemoved)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.FilterText`

**Signature**: `FilterText(text)`

Method for FilterText operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use FilterText method
try:
    result = Journal.FilterText(text)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.FilterText`

**Signature**: `FilterText(text)`

Method for FilterText operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use FilterText method
try:
    result = Journal.FilterText(text)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.GetJournalEntry`

**Signature**: `GetJournalEntry(afterTimestap)`

Method for GetJournalEntry operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use GetJournalEntry method
try:
    result = Journal.GetJournalEntry(afterTimestap)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.GetJournalEntry`

**Signature**: `GetJournalEntry(afterTimestap)`

Method for GetJournalEntry operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use GetJournalEntry method
try:
    result = Journal.GetJournalEntry(afterTimestap)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.GetLineText`

**Signature**: `GetLineText(text, addname)`

Method for GetLineText operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use GetLineText method
try:
    result = Journal.GetLineText(text, addname)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.GetLineText`

**Signature**: `GetLineText(text, addname)`

Method for GetLineText operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use GetLineText method
try:
    result = Journal.GetLineText(text, addname)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.GetSpeechName`

**Signature**: `GetSpeechName()`

Method for GetSpeechName operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use GetSpeechName method
try:
    result = Journal.GetSpeechName()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Journal.GetSpeechName`

**Signature**: `GetSpeechName()`

Method for GetSpeechName operations

**Example**:
```python
from RazorEnhanced import Journal, Misc

# Use GetSpeechName method
try:
    result = Journal.GetSpeechName()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
---

## Misc

> **Import**: `from RazorEnhanced import Misc`

Provides miscellaneous utility functions and game operations.

### Properties

#### `Misc.Name`

Gets the name value

**Example**:
```python
from RazorEnhanced import Misc

# Get name value
value = Misc.Name
print(f"Name: {value}")
```
#### `Misc.Serial`

Gets the serial value

**Example**:
```python
from RazorEnhanced import Misc

# Get serial value
value = Misc.Serial
print(f"Serial: {value}")
```
#### `Misc.Position`

Gets the position value

**Example**:
```python
from RazorEnhanced import Misc

# Get position value
value = Misc.Position
print(f"Position: {value}")
```
#### `Misc.Status`

Gets the status value

**Example**:
```python
from RazorEnhanced import Misc

# Get status value
value = Misc.Status
print(f"Status: {value}")
```
### Methods

#### `Misc.AllSharedValue`

**Signature**: `AllSharedValue()`

Method for AllSharedValue operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use AllSharedValue method
try:
    result = Misc.AllSharedValue()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.AllSharedValue`

**Signature**: `AllSharedValue()`

Method for AllSharedValue operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use AllSharedValue method
try:
    result = Misc.AllSharedValue()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.AppendNotDupToFile`

**Signature**: `AppendNotDupToFile(fileName, lineOfData)`

Method for AppendNotDupToFile operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use AppendNotDupToFile method
try:
    result = Misc.AppendNotDupToFile(fileName, lineOfData)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.AppendNotDupToFile`

**Signature**: `AppendNotDupToFile(fileName, lineOfData)`

Method for AppendNotDupToFile operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use AppendNotDupToFile method
try:
    result = Misc.AppendNotDupToFile(fileName, lineOfData)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.AppendToFile`

**Signature**: `AppendToFile(fileName, lineOfData)`

Method for AppendToFile operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use AppendToFile method
try:
    result = Misc.AppendToFile(fileName, lineOfData)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.AppendToFile`

**Signature**: `AppendToFile(fileName, lineOfData)`

Method for AppendToFile operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use AppendToFile method
try:
    result = Misc.AppendToFile(fileName, lineOfData)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.Beep`

**Signature**: `Beep()`

Method for Beep operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use Beep method
try:
    result = Misc.Beep()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.Beep`

**Signature**: `Beep()`

Method for Beep operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use Beep method
try:
    result = Misc.Beep()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.CancelPrompt`

**Signature**: `CancelPrompt()`

Method for CancelPrompt operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use CancelPrompt method
try:
    result = Misc.CancelPrompt()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Misc.CancelPrompt`

**Signature**: `CancelPrompt()`

Method for CancelPrompt operations

**Example**:
```python
from RazorEnhanced import Misc, Misc

# Use CancelPrompt method
try:
    result = Misc.CancelPrompt()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
---

## Player

> **Import**: `from RazorEnhanced import Player`

Provides access to player character information, stats, and actions.

### Properties

#### `Player.Name`

Gets the name value

**Example**:
```python
from RazorEnhanced import Player

# Get player name
player_name = Player.Name
print(f"Character name: {player_name}")
```
#### `Player.Serial`

Gets the serial value

**Example**:
```python
from RazorEnhanced import Player

# Get serial value
value = Player.Serial
print(f"Serial: {value}")
```
#### `Player.Position`

Gets the position value

**Example**:
```python
from RazorEnhanced import Player

# Get player position
pos = Player.Position
print(f"Player at: X={pos.X}, Y={pos.Y}, Z={pos.Z}")
```
#### `Player.Hits`

Gets the hits value

**Example**:
```python
from RazorEnhanced import Player, Misc

# Check player health
current_hp = Player.Hits
max_hp = Player.HitsMax
health_percent = (current_hp / max_hp) * 100

if health_percent < 50:
    Misc.SendMessage("Health is low!", 0x20)
```
#### `Player.Mana`

Gets the mana value

**Example**:
```python
from RazorEnhanced import Player

# Get mana value
value = Player.Mana
print(f"Mana: {value}")
```
#### `Player.Stamina`

Gets the stamina value

**Example**:
```python
from RazorEnhanced import Player

# Get stamina value
value = Player.Stamina
print(f"Stamina: {value}")
```
#### `Player.Status`

Gets the status value

**Example**:
```python
from RazorEnhanced import Player

# Get status value
value = Player.Status
print(f"Status: {value}")
```
### Methods

#### `Player.MobileID`

**Signature**: `MobileID (see: Mobile.Body)`

Method for MobileID operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use MobileID method
try:
    result = Player.MobileID (see: Mobile.Body)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.Enpowerment`

**Signature**: `Enpowerment (new)`

Method for Enpowerment operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use Enpowerment method
try:
    result = Player.Enpowerment (new)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.Oath`

**Signature**: `Oath (caster)`

Method for Oath operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use Oath method
try:
    result = Player.Oath (caster)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.Oath`

**Signature**: `Oath (curse)`

Method for Oath operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use Oath method
try:
    result = Player.Oath (curse)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.Despair`

**Signature**: `Despair (target)`

Method for Despair operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use Despair method
try:
    result = Player.Despair (target)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.Disarm`

**Signature**: `Disarm (new)`

Method for Disarm operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use Disarm method
try:
    result = Player.Disarm (new)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.One`

**Signature**: `One (new)`

Method for One operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use One method
try:
    result = Player.One (new)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.Focusing`

**Signature**: `Focusing (target)`

Method for Focusing operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use Focusing method
try:
    result = Player.Focusing (target)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.Focusing`

**Signature**: `Focusing (target)`

Method for Focusing operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use Focusing method
try:
    result = Player.Focusing (target)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Player.Body`

**Signature**: `Body (see: Mobile.MobileID)`

Method for Body operations

**Example**:
```python
from RazorEnhanced import Player, Misc

# Use Body method
try:
    result = Player.Body (see: Mobile.MobileID)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
---

## Target

> **Import**: `from RazorEnhanced import Target`

Controls target selection and targeting operations.

### Properties

#### `Target.Name`

Gets the name value

**Example**:
```python
from RazorEnhanced import Target

# Get name value
value = Target.Name
print(f"Name: {value}")
```
#### `Target.Serial`

Gets the serial value

**Example**:
```python
from RazorEnhanced import Target

# Get serial value
value = Target.Serial
print(f"Serial: {value}")
```
### Methods

#### `Target.AttackTargetFromList`

**Signature**: `AttackTargetFromList(target_name)`

Method for AttackTargetFromList operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use AttackTargetFromList method
try:
    result = Target.AttackTargetFromList(target_name)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.AttackTargetFromList`

**Signature**: `AttackTargetFromList(target_name)`

Method for AttackTargetFromList operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use AttackTargetFromList method
try:
    result = Target.AttackTargetFromList(target_name)
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.Cancel`

**Signature**: `Cancel()`

Method for Cancel operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use Cancel method
try:
    result = Target.Cancel()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.Cancel`

**Signature**: `Cancel()`

Method for Cancel operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use Cancel method
try:
    result = Target.Cancel()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.ClearLast`

**Signature**: `ClearLast()`

Method for ClearLast operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use ClearLast method
try:
    result = Target.ClearLast()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.ClearLast`

**Signature**: `ClearLast()`

Method for ClearLast operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use ClearLast method
try:
    result = Target.ClearLast()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.ClearLastAttack`

**Signature**: `ClearLastAttack()`

Method for ClearLastAttack operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use ClearLastAttack method
try:
    result = Target.ClearLastAttack()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.ClearLastAttack`

**Signature**: `ClearLastAttack()`

Method for ClearLastAttack operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use ClearLastAttack method
try:
    result = Target.ClearLastAttack()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.ClearLastandQueue`

**Signature**: `ClearLastandQueue()`

Method for ClearLastandQueue operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use ClearLastandQueue method
try:
    result = Target.ClearLastandQueue()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
#### `Target.ClearLastandQueue`

**Signature**: `ClearLastandQueue()`

Method for ClearLastandQueue operations

**Example**:
```python
from RazorEnhanced import Target, Misc

# Use ClearLastandQueue method
try:
    result = Target.ClearLastandQueue()
    if result:
        Misc.SendMessage("Operation successful", 0x40)
except Exception as e:
    Misc.SendMessage(f"Error: {e}", 0x20)
```
---

## Best Practices

### 1. Always Use Error Handling
Every RazorEnhanced script should include proper error handling to prevent crashes.

```python
from RazorEnhanced import Items, Player, Misc

def safe_item_operation(item_serial):
    try:
        item = Items.FindBySerial(item_serial)
        if item is None:
            raise ValueError("Item not found")
        
        # Perform operation
        Items.Move(item.Serial, Player.Backpack.Serial, 1)
        return True
        
    except Exception as e:
        Misc.SendMessage(f"Error: {e}", 0x20)
        return False
```

### 2. Use Timeouts for Waiting Operations
Always specify timeouts to prevent infinite waiting.

```python
from RazorEnhanced import Target, Items, Misc

# Good: Use timeout
Target.PromptTarget()
if Target.WaitForTarget(5000):  # 5 second timeout
    target = Target.GetTargetSerial()
    # Process target
else:
    Misc.SendMessage("Target selection timed out", 0x20)

# Good: Wait for container contents with timeout
Items.WaitForContents(Player.Backpack.Serial, 2000)
```

### 3. Check Return Values
Many methods return success/failure status - always check these.

```python
from RazorEnhanced import Items, Player, Misc

# Check if operation succeeded
success = Items.Move(item_serial, Player.Backpack.Serial, 1)
if success:
    Misc.SendMessage("Item moved successfully", 0x40)
else:
    Misc.SendMessage("Failed to move item", 0x20)
```

### 4. Use Appropriate Delays
Give the server time to process operations between commands.

```python
from RazorEnhanced import Items, Misc

# Move multiple items with delays
for item_serial in item_list:
    Items.Move(item_serial, container, 1)
    Misc.Pause(100)  # Small delay between moves
```

### 5. Clear Journal Before Monitoring
Always clear the journal before performing actions you want to monitor.

```python
from RazorEnhanced import Journal, Player, Misc

# Clear journal before skill use
Journal.Clear()
Player.UseSkill("Hiding")

# Then check for messages
Misc.Pause(1000)
if Journal.Search("You have hidden"):
    Misc.SendMessage("Hidden successfully", 0x40)
```

### 6. Validate Objects Before Use
Check that objects exist and are valid before using them.

```python
from RazorEnhanced import Items, Player, Misc

# Always validate items
item = Items.FindBySerial(serial)
if item and item.Serial != 0:
    # Item is valid, safe to use
    Items.UseItem(item.Serial)
else:
    Misc.SendMessage("Invalid item", 0x20)

# Check containers before accessing
backpack = Player.Backpack
if backpack and backpack.Serial != 0:
    Items.WaitForContents(backpack.Serial, 1000)
```

## Additional Resources

### Official Documentation
- [RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)
- [Script Library](https://github.com/RazorEnhanced/ScriptLibrary)

### Community Resources
- [RazorEnhanced Discord](https://discord.gg/VdyCpjQ)
- [UO Script Examples](https://github.com/RazorEnhanced/ScriptLibrary/tree/master/Examples)

### Development Tools
- Use RazorEnhanced's built-in script editor for development
- Enable debug logging for troubleshooting
- Test scripts in safe environments before production use

### Contributing
This documentation is generated automatically. For the most current information,
always refer to the official RazorEnhanced documentation.

---
**Generated**: 2025-06-29 12:32:25  
**Source**: Official RazorEnhanced API Documentation  
**Generator Version**: 1.0  
