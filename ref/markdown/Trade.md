# Trade



## Properties

No properties available.

## Methods

### Accept

#### Overload 1

```python
Accept(TradeID: Int32, accept: Boolean = True)
```

Set the accept state of the trade

**Parameters:**

- `TradeID` (Int32): ID of the Trade (Default = -1: Pick a random active trade)
- `accept` (Boolean): Set the state ofthe checkbox

**Returns:** `Boolean` - True: Trade found, False: Trade not found

#### Overload 2

```python
Accept(accept: Boolean = True)
```

**Parameters:**

- `accept` (Boolean)

**Returns:** `Boolean`

### Cancel

#### Overload 1

```python
Cancel(TradeID: Int32)
```

Set the accept state of the trade

**Parameters:**

- `TradeID` (Int32): ID of the Trade (Default = -1: Pick a random active trade)

**Returns:** `Boolean` - True: Trade found, False: Trade not found

#### Overload 2

```python
Cancel()
```

**Returns:** `Boolean`

### Offer

#### Overload 1

```python
Offer(TradeID: Int32, gold: Int32, platinum: Int32, quiet: Boolean = False)
```

Update the amount of gold and platinum in the trade. ( client view dosen't update )

**Parameters:**

- `TradeID` (Int32): ID of the Trade (Default = -1: Pick latest active trade)
- `gold` (Int32): Amount of Gold to offer
- `platinum` (Int32): Amount of Platinum to offer
- `quiet` (Boolean): Suppress output (Default: false - Show warning)

**Returns:** `Boolean` - True: Trade found, False: Trade not found

#### Overload 2

```python
Offer(gold: Int32, platinum: Int32, quiet: Boolean = False)
```

**Parameters:**

- `gold` (Int32)
- `platinum` (Int32)
- `quiet` (Boolean)

**Returns:** `Boolean`

### TradeList

```python
TradeList()
```

Returns the list of currently active Secure Trading gumps, sorted by LastUpdate.

**Returns:** `List[Trade.TradeData]` - A list of Player.SecureTrade objects. Each containing the details of each trade window.

