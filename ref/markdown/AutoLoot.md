# AutoLoot

The Autoloot class allow to interact with the Autoloot Agent, via scripting.

## Properties

No properties available.

## Methods

### ChangeList

```python
ChangeList(listName: String)
```

Change the Autoloot's active list.

**Parameters:**

- `listName` (String): Name of an existing organizer list.

**Returns:** `Void`

### GetList

```python
GetList(lootListName: String, wantMinusOnes: Boolean = False)
```

Given an AutoLoot list name, return a list of AutoLootItem associated.

**Parameters:**

- `lootListName` (String): Name of the AutoLoot list.
- `wantMinusOnes` (Boolean)

**Returns:** `List[AutoLoot.AutoLootItem]`

### GetLootBag

```python
GetLootBag()
```

Get current Autoloot destination container.

**Returns:** `UInt32` - Serial of the container.

### ResetIgnore

```python
ResetIgnore()
```

Reset the Autoloot ignore list.

**Returns:** `Void`

### RunOnce

```python
RunOnce(lootListName: String, millisec: Int32, filter: Items.Filter)
```

Start Autoloot with custom parameters.

**Parameters:**

- `lootListName` (String): Name of the Autoloot listfilter for search on ground.
- `millisec` (Int32): Delay in milliseconds. (unused)
- `filter` (Items.Filter): Item filter

**Returns:** `Void`

### SetNoOpenCorpse

```python
SetNoOpenCorpse(noOpen: Boolean)
```

Toggle "No Open Corpse" on/off. The change doesn't persist if you reopen razor.

**Parameters:**

- `noOpen` (Boolean): True: "No Open Corpse" is active - False: otherwise

**Returns:** `Boolean` - Previous value of "No Open Corpse"

### Start

```python
Start()
```

Start the Autoloot Agent on the currently active list.

**Returns:** `Void`

### Status

```python
Status()
```

Check Autoloot Agent status

**Returns:** `Boolean` - True: if the Autoloot is running - False: otherwise

### Stop

```python
Stop()
```

Stop the Autoloot Agent.

**Returns:** `Void`

