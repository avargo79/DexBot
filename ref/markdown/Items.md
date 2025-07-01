# Items

The Items class provides a wide range of functions to search and interact with Items.

## Properties

No properties available.

## Methods

### ApplyFilter

```python
ApplyFilter(filter: Items.Filter)
```

Filter the global list of Items according to the options specified by the filter ( see: Items.Filter ).

**Parameters:**

- `filter` (Items.Filter): A filter object.

**Returns:** `List[Item]` - the list of Items respectinf the filter criteria.

### BackpackCount

```python
BackpackCount(itemid: Int32, color: Int32 = -1)
```

Count items in Player Backpack.

**Parameters:**

- `itemid` (Int32): ItemID to search.
- `color` (Int32): Color to search. (default -1: any color)

**Returns:** `Int32`

### ChangeDyeingTubColor

```python
ChangeDyeingTubColor(dyes: Item, dyeingTub: Item, color: Int32)
```

Use the Dyes on a Dyeing Tub and select the color via color picker, using dedicated packets. 
Need to specify the dyes, the dye tube and the color to use.

**Parameters:**

- `dyes` (Item): Dyes as Item object.
- `dyeingTub` (Item): Dyeing Tub as Item object.
- `color` (Int32): Color to choose.

**Returns:** `Void`

### Close

#### Overload 1

```python
Close(serial: Int32)
```

Close opened container window. 
On OSI, to close opened corpse window, you need to close the corpse's root container 
Currently corpse's root container can be found by using item filter.

**Parameters:**

- `serial` (Int32): Serial or Item to hide.

**Returns:** `Void`

#### Overload 2

```python
Close(item: Item)
```

**Parameters:**

- `item` (Item)

**Returns:** `Void`

### ContainerCount

#### Overload 1

```python
ContainerCount(container: Item, itemid: Int32, color: Int32 = -1, recursive: Boolean = False)
```

Count items inside a container, summing also the amount in stacks.

**Parameters:**

- `container` (Item): Serial or Item to search into.
- `itemid` (Int32): ItemID of the item to search.
- `color` (Int32): Color to match. (default: -1, any color)
- `recursive` (Boolean): Search also in already open subcontainers.

**Returns:** `Int32`

#### Overload 2

```python
ContainerCount(serial: Int32, itemid: Int32, color: Int32 = -1, recursive: Boolean = False)
```

**Parameters:**

- `serial` (Int32)
- `itemid` (Int32)
- `color` (Int32)
- `recursive` (Boolean)

**Returns:** `Int32`

### ContextExist

#### Overload 1

```python
ContextExist(serial: Int32, name: String)
```

Check if Context Menu entry exists for an Item.

**Parameters:**

- `serial` (Int32): Serial or Item to check.
- `name` (String): Name of the Context Manu entry

**Returns:** `Int32`

#### Overload 2

```python
ContextExist(i: Item, name: String)
```

**Parameters:**

- `i` (Item)
- `name` (String)

**Returns:** `Int32`

### DropFromHand

```python
DropFromHand(item: Item, container: Item)
```

Drop into a bag an Item currently held in-hand. ( see: Items.Lift )

**Parameters:**

- `item` (Item): Item object to drop.
- `container` (Item): Target container.

**Returns:** `Void`

### DropItemGroundSelf

#### Overload 1

```python
DropItemGroundSelf(item: Item, amount: Int32 = 0)
```

Drop an Item on the ground, at the current Player position.
NOTE: On some server is not allowed to drop Items on tiles occupied by Mobiles and the Player.

**Parameters:**

- `item` (Item): Item object to drop.
- `amount` (Int32): Amount to move. (default: 0, the whole stack)

**Returns:** `Void`

#### Overload 2

```python
DropItemGroundSelf(serialitem: Int32, amount: Int32 = 0)
```

This function seldom works because the servers dont allow drop where your standing

**Parameters:**

- `serialitem` (Int32)
- `amount` (Int32)

**Returns:** `Void`

### FindAllByID

#### Overload 1

```python
FindAllByID(itemids: PythonList, color: Int32, container: Int32, range: Int32, considerIgnoreList: Boolean = True)
```

