# Statics

The Statics class provides access to informations about the Map, down to the individual tile.
When using this function it's important to remember the distinction between Land and Tile:
Land
----
For a given (X,Y,map) there can be only 1 (0 zero) Land item, and has 1 specific Z coordinate.
Tile
----
For a given (X,Y,map) there can be any number of Tile items.

## Properties

No properties available.

## Methods

### CheckDeedHouse

```python
CheckDeedHouse(x: Int32, y: Int32)
```

Check if the given Tile is occupied by a private house.
Need to be in-sight, on most servers the maximum distance is 18 tiles.

**Parameters:**

- `x` (Int32): X coordinate.
- `y` (Int32): Y coordinate.

**Returns:** `Boolean` - True: The tile is occupied - False: otherwise

### GetItemData

```python
GetItemData(StaticID: Int32)
```

**Parameters:**

- `StaticID` (Int32)

**Returns:** `ItemData`

### GetLandFlag

```python
GetLandFlag(staticID: Int32, flagname: String)
```

Land: Check Flag value of a given Land item.

**Parameters:**

- `staticID` (Int32): StaticID of a Land item.
- `flagname` (String): None
Translucent
Wall
Damaging
Impassable
Surface
Bridge
Window
NoShoot
Foliage
HoverOver
Roof
Door
Wet

**Returns:** `Boolean` - True: if the Flag is active - False: otherwise

### GetLandID

```python
GetLandID(x: Int32, y: Int32, map: Int32)
```

Land: Return the StaticID of the Land item, give the coordinates and map.

**Parameters:**

- `x` (Int32): X coordinate.
- `y` (Int32): Y coordinate.
- `map` (Int32): 0 = Felucca
1 = Trammel
2 = Ilshenar
3 = Malas
4 = Tokuno
5 = TerMur

**Returns:** `Int32` - Return the StaticID of the Land tile

### GetLandName

```python
GetLandName(StaticID: Int32)
```

Land: Get the name of a Land item given the StaticID.

**Parameters:**

- `StaticID` (Int32): Land item StaticID.

**Returns:** `String` - The name of the Land item.

### GetLandZ

```python
GetLandZ(x: Int32, y: Int32, map: Int32)
```

Land: Return the Z coordinate (height) of the Land item, give the coordinates and map.

**Parameters:**

- `x` (Int32): X coordinate.
- `y` (Int32): Y coordinate.
- `map` (Int32): 0 = Felucca
1 = Trammel
2 = Ilshenar
3 = Malas
4 = Tokuno
5 = TerMur

**Returns:** `Int32`

### GetStaticsLandInfo

```python
GetStaticsLandInfo(x: Int32, y: Int32, map: Int32)
```

Land: Return a TileInfo representing the Land item for a given X,Y, map.

**Parameters:**

- `x` (Int32): X coordinate.
- `y` (Int32): Y coordinate.
- `map` (Int32): 0 = Felucca
1 = Trammel
2 = Ilshenar
3 = Malas
4 = Tokuno
5 = TerMur

**Returns:** `Statics.TileInfo` - A single TileInfo related a Land item.

### GetStaticsTileInfo

```python
GetStaticsTileInfo(x: Int32, y: Int32, map: Int32)
```

Tile: Return a list of TileInfo representing the Tile items for a given X,Y, map.

**Parameters:**

- `x` (Int32): X coordinate.
- `y` (Int32): Y coordinate.
- `map` (Int32): 0 = Felucca
1 = Trammel
2 = Ilshenar
3 = Malas
4 = Tokuno
5 = TerMur

**Returns:** `List[Statics.TileInfo]` - A list of TileInfo related to Tile items.

### GetTileFlag

```python
GetTileFlag(StaticID: Int32, flagname: String)
```

Tile: Check Flag value of a given Tile item.

**Parameters:**

- `StaticID` (Int32): StaticID of a Tile item.
- `flagname` (String): None
Translucent
Wall
Damaging
Impassable
Surface
Bridge
Window
NoShoot
Foliage
HoverOver
Roof
Door
Wet

**Returns:** `Boolean` - True: if the Flag is active - False: otherwise

### GetTileHeight

```python
GetTileHeight(StaticID: Int32)
```

Tile: Get hight of a Tile item, in Z coordinate reference.

**Parameters:**

- `StaticID` (Int32): Tile item StaticID.

**Returns:** `Int32` - Height of a Tile item.

### GetTileName

```python
GetTileName(StaticID: Int32)
```

Tile: Get the name of a Tile item given the StaticID.

**Parameters:**

- `StaticID` (Int32): Tile item StaticID.

**Returns:** `String` - The name of the Land item.

