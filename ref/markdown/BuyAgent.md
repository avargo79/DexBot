# BuyAgent

The BuyAgent class allow you to interect with the BuyAgent, via scripting.

## Properties

No properties available.

## Methods

### ChangeList

```python
ChangeList(listName: String)
```

Change the BuyAgent's active list.

**Parameters:**

- `listName` (String): Name of an existing buy list.

**Returns:** `Void`

### Disable

```python
Disable()
```

Disable BuyAgent Agent.

**Returns:** `Void`

### Enable

```python
Enable()
```

Enable BuyAgent on the currently active list.

**Returns:** `Void`

### Status

```python
Status()
```

Check BuyAgent Agent status

**Returns:** `Boolean` - True: if the BuyAgent is active - False: otherwise