Find a List of Items matching specific list of ItemID, Color and Container. 
Optionally can search in all subcontaners or to a maximum depth in subcontainers.
Can use -1 on color for no chose color, can use -1 on container for search in all item in memory.
The depth defaults to only the top but can search for # of sub containers.

**Parameters:**

- `itemids` (PythonList)
- `color` (Int32): Color filter. (-1: any, 0: natural )
- `container` (Int32): Serial of the container to search. (-1: any Item)
- `range` (Int32)
- `considerIgnoreList` (Boolean): True: Ignore Items are excluded - False: any Item.

**Returns:** `PythonList` - The Item matching the criteria.

#### Overload 2

```python
FindAllByID(itemid: Int32, color: Int32, container: Int32, range: Int32, considerIgnoreList: Boolean = True)
```

**Parameters:**

- `itemid` (Int32)
- `color` (Int32)
- `container` (Int32)
- `range` (Int32)
- `considerIgnoreList` (Boolean)

**Returns:** `PythonList`

#### Overload 3

```python
FindAllByID(itemids: List[Int32], color: Int32, container: Int32, range: Int32, considerIgnoreList: Boolean = True)
```

**Parameters:**

- `itemids` (List[Int32])
- `color` (Int32)
- `container` (Int32)
- `range` (Int32)
- `considerIgnoreList` (Boolean)

**Returns:** `List[Item]`

### FindByID

#### Overload 1

```python
FindByID(itemid: Int32, color: Int32, container: Int32, recursive: Boolean = False, considerIgnoreList: Boolean = True)
```

Find a single Item matching specific ItemID, Color and Container. 
Optionally can search in all subcontaners or to a maximum depth in subcontainers.
Can use -1 on color for no chose color, can use -1 on container for search in all item in memory. The depth defaults to only the top but can search for # of sub containers.

**Parameters:**

- `itemid` (Int32): ItemID filter.
- `color` (Int32): Color filter. (-1: any, 0: natural )
- `container` (Int32): Serial of the container to search. (-1: any Item)
- `recursive` (Boolean): Search subcontainers. 
    True: all subcontainers
    False: only main
    1,2,n: Maximum subcontainer depth
- `considerIgnoreList` (Boolean): True: Ignore Items are excluded - False: any Item.

**Returns:** `Item` - The Item matching the criteria.

#### Overload 2

```python
FindByID(itemid: Int32, color: Int32, container: Int32, range: Int32, considerIgnoreList: Boolean = True)
```

**Parameters:**

- `itemid` (Int32)
- `color` (Int32)
- `container` (Int32)
- `range` (Int32)
- `considerIgnoreList` (Boolean)

**Returns:** `Item`

#### Overload 3

```python
FindByID(itemids: List[Int32], color: Int32 = -1, container: Int32 = -1, range: Int32 = 10, considerIgnoreList: Boolean = True)
```

**Parameters:**

- `itemids` (List[Int32])
- `color` (Int32)
- `container` (Int32)
- `range` (Int32)
- `considerIgnoreList` (Boolean)

**Returns:** `Item`

### FindByName

```python
FindByName(itemName: String, color: Int32, container: Int32, range: Int32, considerIgnoreList: Boolean = True)
```

Find a single Item matching specific Name, Color and Container. 
Optionally can search in all subcontaners or to a maximum depth in subcontainers.
Can use -1 on color for no chose color, can use -1 on container for search in all item in memory. The depth defaults to only the top but can search for # of sub containers.

**Parameters:**

- `itemName` (String): Item Name filter.
- `color` (Int32): Color filter. (-1: any, 0: natural )
- `container` (Int32): Serial of the container to search. (-1: any Item)
- `range` (Int32): Search subcontainers. 
    1,2,n: Maximum subcontainer depth
- `considerIgnoreList` (Boolean): True: Ignore Items are excluded - False: any Item.

**Returns:** `Item` - The Item matching the criteria.

### FindBySerial

```python
FindBySerial(serial: Int32)
```

Search for a specific Item by using it Serial

**Parameters:**

- `serial` (Int32): Serial of the Item.

**Returns:** `Item` - Item object if found, or null if not found.

### GetImage

```python
GetImage(itemID: Int32, hue: Int32 = 0)
```

