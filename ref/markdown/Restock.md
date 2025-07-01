# Restock

The Restock class allow you to interact with the Restock Agent, via scripting.

## Properties

No properties available.

## Methods

### ChangeList

```python
ChangeList(listName: String)
```

Change the Restock's active list.

**Parameters:**

- `listName` (String): Name of an existing restock list.

**Returns:** `Void`

### FStart

```python
FStart()
```

Start the Restock Agent on the currently active list.

**Returns:** `Void`

### FStop

```python
FStop()
```

Stop the Restock Agent.

**Returns:** `Void`

### RunOnce

```python
RunOnce(restockerName: String, sourceBag: Int32, destBag: Int32, dragDelay: Int32)
```

**Parameters:**

- `restockerName` (String)
- `sourceBag` (Int32)
- `destBag` (Int32)
- `dragDelay` (Int32)

**Returns:** `Void`

### Status

```python
Status()
```

Check Restock Agent status

**Returns:** `Boolean` - True: if the Restock is running - False: otherwise

