# Misc

The Misc class contains general purpose functions of common use.

## Properties

No properties available.

## Methods

### AllSharedValue

```python
AllSharedValue()
```

**Returns:** `List[String]`

### AppendNotDupToFile

```python
AppendNotDupToFile(fileName: String, lineOfData: String)
```

Allows creation and append of a file within RE ValidLocations.
For OSI/RE this is only the RE directory / sub-directories
For CUO/RE this is only CUO or RE directory / sub-directories
The filename MUST end in a limited file suffix list
Checks to see if an identical line is already in the file, and does not add if it exists

**Parameters:**

- `fileName` (String)
- `lineOfData` (String)

**Returns:** `Boolean`

### AppendToFile

```python
AppendToFile(fileName: String, lineOfData: String)
```

Allows creation and append of a file within RE ValidLocations.
For OSI/RE this is only the RE directory / sub-directories
For CUO/RE this is only CUO or RE directory / sub-directories
The filename MUST end in a limited file suffix list

**Parameters:**

- `fileName` (String)
- `lineOfData` (String)

**Returns:** `Boolean`

### Beep

```python
Beep()
```

Play Beep system sound.

**Returns:** `Void`

### CancelPrompt

```python
CancelPrompt()
```

Cancel a prompt request.

**Returns:** `Void`

### CaptureNow

```python
CaptureNow()
```

Creates a snapshot of the current UO window.

**Returns:** `String` - The path to the saved file.

### ChangeProfile

```python
ChangeProfile(profileName: String)
```

Allow the scripted loading of a profile

**Parameters:**

- `profileName` (String): Name of profile to load

**Returns:** `Void`

### CheckIgnoreObject

#### Overload 1

```python
CheckIgnoreObject(serial: Int32)
```

Check object from ignore list, return true if present. Can check Serial, Items or Mobiles

**Parameters:**

- `serial` (Int32): Serial to check.

**Returns:** `Boolean` - True: Object is ignored - False: otherwise.

#### Overload 2

```python
CheckIgnoreObject(entity: UOEntity)
```

**Parameters:**

- `entity` (UOEntity)

**Returns:** `Boolean`

### CheckSharedValue

```python
CheckSharedValue(name: String)
```

Check if a shared value exixts.

**Parameters:**

- `name` (String): Name of the value.

**Returns:** `Boolean` - True: Shared value exists - False: otherwise.

### ClearDragQueue

```python
ClearDragQueue()
```

Clear the Drag-n-Drop queue.

**Returns:** `Void`

### ClearIgnore

```python
ClearIgnore()
```

Clear ignore list from all object

**Returns:** `Void`

### CloseBackpack

```python
CloseBackpack()
```

Close the backpack. 
(OSI client only, no ClassicUO)

**Returns:** `Void`

### CloseMenu

```python
CloseMenu()
```

Close opened Old Menu.

**Returns:** `Void`

### ConfigDirectory

```python
ConfigDirectory()
```

Get the full path to the Config Directory.

**Returns:** `String` - Full path to the Scripts Directory.

### ContextReply

#### Overload 1

```python
ContextReply(serial: Int32, respone_num: Int32)
```

Respond to a context menu on mobile or item. Menu ID is base zero, or can use string of menu text.

**Parameters:**

- `serial` (Int32): Serial of the Entity
- `respone_num` (Int32): Poition of the option in the menu. Starts from 0.

**Returns:** `Void`

#### Overload 2

```python
ContextReply(serial: Int32, menu_name: String)
```

**Parameters:**

- `serial` (Int32): serial number of the item to get a context menu from
- `menu_name` (String): Name of the Entry as wirtten in-game.

**Returns:** `Void`

#### Overload 3

```python
ContextReply(entity: UOEntity, menu_num: Int32)
```

**Parameters:**

- `entity` (UOEntity)
- `menu_num` (Int32)

**Returns:** `Void`

#### Overload 4

```python
ContextReply(entity: UOEntity, menu_name: String)
```

**Parameters:**

- `entity` (UOEntity)
- `menu_name` (String)

**Returns:** `Void`

### DataDirectory

```python
DataDirectory()
```

Get the full path to the Config Directory.

**Returns:** `String` - Full path to the Config Directory.

### DeleteFile

```python
DeleteFile(fileName: String)
```

Allows deletion of a file within RE ValidLocations.
For OSI/RE this is only the RE directory / sub-directories
For CUO/RE this is only CUO or RE directory / sub-directories
The filename MUST end in a limited file suffix list

**Parameters:**

- `fileName` (String)