Get the Image on an Item by specifing the ItemID. Optinally is possible to apply a color.

**Parameters:**

- `itemID` (Int32): ItemID to use.
- `hue` (Int32): Optional: Color to apply. (Default 0, natural)

**Returns:** `Bitmap`

### GetPropStringByIndex

#### Overload 1

```python
GetPropStringByIndex(serial: Int32, index: Int32)
```

Get a Property line, by index. if not found returns and empty string.

**Parameters:**

- `serial` (Int32): Serial or Item to read.
- `index` (Int32): Number of the Property line.

**Returns:** `String` - A property line as a string.

#### Overload 2

```python
GetPropStringByIndex(item: Item, index: Int32)
```

**Parameters:**

- `item` (Item)
- `index` (Int32)

**Returns:** `String`

### GetPropStringList

#### Overload 1

```python
GetPropStringList(serial: Int32)
```

Get string list of all Properties of an item, if item no props list is empty.

**Parameters:**

- `serial` (Int32): Serial or Item to read.

**Returns:** `List[String]` - List of strings.

#### Overload 2

```python
GetPropStringList(item: Item)
```

**Parameters:**

- `item` (Item)

**Returns:** `List[String]`

### GetPropValue

#### Overload 1

```python
GetPropValue(serial: Int32, name: String)
```

Read the value of a Property.

**Parameters:**

- `serial` (Int32): Serial or Item to read.
- `name` (String): Name of the Propery.

**Returns:** `Single`

#### Overload 2

```python
GetPropValue(item: Item, name: String)
```

**Parameters:**

- `item` (Item)
- `name` (String)

**Returns:** `Single`

### GetPropValueString

```python
GetPropValueString(serial: Int32, name: String)
```

Get a Property line, by name. if not found returns and empty string.

**Parameters:**

- `serial` (Int32): Serial or Item to read.
- `name` (String): Number of the Property line.

**Returns:** `String` - A property value as a string.

### GetProperties

```python
GetProperties(itemserial: Int32, delay: Int32)
```

Request to get immediatly the Properties of an Item, and wait for a specified amount of time.
This only returns properties and does not attempt to update the object.
Used in this way, properties for object not yet seen can be retrieved

**Parameters:**

- `itemserial` (Int32): Serial or Item read.
- `delay` (Int32): Maximum waiting time, in milliseconds.

**Returns:** `List[Property]`

### GetWeaponAbility

```python
GetWeaponAbility(itemId: Int32)
```

NOTE: This is from an internal razor table and can be changed based on your server!
Returns a pair of string values (Primary Ability, Secondary Ability) 
for the supplied item ID. 
"Invalid", "Invalid" for items not in the internal table

**Parameters:**

- `itemId` (Int32)

**Returns:** `ValueTuple[String, String]`

### Hide

#### Overload 1

```python
Hide(serial: Int32)
```

Hied an Item, affects only the player.

**Parameters:**

- `serial` (Int32): Serial or Item to hide.

**Returns:** `Void`

#### Overload 2

```python
Hide(item: Item)
```

**Parameters:**

- `item` (Item)

**Returns:** `Void`

### IgnoreTypes

```python
IgnoreTypes(itemIdList: PythonList)
```

Used to ignore specific types. Be careful as you wont see things you ignore, 
and could result in a mobile being able to kill you without you seeing it

**Parameters:**

- `itemIdList` (PythonList)

**Returns:** `Void`

### Lift

```python
Lift(item: Item, amount: Int32)
```

Lift an Item and hold it in-hand. ( see: Items.DropFromHand )

**Parameters:**

- `item` (Item): Item object to Lift.
- `amount` (Int32): Amount to lift. (0: the whole stack)

**Returns:** `Void`

### Message

#### Overload 1

```python
Message(item: Item, hue: Int32, message: String)
```

Display an in-game message on top of an Item, visibile only for the Player.

**Parameters:**

- `item` (Item): Serial or Item to display text on.
- `hue` (Int32): Color of the message.
- `message` (String): Message as

**Returns:** `Void`

#### Overload 2

```python
Message(serial: Int32, hue: Int32, message: String)
```

**Parameters:**

- `serial` (Int32)
- `hue` (Int32)
- `message` (String)

