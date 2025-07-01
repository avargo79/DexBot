# Scavenger

The Scavenger class allow you to interect with the Scavenger Agent, via scripting.

## Properties

No properties available.

## Methods

### ChangeList

```python
ChangeList(listName: String)
```

Change the Scavenger's active list.

**Parameters:**

- `listName` (String): Name of an existing organizer list.

**Returns:** `Void`

### GetScavengerBag

```python
GetScavengerBag()
```

Get current Scravenger destination container.

**Returns:** `UInt32` - Serial of the container.

### ResetIgnore

```python
ResetIgnore()
```

**Returns:** `Void`

### RunOnce

```python
RunOnce(scavengerList: List[Scavenger.ScavengerItem], millisec: Int32, filter: Items.Filter)
```

**Parameters:**

- `scavengerList` (List[Scavenger.ScavengerItem])
- `millisec` (Int32)
- `filter` (Items.Filter)

**Returns:** `Void`

### Start

```python
Start()
```

Start the Scavenger Agent on the currently active list.

**Returns:** `Void`

### Status

```python
Status()
```

Check Scavenger Agent status

**Returns:** `Boolean` - True: if the Scavenger is running - False: otherwise

### Stop

```python
Stop()
```

Stop the Scavenger Agent.

**Returns:** `Void`