**Returns:** `Boolean`

### Disconnect

```python
Disconnect()
```

Force client to disconnect.

**Returns:** `Void`

### Distance

```python
Distance(X1: Int32, Y1: Int32, X2: Int32, Y2: Int32)
```

Returns the UO distance between the 2 sets of co-ordinates.

**Parameters:**

- `X1` (Int32): X co-ordinate of first place.
- `Y1` (Int32): Y co-ordinate of first place.
- `X2` (Int32): X co-ordinate of second place.
- `Y2` (Int32): Y co-ordinate of second place.

**Returns:** `Int32`

### DistanceSqrt

```python
DistanceSqrt(point_a: Point3D, point_b: Point3D)
```

Compute the distance between 2 Point3D using pythagorian.

**Parameters:**

- `point_a` (Point3D): First coordinates.
- `point_b` (Point3D): Second coordinates.

**Returns:** `Double`

### ExportPythonAPI

```python
ExportPythonAPI(path: String = None, pretty: Boolean = True)
```

Return a string containing list RE Python API list in JSON format.

**Parameters:**

- `path` (String): Name of the output file. (default: Config/AutoComplete.json )
- `pretty` (Boolean): Print a readable JSON. (default: True )

**Returns:** `Void`

### FilterSeason

```python
FilterSeason(enable: Boolean, seasonFlag: UInt32)
```

Enable or disable the Seasons filter forcing a specific season
Season filter state will be saved on logout but not the season flag that will be recovered.

**Parameters:**

- `enable` (Boolean): True: enable seasons filter
- `seasonFlag` (UInt32): 0: Spring (default fallback)
1: Summer
2: Fall
3: Winter
4: Desolation

**Returns:** `Void`

### FocusUOWindow

```python
FocusUOWindow()
```

Set UoClient window in focus or restore if minimized.

**Returns:** `Void`

### GetContPosition

```python
GetContPosition()
```

Get the position of the currently active Gump/Container.
(OSI client only, no ClassicUO)

**Returns:** `Point` - Return X,Y coordinates as a Point2D

### GetMapInfo

```python
GetMapInfo(serial: UInt32)
```

Get MapInfo about a Mobile or Item using the serial

**Parameters:**

- `serial` (UInt32): Serial of the object.

**Returns:** `Misc.MapInfo` - A MapInfo object.

### GetMenuTitle

```python
GetMenuTitle()
```

Get the title of title for open Old Menu.

**Returns:** `String` - Text of the title.

### GetWindowSize

```python
GetWindowSize()
```

Get a Rectangle representing the window size.
See also: https://docs.microsoft.com/dotnet/api/system.drawing.rectangle

**Returns:** `Rectangle` - Rectangle object. Properties: X, Y, Width, Height.

### HasMenu

```python
HasMenu()
```

Check if an Old Menu is open.

**Returns:** `Boolean` - True: is open - False: otherwise

### HasPrompt

```python
HasPrompt()
```

Check if have a prompt request.

**Returns:** `Boolean` - True: there is a prompt - False: otherwise

### HasQueryString

```python
HasQueryString()
```

Check if a have a query string menu opened, return true or false.

**Returns:** `Boolean` - True: Has quesy - False: otherwise.

### IgnoreObject

#### Overload 1

```python
IgnoreObject(serial: Int32)
```

Add an entiry to the ignore list. Can ignore Serial, Items or Mobiles.

**Parameters:**

- `serial` (Int32): Serial to ignore.

**Returns:** `Void`

#### Overload 2

```python
IgnoreObject(entity: UOEntity)
```

**Parameters:**

- `entity` (UOEntity)

**Returns:** `Void`

### Inspect

```python
Inspect()
```

Prompt the user with a Target. Open the inspector for the selected target.

**Returns:** `Void`

### IsItem

```python
IsItem(serial: UInt32)
```

Determine if the serial is an item

**Parameters:**

- `serial` (UInt32): Serial number of object to test is Item

**Returns:** `Boolean` - Return True - is an Item False - is not an item

### IsMobile

```python
IsMobile(serial: UInt32)
```

Determine if the serial is a mobile

**Parameters:**

- `serial` (UInt32): Serial number of object to test is Mobile

**Returns:** `Boolean` - Return True - is a mobile False - is not a mobile

### LastHotKey

```python
LastHotKey()
```

Returns the latest HotKey recorded by razor as HotKeyEvent object.

**Returns:** `HotKeyEvent`

### LeftMouseClick

```python
LeftMouseClick(xpos: Int32, ypos: Int32, clientCoords: Boolean = True)
```

