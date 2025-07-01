# CUO

The CUO_Functions class contains invocation of CUO code using reflection
DANGER !!

## Properties

No properties available.

## Methods

### CloseGump

```python
CloseGump(serial: UInt32)
```

Invokes the Method close a gump

**Parameters:**

- `serial` (UInt32)

**Returns:** `Void`

### CloseMobileHealthBar

#### Overload 1

```python
CloseMobileHealthBar(mobileserial: Int32)
```

Closes a Mobile Status Gump of an Entity

**Parameters:**

- `mobileserial` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CloseMobileHealthBar(mobileserial: UInt32)
```

Closes a Mobile Status Gump of an Entity

**Parameters:**

- `mobileserial` (UInt32)

**Returns:** `Void`

### CloseMyStatusBar

```python
CloseMyStatusBar()
```

Invokes the Method to close your status bar gump inside the CUO code

**Returns:** `Void`

### CloseTMap

```python
CloseTMap()
```

Invokes the CloseWithRightClick function inside the CUO code
First T-Map is retrieved, and then only closed if it is a map
Returns True if a map was closed, else False

**Returns:** `Boolean`

### FollowMobile

```python
FollowMobile(mobileserial: UInt32)
```

Make the ClassicUO client follow the specific mobile.
            
This is the same behavior as alt + left-clicking, which normally
shows the overhead message "Now following."

**Parameters:**

- `mobileserial` (UInt32)

**Returns:** `Void`

### FollowOff

```python
FollowOff()
```

Stop the ClassicUO client from following, if it was following a
mobile.

**Returns:** `Void`

### Following

```python
Following()
```

Returns the status and target of the ClassicUO client's follow
behavior.

**Returns:** `ValueTuple[Boolean, UInt32]` - bool followingMode, uint followingTarget

### FreeView

```python
FreeView(free: Boolean)
```

Invokes the FreeView function inside the CUO code
First value is retrieved, and then only set if its not correct

**Parameters:**

- `free` (Boolean)

**Returns:** `Void`

### GetSetting

```python
GetSetting(settingName: String)
```

Retrieve Current CUO Setting

**Parameters:**

- `settingName` (String)

**Returns:** `String`

### GoToMarker

```python
GoToMarker(x: Int32, y: Int32)
```

Invokes the GoToMarker function inside the CUO code
Map must be open for this to work

**Parameters:**

- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

### LoadMarkers

```python
LoadMarkers()
```

Invokes the LoadMarkers function inside the CUO code
Map must be open for this to work

**Returns:** `Void`

### MoveGump

```python
MoveGump(serial: UInt32, x: Int32, y: Int32)
```

Invokes the Method move a gump or container if open.

**Parameters:**

- `serial` (UInt32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

### OpenContainerAt

#### Overload 1

```python
OpenContainerAt(bag: Item, x: Int32, y: Int32)
```

Set a location that CUO will open the container at

**Parameters:**

- `bag` (Item)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

#### Overload 2

```python
OpenContainerAt(bag: UInt32, x: Int32, y: Int32)
```

Set a location that CUO will open the container at

**Parameters:**

- `bag` (UInt32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

### OpenMobileHealthBar

#### Overload 1

```python
OpenMobileHealthBar(mobileserial: Int32, x: Int32, y: Int32, custom: Boolean)
```

Open a mobiles health bar at a specified location on the screen

**Parameters:**

- `mobileserial` (Int32)
- `x` (Int32)
- `y` (Int32)
- `custom` (Boolean)

**Returns:** `Void`

#### Overload 2

```python
OpenMobileHealthBar(mobileserial: UInt32, x: Int32, y: Int32, custom: Boolean)
```

Invokes the Method to open your status bar gump inside the CUO code

**Parameters:**

- `mobileserial` (UInt32)
- `x` (Int32)
- `y` (Int32)
- `custom` (Boolean)

**Returns:** `Void`

### OpenMyStatusBar

```python
OpenMyStatusBar(x: Int32, y: Int32)
```

Invokes the Method to open your status bar gump inside the CUO code

**Parameters:**

- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

### PlayMacro

```python
PlayMacro(macroName: String)
```

Play a CUO macro by name
Warning, limited testing !!

**Parameters:**

- `macroName` (String)

**Returns:** `Void`

### ProfilePropertySet

#### Overload 1

```python
ProfilePropertySet(propertyName: String, enable: Boolean)
```

Set a bool Config property in CUO by name

**Parameters:**

- `propertyName` (String)
- `enable` (Boolean)

**Returns:** `Void`

#### Overload 2

```python
ProfilePropertySet(propertyName: String, value: Int32)
```

Set a int Config property in CUO by name

**Parameters:**

- `propertyName` (String)
- `value` (Int32)

**Returns:** `Void`

#### Overload 3

```python
ProfilePropertySet(propertyName: String, value: String)
```

Set a string Config property in CUO by name

**Parameters:**

- `propertyName` (String)
- `value` (String)

**Returns:** `Void`

### SetGumpOpenLocation

```python
SetGumpOpenLocation(gumpserial: UInt32, x: Int32, y: Int32)
```

Set a location that CUO will open the next gump or container at

**Parameters:**

- `gumpserial` (UInt32)
- `x` (Int32)
- `y` (Int32)

**Returns:** `Void`

