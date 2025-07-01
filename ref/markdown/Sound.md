# Sound

The Sound class provides an api to manipulate Sounds. 
For now it just turns logging for sounds on / off or waits for a list of sounds
All the WeakRef stuff seems like overkill and a pia. 
The problem was if you started the wait and then killed the python script, the entry in the waiters list just stayed forever
The only way around this is to have a weakref stored in the list, then if the local var ManualResetEvent went out of scope, 
the WeakRef will go to null.  At end of loop we clean up all null entries so the list stays clean.

## Properties

No properties available.

## Methods

### AddFilter

```python
AddFilter(name: String, sounds: List[Int32])
```

**Parameters:**

- `name` (String)
- `sounds` (List[Int32])

**Returns:** `Void`

### Log

```python
Log(activateLogging: Boolean)
```

Enables/Disables logging of incoming sound requests

**Parameters:**

- `activateLogging` (Boolean): True= activate sound logging/ False Deactivate sound logging

**Returns:** `Void`

### OnFilter

```python
OnFilter(p: PacketReader, args: PacketHandlerEventArgs)
```

**Parameters:**

- `p` (PacketReader)
- `args` (PacketHandlerEventArgs)

**Returns:** `Void`

### RemoveFilter

```python
RemoveFilter(name: String)
```

Removes a filter of incoming sound requests

**Parameters:**

- `name` (String): The name of the filter to be removed

**Returns:** `Void`

### WaitForSound

```python
WaitForSound(sounds: List[Int32], timeout: Int32 = -1)
```

**Parameters:**

- `sounds` (List[Int32])
- `timeout` (Int32)

**Returns:** `Boolean`

