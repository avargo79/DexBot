# Vendor

@experimental
The Vendor class allow you to read the list items purchased last.

## Properties

### LastBuyList

**Type:** `List[Item]`

### LastResellList

**Type:** `List[Item]`

## Methods

### Buy

#### Overload 1

```python
Buy(vendorSerial: Int32, itemName: String, amount: Int32, maxPrice: Int32 = -1)
```

Attempts to buy the item from the vendor specified.
<param name="vendorSerial">The Vendor to buy from</param>
<param name="itemName">the name of the item to buy (can be partial)</param>
<param name="amount">amount to attempt to buy</param>
<param name="maxPrice">Don't buy them if the cost exceeds this price.
default value = -1 means don't check price</param>
Returns True if a purchase is made, False otherwise

**Parameters:**

- `vendorSerial` (Int32): The Vendor to buy from
- `itemName` (String): the name of the item to buy (can be partial)
- `amount` (Int32): amount to attempt to buy
- `maxPrice` (Int32): Don't buy them if the cost exceeds this price.
            default value = -1 means don't check price

**Returns:** `Boolean`

#### Overload 2

```python
Buy(vendorSerial: Int32, itemID: Int32, amount: Int32, maxPrice: Int32 = -1)
```

Attempts to buy the item from the vendor specified.
<param name="vendorSerial">The Vendor to buy from</param>
<param name="itemID">the itemID of the type of item to buy</param>
<param name="amount">amount to attempt to buy</param>
<param name="maxPrice">Don't buy them if the cost exceeds this price.
default value = -1 means don't check price</param>
Returns True if a purchase is made, False otherwise

**Parameters:**

- `vendorSerial` (Int32): The Vendor to buy from
- `itemID` (Int32): the itemID of the type of item to buy
- `amount` (Int32): amount to attempt to buy
- `maxPrice` (Int32): Don't buy them if the cost exceeds this price.
            default value = -1 means don't check price

**Returns:** `Boolean`

### BuyList

```python
BuyList(vendorSerial: Int32 = -1)
```

Get the list of items purchased in the last trade, with a specific Vendor.

**Parameters:**

- `vendorSerial` (Int32): Serial of the Vendor (default: -1 - most recent trade)

**Returns:** `List[Vendor.BuyItem]` - A list of BuyItem

