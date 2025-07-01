# DPSMeter

The DPSMeter class implements a Damage Per Second meter which can be useful to tune meta-builds.(???)

## Properties

No properties available.

## Methods

### GetDamage

```python
GetDamage(serial: Int32)
```

Get total damage per Mobile.

**Parameters:**

- `serial` (Int32): Serial of the Mobile.

**Returns:** `Int32` - Total damage.

### Pause

```python
Pause()
```

Pause DPSMeter data recording.

**Returns:** `Void`

### Start

```python
Start()
```

Start DPSMeter engine.

**Returns:** `Void`

### Status

```python
Status()
```

Check DPSMeter Agent status, returns a bool value.

**Returns:** `Boolean` - True: is running - False: otherwise

### Stop

```python
Stop()
```

Stop DPSMeter engine.

**Returns:** `Void`

