# Mobiles

The Mobiles class provides a wide range of functions to search and interact with Mobile.

## Properties

No properties available.

## Methods

### ApplyFilter

```python
ApplyFilter(filter: Mobiles.Filter)
```

**Parameters:**

- `filter` (Mobiles.Filter)

**Returns:** `List[Mobile]`

### ContextExist

#### Overload 1

```python
ContextExist(mob: Mobile, name: String, showContext: Boolean = False)
```

**Parameters:**

- `mob` (Mobile)
- `name` (String)
- `showContext` (Boolean)

**Returns:** `Int32`

#### Overload 2

```python
ContextExist(serial: Int32, name: String, showContext: Boolean = False)
```

**Parameters:**

- `serial` (Int32)
- `name` (String)
- `showContext` (Boolean)

**Returns:** `Int32`

### FindBySerial

```python
FindBySerial(serial: Int32)
```

Find the Mobile with a specific Serial.

**Parameters:**

- `serial` (Int32): Serial of the Mobile.

**Returns:** `Mobile`

### FindMobile

#### Overload 1

```python
FindMobile(graphic: Int32, notoriety: List[Byte], rangemax: Int32, selector: String, highlight: Boolean)
```

**Parameters:**

- `graphic` (Int32)
- `notoriety` (List[Byte])
- `rangemax` (Int32)
- `selector` (String)
- `highlight` (Boolean)

**Returns:** `Mobile`

#### Overload 2

```python
FindMobile(graphics: List[Int32], notoriety: List[Byte], rangemax: Int32, selector: String, highlight: Boolean)
```

**Parameters:**

- `graphics` (List[Int32])
- `notoriety` (List[Byte])
- `rangemax` (Int32)
- `selector` (String)
- `highlight` (Boolean)

**Returns:** `Mobile`

### GetPropStringByIndex

#### Overload 1

```python
GetPropStringByIndex(serial: Int32, index: Int32)
```

**Parameters:**

- `serial` (Int32)
- `index` (Int32)

**Returns:** `String`

#### Overload 2

```python
GetPropStringByIndex(mob: Mobile, index: Int32)
```

**Parameters:**

- `mob` (Mobile)
- `index` (Int32)

**Returns:** `String`

### GetPropStringList

#### Overload 1

```python
GetPropStringList(serial: Int32)
```

**Parameters:**

- `serial` (Int32)

**Returns:** `List[String]`

#### Overload 2

```python
GetPropStringList(mob: Mobile)
```

**Parameters:**

- `mob` (Mobile)

**Returns:** `List[String]`

### GetPropValue

#### Overload 1

```python
GetPropValue(serial: Int32, name: String)
```

**Parameters:**

- `serial` (Int32)
- `name` (String)

**Returns:** `Single`

#### Overload 2

```python
GetPropValue(mob: Mobile, name: String)
```

**Parameters:**

- `mob` (Mobile)
- `name` (String)

**Returns:** `Single`

### GetTargetingFilter

```python
GetTargetingFilter(target_name: String)
```

**Parameters:**

- `target_name` (String)

**Returns:** `Mobiles.Filter`

### GetTrackingInfo

```python
GetTrackingInfo()
```

Get the most updated information about tracking.

**Returns:** `Mobiles.TrackingInfo`

### Message

#### Overload 1

```python
Message(mobile: Mobile, hue: Int32, message: String, wait: Boolean = True)
```

**Parameters:**

- `mobile` (Mobile)
- `hue` (Int32)
- `message` (String)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 2

```python
Message(serial: Int32, hue: Int32, message: String, wait: Boolean = True)
```

**Parameters:**

- `serial` (Int32)
- `hue` (Int32)
- `message` (String)
- `wait` (Boolean)

**Returns:** `Void`

### Select

```python
Select(mobiles: List[Mobile], selector: String)
```

**Parameters:**

- `mobiles` (List[Mobile])
- `selector` (String)

**Returns:** `Mobile`

### SingleClick

#### Overload 1

```python
SingleClick(mobile: Mobile)
```

**Parameters:**

- `mobile` (Mobile)

**Returns:** `Void`

#### Overload 2

```python
SingleClick(serial: Int32)
```

**Parameters:**

- `serial` (Int32)

**Returns:** `Void`

### UseMobile

#### Overload 1

```python
UseMobile(mobile: Mobile)
```

**Parameters:**

- `mobile` (Mobile)

**Returns:** `Void`

#### Overload 2

```python
UseMobile(mobileserial: Int32)
```

**Parameters:**

- `mobileserial` (Int32)

**Returns:** `Void`

### WaitForProps

#### Overload 1

```python
WaitForProps(m: Mobile, delay: Int32)
```

**Parameters:**

- `m` (Mobile)
- `delay` (Int32)

**Returns:** `Boolean`

#### Overload 2

```python
WaitForProps(mobileserial: Int32, delay: Int32)
```

**Parameters:**

- `mobileserial` (Int32)
- `delay` (Int32)

**Returns:** `Boolean`

### WaitForStats

#### Overload 1

```python
WaitForStats(m: Mobile, delay: Int32)
```

**Parameters:**

- `m` (Mobile)
- `delay` (Int32)

**Returns:** `Boolean`

#### Overload 2

```python
WaitForStats(mobileserial: Int32, delay: Int32)
```

**Parameters:**

- `mobileserial` (Int32)
- `delay` (Int32)

**Returns:** `Boolean`

