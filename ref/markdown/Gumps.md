# Gumps

The Gumps class is used to read and interact with in-game gumps, via scripting.
NOTE
----
During development of scripts that involves interecting with Gumps, is often needed to know gumpids and buttonids.
For this purpose, can be particularly usefull to use *Inspect Gumps* and *Record*, top right, in the internal RE script editor.

## Properties

No properties available.

## Methods

### AddAlphaRegion

```python
AddAlphaRegion(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)

**Returns:** `Void`

### AddBackground

```python
AddBackground(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, gumpId: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `gumpId` (Int32)

**Returns:** `Void`

### AddButton

```python
AddButton(gd: Gumps.GumpData&@, x: Int32, y: Int32, normalID: Int32, pressedID: Int32, buttonID: Int32, type: Int32, param: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `normalID` (Int32)
- `pressedID` (Int32)
- `buttonID` (Int32)
- `type` (Int32)
- `param` (Int32)

**Returns:** `Void`

### AddCheck

```python
AddCheck(gd: Gumps.GumpData&@, x: Int32, y: Int32, inactiveID: Int32, activeID: Int32, initialState: Boolean, switchID: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `inactiveID` (Int32)
- `activeID` (Int32)
- `initialState` (Boolean)
- `switchID` (Int32)

**Returns:** `Void`

### AddGroup

```python
AddGroup(gd: Gumps.GumpData&@, group: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `group` (Int32)

**Returns:** `Void`

### AddHtml

#### Overload 1

```python
AddHtml(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, text: String, background: Boolean, scrollbar: Boolean)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `text` (String)
- `background` (Boolean)
- `scrollbar` (Boolean)

**Returns:** `Void`

#### Overload 2

```python
AddHtml(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, textID: Int32, background: Boolean, scrollbar: Boolean)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `textID` (Int32)
- `background` (Boolean)
- `scrollbar` (Boolean)

**Returns:** `Void`

### AddHtmlLocalized

#### Overload 1

```python
AddHtmlLocalized(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, number: Int32, args: String, color: Int32, background: Boolean, scrollbar: Boolean)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `number` (Int32)
- `args` (String)
- `color` (Int32)
- `background` (Boolean)
- `scrollbar` (Boolean)

**Returns:** `Void`

#### Overload 2

```python
AddHtmlLocalized(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, number: Int32, color: Int32, background: Boolean, scrollbar: Boolean)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `number` (Int32)
- `color` (Int32)
- `background` (Boolean)
- `scrollbar` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
AddHtmlLocalized(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, number: Int32, background: Boolean, scrollbar: Boolean)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `number` (Int32)
- `background` (Boolean)
- `scrollbar` (Boolean)

**Returns:** `Void`

### AddImage

#### Overload 1

```python
AddImage(gd: Gumps.GumpData&@, x: Int32, y: Int32, gumpId: Int32, hue: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `gumpId` (Int32)
- `hue` (Int32)

**Returns:** `Void`

#### Overload 2

```python
AddImage(gd: Gumps.GumpData&@, x: Int32, y: Int32, gumpId: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `gumpId` (Int32)

**Returns:** `Void`

### AddImageTiled

```python
AddImageTiled(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, gumpId: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `gumpId` (Int32)

**Returns:** `Void`

### AddImageTiledButton

#### Overload 1

```python
AddImageTiledButton(gd: Gumps.GumpData&@, x: Int32, y: Int32, normalID: Int32, pressedID: Int32, buttonID: Int32, type: Gumps.GumpButtonType, param: Int32, itemID: Int32, hue: Int32, width: Int32, height: Int32, localizedTooltip: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `normalID` (Int32)
- `pressedID` (Int32)
- `buttonID` (Int32)
- `type` (Gumps.GumpButtonType)
- `param` (Int32)
- `itemID` (Int32)
- `hue` (Int32)
- `width` (Int32)
- `height` (Int32)
- `localizedTooltip` (Int32)

**Returns:** `Void`

#### Overload 2

```python
AddImageTiledButton(gd: Gumps.GumpData&@, x: Int32, y: Int32, normalID: Int32, pressedID: Int32, buttonID: Int32, type: Gumps.GumpButtonType, param: Int32, itemID: Int32, hue: Int32, width: Int32, height: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `normalID` (Int32)
- `pressedID` (Int32)
- `buttonID` (Int32)
- `type` (Gumps.GumpButtonType)
- `param` (Int32)
- `itemID` (Int32)
- `hue` (Int32)
- `width` (Int32)
- `height` (Int32)

**Returns:** `Void`

### AddItem

#### Overload 1

```python
AddItem(gd: Gumps.GumpData&@, x: Int32, y: Int32, itemID: Int32, hue: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `itemID` (Int32)
- `hue` (Int32)

**Returns:** `Void`

#### Overload 2

```python
AddItem(gd: Gumps.GumpData&@, x: Int32, y: Int32, itemID: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `itemID` (Int32)

**Returns:** `Void`

### AddLabel

#### Overload 1

```python
AddLabel(gd: Gumps.GumpData&@, x: Int32, y: Int32, hue: Int32, text: String)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `hue` (Int32)
- `text` (String)

**Returns:** `Void`

#### Overload 2

```python
AddLabel(gd: Gumps.GumpData&@, x: Int32, y: Int32, hue: Int32, textID: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `hue` (Int32)
- `textID` (Int32)

**Returns:** `Void`

### AddLabelCropped

#### Overload 1

```python
AddLabelCropped(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, hue: Int32, text: String)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `hue` (Int32)
- `text` (String)

**Returns:** `Void`

#### Overload 2

```python
AddLabelCropped(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, hue: Int32, textID: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `hue` (Int32)
- `textID` (Int32)

**Returns:** `Void`

### AddPage

```python
AddPage(gd: Gumps.GumpData&@, page: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `page` (Int32)

**Returns:** `Void`

### AddRadio

```python
AddRadio(gd: Gumps.GumpData&@, x: Int32, y: Int32, inactiveID: Int32, activeID: Int32, initialState: Boolean, switchID: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `inactiveID` (Int32)
- `activeID` (Int32)
- `initialState` (Boolean)
- `switchID` (Int32)

**Returns:** `Void`

### AddSpriteImage

```python
AddSpriteImage(gd: Gumps.GumpData&@, x: Int32, y: Int32, gumpId: Int32, spriteX: Int32, spriteY: Int32, spriteW: Int32, spriteH: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `gumpId` (Int32)
- `spriteX` (Int32)
- `spriteY` (Int32)
- `spriteW` (Int32)
- `spriteH` (Int32)

**Returns:** `Void`

### AddTextEntry

#### Overload 1

```python
AddTextEntry(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, hue: Int32, entryID: Int32, initialText: String)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `hue` (Int32)
- `entryID` (Int32)
- `initialText` (String)

**Returns:** `Void`

#### Overload 2

```python
AddTextEntry(gd: Gumps.GumpData&@, x: Int32, y: Int32, width: Int32, height: Int32, hue: Int32, entryID: Int32, initialTextID: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `x` (Int32)
- `y` (Int32)
- `width` (Int32)
- `height` (Int32)
- `hue` (Int32)
- `entryID` (Int32)
- `initialTextID` (Int32)

**Returns:** `Void`

### AddTooltip

#### Overload 1

```python
AddTooltip(gd: Gumps.GumpData&@, cliloc: Int32, text: String)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `cliloc` (Int32)
- `text` (String)

**Returns:** `Void`

#### Overload 2

```python
AddTooltip(gd: Gumps.GumpData&@, number: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `number` (Int32)

**Returns:** `Void`

#### Overload 3

```python
AddTooltip(gd: Gumps.GumpData&@, text: String)
```

**Parameters:**

- `gd` (Gumps.GumpData&@)
- `text` (String)

**Returns:** `Void`

### AllGumpIDs

```python
AllGumpIDs()
```

**Returns:** `List[UInt32]`

### CloseGump

```python
CloseGump(gumpid: UInt32)
```

Close a specific Gump.

**Parameters:**

- `gumpid` (UInt32): ID of the gump

**Returns:** `Void`

### CreateGump

```python
CreateGump(movable: Boolean = True, closable: Boolean = True, disposable: Boolean = True, resizeable: Boolean = True)
```

Creates an initialized GumpData structure

**Parameters:**

- `movable` (Boolean): allow the gump to be moved
- `closable` (Boolean): allow the gump to be right clicked to close
- `disposable` (Boolean): allow the gump to be disposed (beats me what it does)
- `resizeable` (Boolean): allow the gump to be resized

**Returns:** `Gumps.GumpData`

### CurrentGump

```python
CurrentGump()
```

Return the ID of most recent, still open Gump.

**Returns:** `UInt32` - ID of gump.

### GetGumpData

```python
GetGumpData(gumpid: UInt32)
```

**Parameters:**

- `gumpid` (UInt32)

**Returns:** `Gumps.GumpData`

### GetGumpRawLayout

```python
GetGumpRawLayout(gumpid: UInt32)
```

Get the Raw layout (definition) of a specific gumpid

**Parameters:**

- `gumpid` (UInt32)

**Returns:** `String` - layout (definition) of the gump.

### GetGumpText

```python
GetGumpText(gumpid: UInt32)
```

Get the Text of a specific Gump.
It is the cliloc translation of the #s in the gump

**Parameters:**

- `gumpid` (UInt32)

**Returns:** `List[String]` - List of Text in the gump

### GetLine

```python
GetLine(gumpId: UInt32, line_num: Int32)
```

Get a specific DATA line from the gumpId if it exists. Filter by line number.
The textual strings are not considered

**Parameters:**

- `gumpId` (UInt32): gump id to get data from
- `line_num` (Int32): Number of the line.

**Returns:** `String` - Text content of the line. (empty: line not found)

### GetLineList

```python
GetLineList(gumpId: UInt32, dataOnly: Boolean = False)
```

Get all text from the specified Gump if still open

**Parameters:**

- `gumpId` (UInt32): gump id to get data from
- `dataOnly` (Boolean)

**Returns:** `List[String]` - Text of the gump.

### GetTextByID

```python
GetTextByID(gd: Gumps.GumpData, id: Int32)
```

**Parameters:**

- `gd` (Gumps.GumpData)
- `id` (Int32)

**Returns:** `String`

### HasGump

#### Overload 1

```python
HasGump(gumpId: UInt32)
```

**Parameters:**

- `gumpId` (UInt32)

**Returns:** `Boolean`

#### Overload 2

```python
HasGump()
```

Get status if have a gump open or not.

**Returns:** `Boolean` - True: There is a Gump open - False: otherwise.

### IsValid

```python
IsValid(gumpId: Int32)
```

Validates if the gumpid provided exists in the gump file

**Parameters:**

- `gumpId` (Int32): The id of the gump to check for in the gumps.mul file

**Returns:** `Boolean`

### LastGumpGetLine

```python
LastGumpGetLine(line_num: Int32)
```

Get a specific line from the most recent and still open Gump. Filter by line number.
The text constants on the gump ARE included in indexing

**Parameters:**

- `line_num` (Int32): Number of the line.

**Returns:** `String` - Text content of the line. (empty: line not found)

### LastGumpGetLineList

```python
LastGumpGetLineList()
```

Get all text from the most recent and still open Gump.

**Returns:** `List[String]` - Text of the gump.

### LastGumpRawLayout

```python
LastGumpRawLayout()
```

Get the raw layout (definition) of the most recent and still open Gump.

**Returns:** `String` - layout (definition) of the gump.

### LastGumpTextExist

```python
LastGumpTextExist(text: String)
```

Search for text inside the most recent and still open Gump.

**Parameters:**

- `text` (String): Text to search.

**Returns:** `Boolean` - True: Text found in active Gump - False: otherwise

### LastGumpTextExistByLine

```python
LastGumpTextExistByLine(line_num: Int32, text: String)
```

Search for text, in a spacific line of the most recent and still open Gump.

**Parameters:**

- `line_num` (Int32): Number of the line.
- `text` (String): Text to search.

**Returns:** `Boolean`

### LastGumpTile

```python
LastGumpTile()
```

Get the list of Gump Tile (! this documentation is a stub !)

**Returns:** `List[Int32]` - List of Gump Tile.

### ResetGump

```python
ResetGump()
```

Clean current status of Gumps.

**Returns:** `Void`

### SendAction

```python
SendAction(gumpid: UInt32, buttonid: Int32)
```

Send a Gump response by gumpid and buttonid.

**Parameters:**

- `gumpid` (UInt32): ID of the gump.
- `buttonid` (Int32): ID of the Button to press.

**Returns:** `Void`

### SendAdvancedAction

#### Overload 1

```python
SendAdvancedAction(gumpid: UInt32, buttonid: Int32, inSwitches: List[Int32], textlist_id: List[Int32], textlist_str: List[String])
```

**Parameters:**

- `gumpid` (UInt32)
- `buttonid` (Int32)
- `inSwitches` (List[Int32])
- `textlist_id` (List[Int32])
- `textlist_str` (List[String])

**Returns:** `Void`

#### Overload 2

```python
SendAdvancedAction(gumpid: UInt32, buttonid: Int32, switchlist_id: PythonList, textlist_id: PythonList, textlist_str: PythonList)
```

Send a Gump response, with gumpid and buttonid and advanced switch in gumps. 
This function is intended for more complex Gumps, with not only Buttons, but also Switches, CheckBoxes and Text fileds.

**Parameters:**

- `gumpid` (UInt32): ID of the gump.
- `buttonid` (Int32): ID of the Button.
- `switchlist_id` (PythonList): List of ID of ON/Active switches. (empty: all Switches OFF)
- `textlist_id` (PythonList): List of ID of Text fileds. (empty: all text fileds empty )
- `textlist_str` (PythonList): List of the contents of the Text fields, provided in the same order as textlist_id.

**Returns:** `Void`

#### Overload 3

```python
SendAdvancedAction(gumpid: UInt32, buttonid: Int32, textlist_id: List[Int32], textlist_str: List[String])
```

**Parameters:**

- `gumpid` (UInt32)
- `buttonid` (Int32)
- `textlist_id` (List[Int32])
- `textlist_str` (List[String])

**Returns:** `Void`

#### Overload 4

```python
SendAdvancedAction(gumpid: UInt32, buttonid: Int32, textlist_id: PythonList, textlist_str: PythonList)
```

This method can also be used only Text fileds, without Switches.

**Parameters:**

- `gumpid` (UInt32)
- `buttonid` (Int32)
- `textlist_id` (PythonList)
- `textlist_str` (PythonList)

**Returns:** `Void`

#### Overload 5

```python
SendAdvancedAction(gumpid: UInt32, buttonid: Int32, inSwitches: List[Int32])
```

**Parameters:**

- `gumpid` (UInt32)
- `buttonid` (Int32)
- `inSwitches` (List[Int32])

**Returns:** `Void`

#### Overload 6

```python
SendAdvancedAction(gumpid: UInt32, buttonid: Int32, switchs: PythonList)
```

This method can also be used only Switches, without Text fileds.

**Parameters:**

- `gumpid` (UInt32)
- `buttonid` (Int32)
- `switchs` (PythonList)

**Returns:** `Void`

### SendGump

#### Overload 1

```python
SendGump(gumpid: UInt32, serial: UInt32, x: UInt32, y: UInt32, gumpDefinition: String, gumpStrings: List[String])
```

**Parameters:**

- `gumpid` (UInt32)
- `serial` (UInt32)
- `x` (UInt32)
- `y` (UInt32)
- `gumpDefinition` (String)
- `gumpStrings` (List[String])

**Returns:** `Void`

#### Overload 2

```python
SendGump(gd: Gumps.GumpData, x: UInt32, y: UInt32)
```

Sends a gump using an existing GumpData structure

**Parameters:**

- `gd` (Gumps.GumpData)
- `x` (UInt32)
- `y` (UInt32)

**Returns:** `Void`

### WaitForGump

```python
WaitForGump(gumpid: UInt32, delay: Int32)
```

Waits for a specific Gump to appear, for a maximum amount of time. If gumpid is 0 it will match any Gump.

**Parameters:**

- `gumpid` (UInt32): ID of the gump. (0: any)
- `delay` (Int32): Maximum wait, in milliseconds.

**Returns:** `Boolean` - True: wait found the gump - False: otherwise.

