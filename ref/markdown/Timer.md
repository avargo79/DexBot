# Timer

Timer are normally used to display messages after a certain period of time. 
They are also often used to keep track of the maximum amount of time for an action to complete.

## Properties

No properties available.

## Methods

### Check

```python
Check(name: String)
```

Check if a timer object is expired or not.

**Parameters:**

- `name` (String)

**Returns:** `Boolean` - true if not expired, false if expired

### Create

#### Overload 1

```python
Create(name: String, delay: Int32, message: String)
```

Create a timer with the provided name that will expire in ms_timer time (in milliseconds)

**Parameters:**

- `name` (String): Timer name.
- `delay` (Int32): Delay in milliseconds.
- `message` (String): Message displayed at timeouit.

**Returns:** `Void`

#### Overload 2

```python
Create(name: String, delay: Int32)
```

**Parameters:**

- `name` (String)
- `delay` (Int32)

**Returns:** `Void`

### Remaining

```python
Remaining(name: String)
```

Get remaining time for a named timer

**Parameters:**

- `name` (String): Timer name

**Returns:** `Int32` - Returns the milliseconds remaining for a timer.