Perform a phisical left click on the window using Windows API.
Is possible to use abolute Screen Coordinates by setting clientCoords=False.

**Parameters:**

- `xpos` (Int32): X click coordinate.
- `ypos` (Int32): Y click coordinate.
- `clientCoords` (Boolean): True: Client coordinates.- False:Screen coordinates (default: True, client).

**Returns:** `Void`

### MenuContain

```python
MenuContain(text: String)
```

Search in open Old Menu if contains a specific text.

**Parameters:**

- `text` (String): Text to search.

**Returns:** `Boolean` - True: Text found - False: otherwise.

### MenuResponse

```python
MenuResponse(text: String)
```

Perform a menu response by subitem name. If item not exist close menu.

**Parameters:**

- `text` (String): Name of subitem to respond.

**Returns:** `Void`

### MouseLocation

```python
MouseLocation()
```

Returns a point with the X and Y coordinates of the mouse relative to the UO Window

**Returns:** `Point` - Return X,Y coords as Point object.

### MouseMove

```python
MouseMove(posX: Int32, posY: Int32)
```

Moves the mouse pointer to the position X,Y relative to the UO window

**Parameters:**

- `posX` (Int32): X screen coordinate.
- `posY` (Int32): Y screen coordinate.

**Returns:** `Void`

### NextContPosition

```python
NextContPosition(x: Int32, y: Int32)
```

Return the X,Y of the next container, relative to the game window.
(OSI client only, no ClassicUO)

**Parameters:**

- `x` (Int32): X coordinate.
- `y` (Int32): Y coordinate.

**Returns:** `Void`

### NoOperation

```python
NoOperation()
```

Just do nothing and enjot the present moment.

**Returns:** `Void`

### NoRunStealthStatus

```python
NoRunStealthStatus()
```

Get the status of "No Run When Stealth" via scripting.

**Returns:** `Boolean` - True: Open is active - False: otherwise.

### NoRunStealthToggle

```python
NoRunStealthToggle(enable: Boolean)
```

Set "No Run When Stealth" via scripting. Changes via scripting are not persistents.

**Parameters:**

- `enable` (Boolean): True: enable the option.

**Returns:** `Void`

### OpenPaperdoll

```python
OpenPaperdoll()
```

Open the backpack. 
(OSI client only, no ClassicUO)

**Returns:** `Void`

### Pause

```python
Pause(millisec: Int32)
```

Pause the script for a given amount of time.

**Parameters:**

- `millisec` (Int32): Pause duration, in milliseconds.

**Returns:** `Void`

### PetRename

#### Overload 1

```python
PetRename(serial: Int32, name: String)
```

Rename a specific pet.

**Parameters:**

- `serial` (Int32): Serial of the pet.
- `name` (String): New name to set.

**Returns:** `Void`

#### Overload 2

```python
PetRename(mob: Mobile, name: String)
```

**Parameters:**

- `mob` (Mobile): Mobile object representing the pet.
- `name` (String): name to assign to the pet

**Returns:** `Void`

### PlaySound

```python
PlaySound(sound: Int32, x: Int32, y: Int32, z: Int32)
```

Send a sound to the client.

**Parameters:**

- `sound` (Int32): The sound to play.
- `x` (Int32): The x point to send sound to.
- `y` (Int32): The y point to send sound to.
- `z` (Int32): The z point to send sound to.

**Returns:** `Void`

### QueryStringResponse

```python
QueryStringResponse(okcancel: Boolean, response: String)
```

Perform a query string response by ok or cancel button and specific response string.

**Parameters:**

- `okcancel` (Boolean): OK Button
- `response` (String): Cancel Button

**Returns:** `Void`

### RazorDirectory

```python
RazorDirectory()
```

Get the full path to the main Razor Enhanced folder.
This path maybe be different from the Python starting folder when RE is loaded as plugin (ex: ClassicUO)

**Returns:** `String` - Path as text

### ReadSharedValue

```python
ReadSharedValue(name: String)
```

Get a Shared Value, if value not exist return null.
Shared values are accessible by every script.

**Parameters:**

- `name` (String): Name of the value.

**Returns:** `Object` - The stored object.

### RemoveLineInFile

```python
RemoveLineInFile(fileName: String, lineOfData: String)
```

Allows removal of a line in a file within RE ValidLocations.
For OSI/RE this is only the RE directory / sub-directories
For CUO/RE this is only CUO or RE directory / sub-directories
The filename MUST end in a limited file suffix list
Checks to see if an identical line is in the file, and if it exists, it is removed and file written

