# Organizer

The Organizer class allow you to interect with the Scavenger Agent, via scripting.

## Properties

No properties available.

## Methods

### ChangeList

```python
ChangeList(listName: String)
```

Change the Organizer's active list.

**Parameters:**

- `listName` (String): Name of an existing organizer list.

**Returns:** `Void`

### FStart

```python
FStart()
```

Start the Organizer Agent on the currently active list.

**Returns:** `Void`

### FStop

```python
FStop()
```

Stop the Organizer Agent.

**Returns:** `Void`

### RunOnce

```python
RunOnce(organizerName: String, sourceBag: Int32, destBag: Int32, dragDelay: Int32)
```

**Parameters:**

- `organizerName` (String)
- `sourceBag` (Int32)
- `destBag` (Int32)
- `dragDelay` (Int32)

**Returns:** `Void`

### Status

```python
Status()
```

Check Organizer Agent status

**Returns:** `Boolean` - True: if the Organizer is running - False: otherwise

