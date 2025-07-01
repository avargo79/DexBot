# Target

The Target class provides various methods for targeting Land, Items and Mobiles in game.

## Properties

No properties available.

## Methods

### AttackTargetFromList

```python
AttackTargetFromList(target_name: String)
```

Attack Target from gui filter selector, in Targetting tab.

**Parameters:**

- `target_name` (String)

**Returns:** `Void`

### Cancel

```python
Cancel()
```

Cancel the current target.

**Returns:** `Void`

### ClearLast

```python
ClearLast()
```

Clear the last target.

**Returns:** `Void`

### ClearLastAttack

```python
ClearLastAttack()
```

Clear the last attacked target

**Returns:** `Void`

### ClearLastandQueue

```python
ClearLastandQueue()
```

Clear last target and target queue.

**Returns:** `Void`

### ClearQueue

```python
ClearQueue()
```

Clear Queue Target.

**Returns:** `Void`

### GetLast

```python
GetLast()
```

Get serial number of last target

**Returns:** `Int32` - Serial as number.

### GetLastAttack

```python
GetLastAttack()
```

Get serial number of last attack target

**Returns:** `Int32` - Serial as number.

### GetTargetFromList

```python
GetTargetFromList(target_name: String)
```

Get Mobile object from GUI filter selector, in Targetting tab.

**Parameters:**

- `target_name` (String): Name of the target filter.

**Returns:** `Mobile` - Mobile object matching. None: not found

### HasTarget

```python
HasTarget(targetFlag: String = Any)
```

Get the status of the in-game target cursor
Optionally specify the target flag and check if the cursor is "Beneficial", "Harmful", or "Neutral".

**Parameters:**

- `targetFlag` (String): The target flag to check for can be "Any", "Beneficial", "Harmful", or "Neutral".

**Returns:** `Boolean` - True if the client has a target cursor and the optional flag matches; otherwise, false.

### Last

```python
Last()
```

Execute the target on the last Item or Mobile targeted.

**Returns:** `Void`

### LastQueued

```python
LastQueued()
```

Enqueue the next target on the last Item or Mobile targeted.

**Returns:** `Void`

### LastUsedObject

```python
LastUsedObject()
```

Returns the serial of last object used by the player.

**Returns:** `Int32`

### PerformTargetFromList

```python
PerformTargetFromList(target_name: String)
```

Execute Target from GUI filter selector, in Targetting tab.

**Parameters:**

- `target_name` (String): Name of the target filter.

**Returns:** `Void`

### PromptGroundTarget

```python
PromptGroundTarget(message: String = Select Ground Position, color: Int32 = 945)
```

Prompt a target in-game, wait for the Player to select the ground. Can also specific a text message for prompt.

**Parameters:**

- `message` (String): Hint on what to select.
- `color` (Int32): Color of the message. (default: 945, gray)

**Returns:** `Point3D` - A Point3D object, containing the X,Y,Z coordinate

### PromptTarget

```python
PromptTarget(message: String = Select Item or Mobile, color: Int32 = 945)
```

Prompt a target in-game, wait for the Player to select an Item or a Mobile. Can also specific a text message for prompt.

**Parameters:**

- `message` (String): Hint on what to select.
- `color` (Int32): Color of the message. (default: 945, gray)

**Returns:** `Int32` - Serial of the selected object.

### Self

```python
Self()
```

Execute the target on the Player.

**Returns:** `Void`

### SelfQueued

```python
SelfQueued()
```

Enqueue the next target on the Player.

**Returns:** `Void`

### SetLast

#### Overload 1

```python
SetLast(serial: Int32, wait: Boolean = True)
```

Set the last target to specific mobile, using the serial.

**Parameters:**

- `serial` (Int32): Serial of the Mobile.
- `wait` (Boolean): Wait confirmation from the server.

**Returns:** `Void`

#### Overload 2

```python
SetLast(mob: Mobile)
```

**Parameters:**

- `mob` (Mobile)

**Returns:** `Void`

### SetLastTargetFromList

```python
SetLastTargetFromList(target_name: String)
```

Set Last Target from GUI filter selector, in Targetting tab.