**Parameters:**

- `fileName` (String)
- `lineOfData` (String)

**Returns:** `Boolean`

### RemoveSharedValue

```python
RemoveSharedValue(name: String)
```

Remove a Shared Value.

**Parameters:**

- `name` (String): Name of the value.

**Returns:** `Void`

### ResetPrompt

```python
ResetPrompt()
```

Reset a prompt response.

**Returns:** `Void`

### ResponsePrompt

```python
ResponsePrompt(text: String)
```

Response a prompt request. Often used to rename runes and similar.

**Parameters:**

- `text` (String): Text of the response.

**Returns:** `Void`

### Resync

```python
Resync()
```

Trigger a client ReSync.

**Returns:** `Void`

### RightMouseClick

```python
RightMouseClick(xpos: Int32, ypos: Int32, clientCoords: Boolean = True)
```

Perform a phisical Right click on the window.

**Parameters:**

- `xpos` (Int32): X click coordinate.
- `ypos` (Int32): Y click coordinate.
- `clientCoords` (Boolean): True: Client coordinates - False: Screen coordinates (default: True, client).

**Returns:** `Void`

### ScriptCurrent

```python
ScriptCurrent(fullpath: Boolean = True)
```

Returns the path of the current script.

**Parameters:**

- `fullpath` (Boolean): True:Returns the full path. False: Returns the filename. (Dafault: true)

**Returns:** `String`

### ScriptDirectory

```python
ScriptDirectory()
```

Get the full path to the Scripts Directory.

**Returns:** `String` - Full path to the Scripts Directory.

### ScriptIsSuspended

```python
ScriptIsSuspended(scriptfile: String)
```

Get status of script if is suspended or not, Script must be present in script grid.

**Parameters:**

- `scriptfile` (String)

**Returns:** `Boolean` - True: Script is suspended - False: otherwise.

### ScriptResume

```python
ScriptResume(scriptfile: String)
```

Resume a script by file name, Script must be present in script grid.

**Parameters:**

- `scriptfile` (String): Name of the script.

**Returns:** `Void`

### ScriptRun

```python
ScriptRun(scriptfile: String)
```

Run a script by file name, Script must be present in script grid.

**Parameters:**

- `scriptfile` (String): Name of the script.

**Returns:** `Void`

### ScriptStatus

```python
ScriptStatus(scriptfile: String)
```

Get status of script if running or not, Script must be present in script grid.

**Parameters:**

- `scriptfile` (String)

**Returns:** `Boolean` - True: Script is running - False: otherwise.

### ScriptStop

```python
ScriptStop(scriptfile: String)
```

Stop a script by file name, Script must be present in script grid.

**Parameters:**

- `scriptfile` (String): Name of the script.

**Returns:** `Void`

### ScriptStopAll

```python
ScriptStopAll(skipCurrent: Boolean = False)
```

Stop all script running.

**Parameters:**

- `skipCurrent` (Boolean): True: Stop all scripts, but the current one - False: stop all scripts. (Dafault: false)

**Returns:** `Void`

### ScriptSuspend

```python
ScriptSuspend(scriptfile: String)
```

Suspend a script by file name, Script must be present in script grid.

**Parameters:**

- `scriptfile` (String): Name of the script.

**Returns:** `Void`

### SendMessage

#### Overload 1

```python
SendMessage(msg: String, color: Int32, wait: Boolean)
```

Send a message to the client.

**Parameters:**

- `msg` (String): The object to print.
- `color` (Int32): Color of the message.
- `wait` (Boolean): True: Wait for confimation. - False: Returns instatnly.

**Returns:** `Void`

#### Overload 2

```python
SendMessage(obj: Object, color: Int32)
```

**Parameters:**

- `obj` (Object)
- `color` (Int32)

**Returns:** `Void`

#### Overload 3

```python
SendMessage(num: Int32, color: Int32)
```

**Parameters:**

- `num` (Int32)
- `color` (Int32)

**Returns:** `Void`

#### Overload 4

```python
SendMessage(num: UInt32, color: Int32)
```

**Parameters:**

- `num` (UInt32)
- `color` (Int32)

**Returns:** `Void`

#### Overload 5

```python
SendMessage(msg: Boolean, color: Int32)
```

**Parameters:**

- `msg` (Boolean)
- `color` (Int32)

**Returns:** `Void`

#### Overload 6

```python
SendMessage(msg: Double, color: Int32)
```

**Parameters:**

- `msg` (Double)
- `color` (Int32)

**Returns:** `Void`

#### Overload 7