**Returns:** `Void`

### Move

#### Overload 1

```python
Move(source: Int32, destination: Int32, amount: Int32, x: Int32, y: Int32)
```

Move an Item to a destination, which can be an Item or a Mobile.

**Parameters:**

- `source` (Int32): Serial or Item of the Item to move.
- `destination` (Int32): Serial, Mobile or Item as destination.
- `amount` (Int32): Amount to move (-1: the whole stack)
- `x` (Int32): Optional: X coordinate inside the container.
- `y` (Int32): Optional: Y coordinate inside the container.

**Returns:** `Void`

#### Overload 2

```python
Move(source: Item, destination: Mobile, amount: Int32, x: Int32, y: Int32)
```

**Parameters:**

- `source` (Item)
- `destination` (Mobile)
- `amount` (Int32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

#### Overload 3

```python
Move(source: Int32, destination: Mobile, amount: Int32, x: Int32, y: Int32)
```

**Parameters:**

- `source` (Int32)
- `destination` (Mobile)
- `amount` (Int32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

#### Overload 4

```python
Move(source: Item, destination: Int32, amount: Int32, x: Int32, y: Int32)
```

**Parameters:**

- `source` (Item)
- `destination` (Int32)
- `amount` (Int32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

#### Overload 5

```python
Move(source: Int32, destination: Item, amount: Int32, x: Int32, y: Int32)
```

**Parameters:**

- `source` (Int32)
- `destination` (Item)
- `amount` (Int32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

#### Overload 6

```python
Move(source: Item, destination: Item, amount: Int32, x: Int32, y: Int32)
```

**Parameters:**

- `source` (Item)
- `destination` (Item)
- `amount` (Int32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

#### Overload 7

```python
Move(source: Item, destination: Mobile, amount: Int32)
```

**Parameters:**

- `source` (Item)
- `destination` (Mobile)
- `amount` (Int32)

**Returns:** `Void`

#### Overload 8

```python
Move(source: Int32, destination: Mobile, amount: Int32)
```

**Parameters:**

- `source` (Int32)
- `destination` (Mobile)
- `amount` (Int32)

**Returns:** `Void`

#### Overload 9

```python
Move(source: Item, destination: Int32, amount: Int32)
```

**Parameters:**

- `source` (Item)
- `destination` (Int32)
- `amount` (Int32)

**Returns:** `Void`

#### Overload 10

```python
Move(source: Int32, destination: Item, amount: Int32)
```

**Parameters:**

- `source` (Int32)
- `destination` (Item)
- `amount` (Int32)

**Returns:** `Void`

#### Overload 11

```python
Move(source: Item, destination: Item, amount: Int32)
```

**Parameters:**

- `source` (Item)
- `destination` (Item)
- `amount` (Int32)

**Returns:** `Void`

#### Overload 12

```python
Move(source: Int32, destination: Int32, amount: Int32)
```

**Parameters:**

- `source` (Int32)
- `destination` (Int32)
- `amount` (Int32)

**Returns:** `Void`

### MoveOnGround

#### Overload 1

```python
MoveOnGround(source: Int32, amount: Int32, x: Int32, y: Int32, z: Int32)
```

Move an Item on the ground to a specific location.

**Parameters:**

- `source` (Int32): Serial or Item to move.
- `amount` (Int32): Amount of Items to move (0: the whole stack )
- `x` (Int32): X world coordinates.
- `y` (Int32): Y world coordinates.
- `z` (Int32): Z world coordinates.

**Returns:** `Void`

#### Overload 2

```python
MoveOnGround(source: Item, amount: Int32, x: Int32, y: Int32, z: Int32)
```

**Parameters:**

- `source` (Item)
- `amount` (Int32)
- `x` (Int32)
- `y` (Int32)
- `z` (Int32)

**Returns:** `Void`

### OpenAt

#### Overload 1

```python
OpenAt(serial: Int32, x: Int32, y: Int32)
```

**Parameters:**

- `serial` (Int32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

#### Overload 2

```python
OpenAt(item: Item, x: Int32, y: Int32)
```

**Parameters:**

- `item` (Item)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

### OpenContainerAt

```python
OpenContainerAt(bag: Item, x: Int32, y: Int32)
```

Open a container at a specific location on the screen

**Parameters:**

- `bag` (Item): Container as Item object.
- `x` (Int32): x location to open at
- `y` (Int32): y location to open at

**Returns:** `Void`

### Select

```python
Select(items: List[Item], selector: String)
```

**Parameters:**

- `items` (List[Item])
- `selector` (String)

**Returns:** `Item`

### SetColor

```python
SetColor(serial: Int32, color: Int32 = -1)
```

Change/override the Color of an Item, the change affects only Player client. The change is not persistent.
If the color is -1 or unspecified, the color of the item is restored.

**Parameters:**

- `serial` (Int32): Serial of the Item.
- `color` (Int32): Color as number. (default: -1, reset original color)

**Returns:** `Void`

### SingleClick

#### Overload 1

```python
SingleClick(item: Item)
```

Send a single click network event to the server.

**Parameters:**

- `item` (Item): Serial or Item to click

**Returns:** `Void`

#### Overload 2

```python
SingleClick(itemserial: Int32)
```

**Parameters:**

- `itemserial` (Int32)

**Returns:** `Void`

### UseItem

#### Overload 1

```python
UseItem(itemSerial: Int32, targetSerial: Int32, wait: Boolean)
```

Use an Item, optionally is possible to specify a Item or Mobile target.
NOTE: The optional target may not work on some free shards. Use Target.Execute instead.

**Parameters:**

- `itemSerial` (Int32): Serial or Item to use.
- `targetSerial` (Int32): Optional: Serial of the Item or Mobile target.
- `wait` (Boolean): Optional: Wait for confirmation by the server. (default: True)

**Returns:** `Void`

#### Overload 2

```python
UseItem(item: Item, target: UOEntity)
```

**Parameters:**

- `item` (Item)
- `target` (UOEntity)

**Returns:** `Void`

#### Overload 3

```python
UseItem(item: Int32, target: UOEntity)
```

**Parameters:**

- `item` (Int32)
- `target` (UOEntity)

**Returns:** `Void`

#### Overload 4

```python
UseItem(item: Item, target: Int32)
```

**Parameters:**

- `item` (Item)
- `target` (Int32)

**Returns:** `Void`

#### Overload 5

```python
UseItem(itemSerial: Int32, targetSerial: Int32)
```

**Parameters:**

- `itemSerial` (Int32)
- `targetSerial` (Int32)

**Returns:** `Void`

#### Overload 6

```python
UseItem(itemserial: Int32)
```

**Parameters:**

- `itemserial` (Int32)

**Returns:** `Void`

#### Overload 7

```python
UseItem(item: Item)
```

**Parameters:**

- `item` (Item)

**Returns:** `Void`

### UseItemByID

```python
UseItemByID(itemid: Int32, color: Int32 = -1)
```

Use any item of a specific type, matching Item.ItemID. Optionally also of a specific color, matching Item.Hue.

**Parameters:**

- `itemid` (Int32): ItemID to be used.
- `color` (Int32): Color to be used. (default: -1, any)

**Returns:** `Boolean`

### WaitForContents

#### Overload 1

```python
WaitForContents(bag: Item, delay: Int32)
```

Open a container an wait for the Items to load, for a maximum amount of time.

**Parameters:**

- `bag` (Item): Container as Item object.
- `delay` (Int32): Maximum wait, in milliseconds.

**Returns:** `Boolean`

#### Overload 2

```python
WaitForContents(bag_serial: Int32, delay: Int32)
```

**Parameters:**

- `bag_serial` (Int32): Container as Item serial.
- `delay` (Int32): max time to wait for contents

**Returns:** `Boolean`

### WaitForProps

#### Overload 1

```python
WaitForProps(itemserial: Int32, delay: Int32)
```

If not updated, request to the Properties of an Item, and wait for a maximum amount of time.

**Parameters:**

- `itemserial` (Int32): Serial or Item read.
- `delay` (Int32): Maximum waiting time, in milliseconds.

**Returns:** `Void`

#### Overload 2

```python
WaitForProps(i: Item, delay: Int32)
```

**Parameters:**

- `i` (Item)
- `delay` (Int32)

**Returns:** `Void`