**Parameters:**

- `target_name` (String): Name of the target filter.

**Returns:** `Void`

### TargetExecute

#### Overload 1

```python
TargetExecute(x: Int32, y: Int32, z: Int32, StaticID: Int32)
```

Execute target on specific serial, item, mobile, X Y Z point.

**Parameters:**

- `x` (Int32): X coordinate.
- `y` (Int32): Y coordinate.
- `z` (Int32): Z coordinate.
- `StaticID` (Int32): ID of Land/Tile

**Returns:** `Void`

#### Overload 2

```python
TargetExecute(x: Int32, y: Int32, z: Int32)
```

**Parameters:**

- `x` (Int32)
- `y` (Int32)
- `z` (Int32)

**Returns:** `Void`

#### Overload 3

```python
TargetExecute(serial: Int32)
```

**Parameters:**

- `serial` (Int32): Serial of the Target

**Returns:** `Void`

#### Overload 4

```python
TargetExecute(entity: UOEntity)
```

Targets the Mobil or Item specified

**Parameters:**

- `entity` (UOEntity): object can be a Mobil or an Item.

**Returns:** `Void`

### TargetExecuteRelative

#### Overload 1

```python
TargetExecuteRelative(mobile: Mobile, offset: Int32)
```

Execute target on specific land point with offset distance from Mobile. Distance is calculated by target Mobile.Direction.

**Parameters:**

- `mobile` (Mobile): Mobile object to target.
- `offset` (Int32): Distance from the target.

**Returns:** `Void`

#### Overload 2

```python
TargetExecuteRelative(serial: Int32, offset: Int32)
```

**Parameters:**

- `serial` (Int32): Serial of the mobile
- `offset` (Int32): +- distance to offset from the mobile identified with serial

**Returns:** `Void`

### TargetResource

#### Overload 1

```python
TargetResource(item_serial: Int32, resource_number: Int32)
```

Find and target a resource using the specified item.

**Parameters:**

- `item_serial` (Int32): Item object to use.
- `resource_number` (Int32): Resource as standard name or custom number
               0: ore
               1: sand
               2: wood
               3: graves
               4: red_mushrooms
               n: custom

**Returns:** `Void`

#### Overload 2

```python
TargetResource(item_serial: Int32, resource_name: String)
```

**Parameters:**

- `item_serial` (Int32)
- `resource_name` (String)

**Returns:** `Void`

#### Overload 3

```python
TargetResource(item: Item, resouce_name: String)
```

**Parameters:**

- `item` (Item): Item object to use.
- `resouce_name` (String): name of the resource to be targeted. ore, sand, wood, graves, red mushroom

**Returns:** `Void`

#### Overload 4

```python
TargetResource(item: Item, resoruce_number: Int32)
```

**Parameters:**

- `item` (Item)
- `resoruce_number` (Int32)

**Returns:** `Void`

### TargetType

```python
TargetType(graphic: Int32, color: Int32 = -1, range: Int32 = 20, selector: String = Nearest, notoriety: List[Byte] = None)
```

**Parameters:**

- `graphic` (Int32)
- `color` (Int32)
- `range` (Int32)
- `selector` (String)
- `notoriety` (List[Byte])

**Returns:** `Boolean`

### WaitForTarget

```python
WaitForTarget(delay: Int32, noshow: Boolean = False)
```

Wait for the cursor to show the target, pause the script for a maximum amount of time. and optional flag True or False. True Not show cursor, false show it

**Parameters:**

- `delay` (Int32): Maximum amount to wait, in milliseconds
- `noshow` (Boolean): Pevent the cursor to display the target.

**Returns:** `Boolean`

### WaitForTargetOrFizzle

```python
WaitForTargetOrFizzle(delay: Int32 = 5000, noshow: Boolean = False)
```

Wait for the cursor to show the target, or the sound for fizzle (0x5c) or pause the script for a maximum amount of time. 
and an optional flag True or False. True Not show cursor, false show it

**Parameters:**

- `delay` (Int32): Maximum amount to wait, in milliseconds
- `noshow` (Boolean): Prevent the cursor to display the target.

**Returns:** `Boolean`

