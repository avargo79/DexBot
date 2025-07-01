# Mobile

The Mobile class represents an single alive entity. 
While the Mobile.Serial is unique for each Mobile, Mobile.MobileID is the unique for the Mobile apparence, or image. Sometimes is also called Body or Body ID.
Mobiles which dies and leave a corpse behind, they stop existing as Mobiles and instead leave a corpse as a Item object appears.

## Properties

### Backpack

**Type:** `Item`

Get the Item representing the backpack of a Mobile. Return null if it doesn't have one.

### CanRename

**Type:** `Boolean`

Determine if a mobile can be renamed. (Ex: pets, summons, etc )

### Color

**Type:** `UInt16`

Color of the mobile.

### Contains

**Type:** `List[Item]`

Returns the list of items present in the Paperdoll (or equivalent) of the Mobile.
Might not match the items found using via Layer.

### Deleted

**Type:** `Boolean`

### Direction

**Type:** `String`

Returns the direction of the Mobile.

### Fame

**Type:** `Int32`

Fame has to be reverse engineered from the title so it is just ranges:
0: neutaral - 3 is highest fame

### Female

**Type:** `Boolean`

The Mobile is a female.

### Flying

**Type:** `Boolean`

The mobile is Flying ( Gragoyle )

### Graphics

**Type:** `UInt16`

### Hits

**Type:** `Int32`

The current hit point of a Mobile. To be read as propotion over Mobile.HitsMax.

### HitsMax

**Type:** `Int32`

Maximum hitpoint of a Mobile.

### Hue

**Type:** `UInt16`

### InParty

**Type:** `Boolean`

True: if the Mobile is in your party. - False: otherwise.

### IsGhost

**Type:** `Boolean`

If is a Ghost
Match any MobileID  in the list:
    402, 403, 607, 608, 694, 695, 970

### IsHuman

**Type:** `Boolean`

Check is the Mobile has a human body.
Match any MobileID in the list:
    183, 184, 185, 186, 400, 
    401, 402, 403, 605, 606,
    607, 608, 666, 667, 694, 
    744, 745, 747, 748, 750,  
    751, 970, 695

### ItemID

**Type:** `Int32`

### Karma

**Type:** `Int32`

Karma has to be reverse engineered from the title so it is just ranges:
-5: most evil, 0: neutaral, 5 most good

### KarmaTitle

**Type:** `String`

This is the title string returned from the server

### Mana

**Type:** `Int32`

The current mana of a Mobile. To be read as propotion over Mobile.ManaMax.

### ManaMax

**Type:** `Int32`

Maximum mana of a Mobile.

### Map

**Type:** `Int32`

Current map or facet.

### MobileID

**Type:** `Int32`

Represents the type of Mobile, usually unique for the Mobile image. ( Alias: Mobile.Body )

### Mount

**Type:** `Item`

Returns the Item assigned to the "Mount" Layer.

### Name

**Type:** `String`

Name of the Mobile.

### Notoriety

**Type:** `Int32`

Get the notoriety of the Mobile.

Notorieties:
    1: blue, innocent
    2: green, friend
    3: gray, neutral
    4: gray, criminal
    5: orange, enemy
    6: red, hostile 
    6: yellow, invulnerable

### Paralized

**Type:** `Boolean`

The mobile is Paralized.

### Poisoned

**Type:** `Boolean`

The mobile is Poisoned.

### Position

**Type:** `Point3D`

### Properties

**Type:** `List[Property]`

Get all properties of a Mobile as list of lines of the tooltip.

### PropsUpdated

**Type:** `Boolean`

True: Mobile.Propertires are updated - False: otherwise.

### Quiver

**Type:** `Item`

Get the Item representing the quiver of a Mobile. Return null if it doesn't have one.

### Serial

**Type:** `Int32`

### Stam

**Type:** `Int32`

The current stamina of a Mobile. To be read as propotion over Mobile.StamMax.

### StamMax

**Type:** `Int32`

Maximum stamina of a Mobile.

### Visible

**Type:** `Boolean`

True: The Mobile is visible - Flase: The mobile is hidden.

### WarMode

**Type:** `Boolean`

Mobile is in War mode.

### YellowHits

**Type:** `Boolean`

The mobile healthbar is not blue, but yellow.

## Methods

### DistanceTo

```python
DistanceTo(other_mobile: Mobile)
```

Returns the UO distance between the current Mobile and another one.

**Parameters:**

- `other_mobile` (Mobile): The other mobile.

**Returns:** `Int32`

### Equals

#### Overload 1

```python
Equals(obj: Object)
```

**Parameters:**

- `obj` (Object)

**Returns:** `Boolean`

#### Overload 2

```python
Equals(entity: UOEntity)
```

**Parameters:**

- `entity` (UOEntity)

**Returns:** `Boolean`

### GetHashCode

```python
GetHashCode()
```

**Returns:** `Int32`

### GetItemOnLayer

```python
GetItemOnLayer(layer: String)
```

Returns the Item associated with a Mobile Layer.

**Parameters:**

- `layer` (String): Layers:
   Layername
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

**Returns:** `Item` - Item for the layer. Return null if not found or Layer invalid.

### UpdateKarma

```python
UpdateKarma()
```

Costly! 
Updates the Fame and Karma of the Mobile, but it can take as long as 1 second to complete.

**Returns:** `Boolean` - True if successful, False if not server packet received

