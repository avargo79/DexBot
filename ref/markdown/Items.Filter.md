# Items.Filter

The Items.Filter class is used to store options to filter the global Item list.
Often used in combination with Items.ApplyFilter.

## Properties

### CheckIgnoreObject

**Type:** `Boolean`

Exclude from the search Items which are currently on the global Ignore List. ( default: False, any Item )

### Enabled

**Type:** `Boolean`

True: The filter is used - False: Return all Item. ( default: True, active )

### Graphics

**Type:** `List[Int32]`

Limit the search to a list of Grapichs ID (see: Item.ItemID ) 
Supports .Add() and .AddRange()

### Hues

**Type:** `List[Int32]`

Limit the search to a list of Colors.
Supports .Add() and .AddRange()

### IsContainer

**Type:** `Int32`

Limit the search to the Items which are also containers. (default: -1: any Item)

### IsCorpse

**Type:** `Int32`

Limit the search to the corpses on the ground. (default: -1, any Item)

### IsDoor

**Type:** `Int32`

Limit the search to the doors. (default: -1: any Item)

### Layers

**Type:** `List[String]`

Limit the search to the wearable Items by Layer.
Supports .Add() and .AddRange()

Layers:
    RightHand
    LeftHand
    Shoes
    Pants
    Shirt
    Head
    Gloves
    Ring
    Neck
    Waist
    InnerTorso
    Bracelet
    MiddleTorso
    Earrings
    Arms
    Cloak
    OuterTorso
    OuterLegs
    InnerLegs
    Talisman

### Movable

**Type:** `Int32`

Limit the search to only Movable Items. ( default: -1, any Item )

### Multi

**Type:** `Int32`

Limit the search to only Multi Items. ( default: -1, any Item )

### Name

**Type:** `String`

Limit the search by name of the Item.

### OnGround

**Type:** `Int32`

Limit the search to the Items on the ground. (default: -1, any Item)

### RangeMax

**Type:** `Double`

Limit the search by distance, to Items which are at most RangeMax tiles away from the Player. ( default: -1, any Item )

### RangeMin

**Type:** `Double`

Limit the search by distance, to Items which are at least RangeMin tiles away from the Player. ( default: -1, any Item )

### Serials

**Type:** `List[Int32]`

Limit the search to a list of Serials of Item to find. (ex: 0x0406EFCA )
Supports .Add() and .AddRange()

### ZRangeMax

**Type:** `Double`

Limit the search by height, to Items which are at most ZRangeMax coordinates away from the Player. ( default: -1, any Item )

### ZRangeMin

**Type:** `Double`

Limit the search by height, to Items which are at least ZRangeMin coordinates away from the Player. ( default: -1, any Item )

## Methods

No methods available.

