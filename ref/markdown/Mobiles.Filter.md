# Mobiles.Filter

The Mobiles.Filter class is used to store options to filter the global Mobile list.
Often used in combination with Mobiles.ApplyFilter.

## Properties

### Blessed

**Type:** `Int32`

Limit the search to only Blessed Mobiles.  (default: -1, any Mobile)

### Bodies

**Type:** `List[Int32]`

Limit the search to a list of MobileID (see: Mobile.ItemID or Mobile.Body ) 
Supports .Add() and .AddRange()

### CheckIgnoreObject

**Type:** `Boolean`

Exclude from the search Mobiles which are currently on the global Ignore List. ( default: False, any Item )

### CheckLineOfSight

**Type:** `Boolean`

Limit the search only to the Mobiles which are in line of sight. (default: false, any Mobile)

### Enabled

**Type:** `Boolean`

True: The filter is used - False: Return all Mobile. ( default: True, active )

### Female

**Type:** `Int32`

Limit the search to female Mobile.  (default: -1, any)

### Friend

**Type:** `Int32`

Limit the search to friend Mobile. (default: -1, any)

### Graphics

**Type:** `List[Int32]`

### Hues

**Type:** `List[Int32]`

Limit the search to a list of Colors.
Supports .Add() and .AddRange()

### IgnorePets

**Type:** `Boolean`

Include the Mobiles which are currently on the Pet List. ( default: True, include Pets )

### IsGhost

**Type:** `Int32`

Limit the search to Ghost only. (default: -1, any Mobile )
Match any MobileID in the list:
    402, 403, 607, 608, 694, 695, 970

### IsHuman

**Type:** `Int32`

Limit the search to Humans only. (default: -1, any Mobile )
Match any MobileID in the list:
    183, 184, 185, 186, 400, 
    401, 402, 403, 605, 606,
    607, 608, 666, 667, 694, 
    744, 745, 747, 748, 750,  
    751, 970, 695

### Name

**Type:** `String`

Limit the search by name of the Mobile.

### Notorieties

**Type:** `List[Byte]`

Limit the search to the Mobile by notoriety.
Supports .Add() and .AddRange()

Notorieties:
    1: blue, innocent
    2: green, friend
    3: gray, neutral
    4: gray, criminal
    5: orange, enemy
    6: red, hostile 
    6: yellow, invulnerable

### Paralized

**Type:** `Int32`

Limit the search to paralized Mobile. (default: -1, any)

### Poisoned

**Type:** `Int32`

Limit the search to only Poisoned Mobiles.  (default: -1, any Mobile)

### RangeMax

**Type:** `Double`

Limit the search by distance, to Mobiles which are at most RangeMax tiles away from the Player. ( default: -1, any Mobile )

### RangeMin

**Type:** `Double`

Limit the search by distance, to Mobiles which are at least RangeMin tiles away from the Player. ( default: -1, any Mobile )

### Serials

**Type:** `List[Int32]`

Limit the search to a list of Serials of Mobile to find. (ex: 0x0406EFCA )
Supports .Add() and .AddRange()

### Warmode

**Type:** `Int32`

Limit the search to Mobile War mode. (default: -1, any Mobile)
    -1: any
     0: peace
     1: war

### ZLevelMax

**Type:** `Double`

Limit the search by z-level, to Mobiles which are at most z-level specified. ( default: 4096, all z-levels )

### ZLevelMin

**Type:** `Double`

Limit the search by z-level, to Mobiles which are at least z-level specified. ( default: -4096, all z-levels )

## Methods

No methods available.

