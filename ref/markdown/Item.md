# Item

The Item class represent a single in-game Item object. Examples of Item are: Swords, bags, bandages, reagents, clothing.
While the Item.Serial is unique for each Item, Item.ItemID is the unique for the Item apparence, or image. Sometimes is also called ID or Graphics ID.
Item can also be house foriture as well as decorative items on the ground, like lamp post and banches.
However, for Item on the ground that cannot be picked up, they might be part of the world map, see Statics class.

## Properties

### Amount

**Type:** `Int32`

Read amount from item type object.

### Color

**Type:** `UInt16`

### Container

**Type:** `Int32`

Serial of the container which contains the object.

### ContainerOpened

**Type:** `Boolean`

True when the container was opened

### Contains

**Type:** `List[Item]`

Contains the list of Item inside a container.

### CorpseNumberItems

**Type:** `Int32`

-1 until corpse is checked, then # items in corpse. Used by looter to ignore empty corpses

### Deleted

**Type:** `Boolean`

### Direction

**Type:** `String`

Item direction.

### Durability

**Type:** `Int32`

Get the current durability of an Item. (0: no durability)

### Graphics

**Type:** `UInt16`

### GridNum

**Type:** `Byte`

Returns the GridNum of the item. (need better documentation)

### Hue

**Type:** `UInt16`

### Image

**Type:** `Bitmap`

Get the in-game image on an Item as Bitmap object.
See MSDN: https://docs.microsoft.com/dotnet/api/system.drawing.bitmap

### IsBagOfSending

**Type:** `Boolean`

True: if the item is a bag of sending - False: otherwise.

### IsContainer

**Type:** `Boolean`

True: if the item is a container - False: otherwise.

### IsCorpse

**Type:** `Boolean`

True: if the item is a corpse - False: otherwise.

### IsDoor

**Type:** `Boolean`

True: if the item is a door - False: otherwise.

### IsInBank

**Type:** `Boolean`

True: if the item is in the Player's bank - False: otherwise.

### IsLootable

**Type:** `Boolean`

True: For regualar items - False: for hair, beards, etc.

### IsPotion

**Type:** `Boolean`

True: if the item is a potion - False: otherwise.

### IsResource

**Type:** `Boolean`

True: if the item is a resource (ore, sand, wood, stone, fish) - False: otherwise

### IsSearchable

**Type:** `Boolean`

True: if the item is a pouch - False: otherwise.

### IsTwoHanded

**Type:** `Boolean`

True: if the item is a 2-handed weapon - False: otherwise.

### IsVirtueShield

**Type:** `Boolean`

True: if the item is a virtue shield - False: otherwise.

### ItemID

**Type:** `Int32`

Represents the type of Item, usually unique for the Item image.  Sometime called ID or Graphics ID.

### Layer

**Type:** `String`

Gets the Layer, for werable items only. (need better documentation)

### Light

**Type:** `Byte`

Item light's direction (e.g. will affect corpse's facing direction)

### MaxDurability

**Type:** `Int32`

Get the maximum durability of an Item. (0: no durability)

### Movable

**Type:** `Boolean`

Item is movable

### Name

**Type:** `String`

Item name

### OnGround

**Type:** `Boolean`

True: if the item is on the ground - False: otherwise.

### Position

**Type:** `Point3D`

### Properties

**Type:** `List[Property]`

Get the list of Properties of an Item.

### PropsUpdated

**Type:** `Boolean`

True: if Properties are updated - False: otherwise.

### RootContainer

**Type:** `Int32`

Get serial of root container of item.

### Serial

**Type:** `Int32`

### Updated

**Type:** `Boolean`

Check if the Item already have been updated with all the properties. (need better documentation)

### Visible

**Type:** `Boolean`

Item is Visible

### Weight

**Type:** `Int32`

Get the weight of a item. (0: no weight)

## Methods

### DistanceTo

#### Overload 1

```python
DistanceTo(mob: Mobile)
```

Return the distance in number of tiles, from Item to Mobile.

**Parameters:**

- `mob` (Mobile): Target as Mobile

**Returns:** `Int32` - Distance in number of tiles.

#### Overload 2

```python
DistanceTo(itm: Item)
```

**Parameters:**

- `itm` (Item): Target as Item

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

### GetWorldPosition

```python
GetWorldPosition()
```

**Returns:** `Point3D`

### IsChildOf

#### Overload 1

```python
IsChildOf(container: Item, maxDepth: Int32 = 100)
```

Check if an Item is contained in a container. Can be a Item or a Mobile (wear by).

**Parameters:**

- `container` (Item): Item as container.
- `maxDepth` (Int32)

**Returns:** `Boolean` - True: if is contained - False: otherwise.

#### Overload 2

```python
IsChildOf(container: Mobile, maxDepth: Int32 = 100)
```

**Parameters:**

- `container` (Mobile): Mobile as container.
- `maxDepth` (Int32)

**Returns:** `Boolean`

### ToString

```python
ToString()
```

**Returns:** `String`

