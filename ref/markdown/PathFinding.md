# PathFinding

This class implements the PathFinding algorithm using A-Star.

## Properties

No properties available.

## Methods

### GetPath

```python
GetPath(dst_x: Int32, dst_y: Int32, ignoremob: Boolean)
```

Compute the path for the given destination and returns a list of Tile (coordinates).

**Parameters:**

- `dst_x` (Int32): Destination X.
- `dst_y` (Int32): Destination Y.
- `ignoremob` (Boolean): Ignores any mobiles with the path calculation.

**Returns:** `List[Tile]` - List of Tile objects, each holds a .X and .Y coordinates.

### Go

```python
Go(r: PathFinding.Route)
```

Check if a destination is reachable.

**Parameters:**

- `r` (PathFinding.Route): A customized Route object.

**Returns:** `Boolean` - True: if a destination is reachable.

### PathFindTo

#### Overload 1

```python
PathFindTo(x: Int32, y: Int32, z: Int32 = 0)
```

Go to the given coordinates using Razor pathfinding.

**Parameters:**

- `x` (Int32): X map coordinates or Point3D
- `y` (Int32): Y map coordinates
- `z` (Int32): Z map coordinates

**Returns:** `Void`

#### Overload 2

```python
PathFindTo(destination: Point3D)
```

Go to the given coordinates using Razor pathfinding.

**Parameters:**

- `destination` (Point3D)

**Returns:** `Void`

### RunPath

```python
RunPath(path: List[Tile], timeout: Single = -1, debugMessage: Boolean = False, useResync: Boolean = True)
```

**Parameters:**

- `path` (List[Tile])
- `timeout` (Single)
- `debugMessage` (Boolean)
- `useResync` (Boolean)

**Returns:** `Boolean`

### Tile

```python
Tile(x: Int32, y: Int32)
```

Create a Tile starting from X,Y coordinates (see PathFindig.RunPath)

**Parameters:**

- `x` (Int32): X coordinate
- `y` (Int32): Y coordinate

**Returns:** `Tile` - Returns a Tile object

### WalkPath

```python
WalkPath(path: List[Tile], timeout: Single = -1, debugMessage: Boolean = False, useResync: Boolean = True)
```

**Parameters:**

- `path` (List[Tile])
- `timeout` (Single)
- `debugMessage` (Boolean)
- `useResync` (Boolean)

**Returns:** `Boolean`

### runPath

```python
runPath(timeout: Single = -1, debugMessage: Boolean = False, useResync: Boolean = True)
```

**Parameters:**

- `timeout` (Single): Maximum amount of time to run the path. (default: -1, no limit)
- `debugMessage` (Boolean): Outputs a debug message.
- `useResync` (Boolean): ReSyncs the path calculation.

**Returns:** `Boolean` - True: if it finish the path in time. False: otherwise

### walkPath

```python
walkPath(timeout: Single = -1, debugMessage: Boolean = False, useResync: Boolean = True)
```

**Parameters:**

- `timeout` (Single)
- `debugMessage` (Boolean)
- `useResync` (Boolean)

**Returns:** `Boolean`

