# RazorEnhanced API Reference

> **Generated on**: 2025-06-29 10:18:50
> 
> This is a local reference for the RazorEnhanced API, automatically generated for DexBot development.
> For the most current information, always refer to the [official documentation](https://github.com/RazorEnhanced/ScriptLibrary/wiki).

## Table of Contents

- [Gumps](#gumps)
- [Items](#items)
- [Journal](#journal)
- [Misc](#misc)
- [Mobile](#mobile)
- [Player](#player)
- [Spells](#spells)
- [Target](#target)
- [Timer](#timer)
- [Trade](#trade)

## Quick Reference


### Common Import Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
import RazorEnhanced as RE
from RazorEnhanced import *
```

### Basic Usage Examples
```python
# Player information
player_name = Player.Name
player_hp = Player.Hits
player_position = Player.Position

# Item handling
item = Items.FindBySerial(0x12345678)
if item:
    Items.Move(item.Serial, Player.Backpack.Serial, 1)

# Gump interaction
if Gumps.HasGump():
    gump = Gumps.GetGump()
    Gumps.SendAction(gump.Serial, 1)  # Press button 1

# Journal monitoring
Journal.Clear()
# ... perform action ...
if Journal.Search("You successfully"):
    print("Action succeeded!")
```

### Error Handling Best Practices
```python
try:
    # Your RazorEnhanced code here
    result = Items.FindBySerial(serial)
    if result is None:
        raise ValueError("Item not found")
except Exception as e:
    print(f"Error: {e}")
    # Handle the error appropriately
```

## Detailed API Documentation


## Gumps

# Gumps API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Gumps API - User interface interaction

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Gumps

# Example usage
# Gumps-specific methods will be documented here
```

## Examples

```python
# Basic gumps operations
try:
    # Your Gumps code here
    pass
except Exception as e:
    print(f"Error in Gumps operation: {e}")
```

## Error Handling

When working with the Gumps API, always implement proper error handling:

```python
try:
    # Gumps operations
    pass
except Exception as e:
    # Log the error
    print(f"Gumps API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Items

# Items API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Items API - Item manipulation and queries

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Items

# Example usage
# Items-specific methods will be documented here
```

## Examples

```python
# Basic items operations
try:
    # Your Items code here
    pass
except Exception as e:
    print(f"Error in Items operation: {e}")
```

## Error Handling

When working with the Items API, always implement proper error handling:

```python
try:
    # Items operations
    pass
except Exception as e:
    # Log the error
    print(f"Items API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Journal

# Journal API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Journal API - Game message monitoring

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Journal

# Example usage
# Journal-specific methods will be documented here
```

## Examples

```python
# Basic journal operations
try:
    # Your Journal code here
    pass
except Exception as e:
    print(f"Error in Journal operation: {e}")
```

## Error Handling

When working with the Journal API, always implement proper error handling:

```python
try:
    # Journal operations
    pass
except Exception as e:
    # Log the error
    print(f"Journal API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Misc

# Misc API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Misc API - Utility functions

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Misc

# Example usage
# Misc-specific methods will be documented here
```

## Examples

```python
# Basic misc operations
try:
    # Your Misc code here
    pass
except Exception as e:
    print(f"Error in Misc operation: {e}")
```

## Error Handling

When working with the Misc API, always implement proper error handling:

```python
try:
    # Misc operations
    pass
except Exception as e:
    # Log the error
    print(f"Misc API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Mobile

# Mobile API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Mobile API - Mobile/NPC interactions

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Mobile

# Example usage
# Mobile-specific methods will be documented here
```

## Examples

```python
# Basic mobile operations
try:
    # Your Mobile code here
    pass
except Exception as e:
    print(f"Error in Mobile operation: {e}")
```

## Error Handling

When working with the Mobile API, always implement proper error handling:

```python
try:
    # Mobile operations
    pass
except Exception as e:
    # Log the error
    print(f"Mobile API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Player

# Player API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Player API - Character information and actions

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Player

# Example usage
# Player-specific methods will be documented here
```

## Examples

```python
# Basic player operations
try:
    # Your Player code here
    pass
except Exception as e:
    print(f"Error in Player operation: {e}")
```

## Error Handling

When working with the Player API, always implement proper error handling:

```python
try:
    # Player operations
    pass
except Exception as e:
    # Log the error
    print(f"Player API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Spells

# Spells API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Spells API - Spell casting

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Spells

# Example usage
# Spells-specific methods will be documented here
```

## Examples

```python
# Basic spells operations
try:
    # Your Spells code here
    pass
except Exception as e:
    print(f"Error in Spells operation: {e}")
```

## Error Handling

When working with the Spells API, always implement proper error handling:

```python
try:
    # Spells operations
    pass
except Exception as e:
    # Log the error
    print(f"Spells API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Target

# Target API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Target API - Target selection

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Target

# Example usage
# Target-specific methods will be documented here
```

## Examples

```python
# Basic target operations
try:
    # Your Target code here
    pass
except Exception as e:
    print(f"Error in Target operation: {e}")
```

## Error Handling

When working with the Target API, always implement proper error handling:

```python
try:
    # Target operations
    pass
except Exception as e:
    # Log the error
    print(f"Target API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Timer

# Timer API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Timer API - Timing utilities

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Timer

# Example usage
# Timer-specific methods will be documented here
```

## Examples

```python
# Basic timer operations
try:
    # Your Timer code here
    pass
except Exception as e:
    print(f"Error in Timer operation: {e}")
```

## Error Handling

When working with the Timer API, always implement proper error handling:

```python
try:
    # Timer operations
    pass
except Exception as e:
    # Log the error
    print(f"Timer API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Trade

# Trade API

> **Note**: This documentation is automatically generated for DexBot development.
> For the most up-to-date information, please visit the [official API documentation](https://razorenhanced.github.io/doc/api/).

## Overview

Trade API - Trading functionality

## Common Methods

### Basic Usage Pattern
```python
import clr
clr.AddReference('RazorEnhanced')
from RazorEnhanced import Trade

# Example usage
# Trade-specific methods will be documented here
```

## Examples

```python
# Basic trade operations
try:
    # Your Trade code here
    pass
except Exception as e:
    print(f"Error in Trade operation: {e}")
```

## Error Handling

When working with the Trade API, always implement proper error handling:

```python
try:
    # Trade operations
    pass
except Exception as e:
    # Log the error
    print(f"Trade API Error: {e}")
    # Handle gracefully
```

## See Also

- [Official RazorEnhanced API Documentation](https://razorenhanced.github.io/doc/api/)
- [RazorEnhanced Wiki](http://razorenhanced.net/dokuwiki/doku.php)
- [RazorEnhanced GitHub Repository](https://github.com/RazorEnhanced/RazorEnhanced)

---
*Last updated: 2025-06-29 10:18:50*


---

## Additional Resources

### Official Documentation
- [RazorEnhanced Wiki](https://github.com/RazorEnhanced/ScriptLibrary/wiki)
- [RazorEnhanced GitHub](https://github.com/RazorEnhanced/RazorEnhanced)
- [Script Library](https://github.com/RazorEnhanced/ScriptLibrary)

### DexBot Integration
This API reference is maintained as part of the DexBot project to provide
offline access to RazorEnhanced documentation during development.

### Contributing
If you notice any discrepancies or have improvements to suggest, please:
1. Check the official documentation first
2. Update this reference by running `python scripts/update_api_docs.py`
3. Submit a pull request with your changes

---
*This document was automatically generated by DexBot's API documentation fetcher.*
*Last updated: 2025-06-29 10:18:50*