```python
SendMessage(msg: String, wait: Boolean = True)
```

**Parameters:**

- `msg` (String)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 8

```python
SendMessage(num: Int32)
```

**Parameters:**

- `num` (Int32)

**Returns:** `Void`

#### Overload 9

```python
SendMessage(obj: Object)
```

**Parameters:**

- `obj` (Object)

**Returns:** `Void`

#### Overload 10

```python
SendMessage(num: UInt32)
```

**Parameters:**

- `num` (UInt32)

**Returns:** `Void`

#### Overload 11

```python
SendMessage(msg: Boolean)
```

**Parameters:**

- `msg` (Boolean)

**Returns:** `Void`

#### Overload 12

```python
SendMessage(msg: Double)
```

**Parameters:**

- `msg` (Double)

**Returns:** `Void`

#### Overload 13

```python
SendMessage(num: Single)
```

**Parameters:**

- `num` (Single)

**Returns:** `Void`

### SendToClient

```python
SendToClient(keys: String)
```

Send to the client a list of keystrokes. Can contain control characters: 
- Send Control+Key: ctrl+u: ^u
- Send ENTER: {Enter}
Note: some keys don't work with ClassicUO (es: {Enter} )

**Parameters:**

- `keys` (String): List of keys.

**Returns:** `Void`

### SetSharedValue

```python
SetSharedValue(name: String, value: Object)
```

Set a Shared Value by specific name, if value exist he repalce value.
Shared values are accessible by every script.

**Parameters:**

- `name` (String): Name of the value.
- `value` (Object): Value to set.

**Returns:** `Void`

### ShardName

```python
ShardName()
```

Get the name of the shard.

**Returns:** `String` - Name of the shard

### UnIgnoreObject

#### Overload 1

```python
UnIgnoreObject(serial: Int32)
```

Remove object from ignore list. Can remove serial, items or mobiles

**Parameters:**

- `serial` (Int32): Serial to unignore.

**Returns:** `Void`

#### Overload 2

```python
UnIgnoreObject(entity: UOEntity)
```

**Parameters:**

- `entity` (UOEntity): Item to unignore.

**Returns:** `Void`

### UseContextMenu

```python
UseContextMenu(serial: Int32, choice: String, delay: Int32)
```

Open and click the option of Context menu, given the serial of Mobile or Item, via packets.

**Parameters:**

- `serial` (Int32): Serial of the Item or Mobile.
- `choice` (String): Option as Text or integer.
- `delay` (Int32): Maximum wait for the action to complete.

**Returns:** `Boolean` - True: Optiona selected succesfully - False: otherwise.

### WaitForContext

#### Overload 1

```python
WaitForContext(serial: Int32, delay: Int32, showContext: Boolean = False)
```

Return the List entry of a Context menu, of Mobile or Item objects.
The function will ask the server for the List and wait for a maximum amount of time.

**Parameters:**

- `serial` (Int32): Serial of the entity.
- `delay` (Int32): Maximum wait.
- `showContext` (Boolean): Show context menu in-game. (default: True)

**Returns:** `List[Misc.Context]` - A List of Context objects.

#### Overload 2

```python
WaitForContext(mob: Mobile, delay: Int32, showContext: Boolean = False)
```

**Parameters:**

- `mob` (Mobile): Entity as Item object.
- `delay` (Int32): max time to wait for context
- `showContext` (Boolean)

**Returns:** `List[Misc.Context]`

#### Overload 3

```python
WaitForContext(itm: Item, delay: Int32, showContext: Boolean = False)
```

**Parameters:**

- `itm` (Item): Entity as Item object.
- `delay` (Int32): max time to wait for context
- `showContext` (Boolean)

**Returns:** `List[Misc.Context]`

### WaitForMenu

```python
WaitForMenu(delay: Int32)
```

Pause script until server send an Old Menu, for a maximum amount of time.

**Parameters:**

- `delay` (Int32): Maximum wait, in milliseconds.

**Returns:** `Boolean` - True: if the Old Menu is open - False: otherwise.

### WaitForPrompt

```python
WaitForPrompt(delay: Int32)
```

Wait for a prompt for a maximum amount of time.

**Parameters:**

- `delay` (Int32): Maximum wait time.

**Returns:** `Boolean` - True: Prompt is present - False: otherwise

### WaitForQueryString

```python
WaitForQueryString(delay: Int32)
```

Pause script until server send query string request, for a maximum amount of time.

**Parameters:**

- `delay` (Int32): Maximum wait, in milliseconds.

**Returns:** `Boolean` - True: if player has a query - False: otherwise.

