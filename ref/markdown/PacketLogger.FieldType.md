# PacketLogger.FieldType

Type of Fields available for FieldTemplate 
Example of "Damage" (0x0B) packet:
{
 'packetID': 0x0B,
 'name': 'Damage 0x0B',
 'showHexDump': true,
 'fields':[
   { 'name':'packetID', 'length':1, 'type':'packetID'},
   { 'name':'Serial', 'length':4, 'type':'serial'},
   { 'name':'Damage', 'length': 2, 'type':'int'},
 ]
}

## Properties

### BOOL

**Type:** `String`

Boolean type, length is fixed to 1 byte.
      
Example:
{'name':'Paralized', 'type':'bool'}

### DUMP

**Type:** `String`

Dump a certain amount of data as raw bytes-by-bytes HEX 
Length is mandatory.
      
Example:
{'name':'unused', 'type':'dump', 'length': 40}

### FIELDS

**Type:** `String`

A special field which has subfields, useful for displaying stucts. 
'length' is ignored, 'type' is optional, 'fields' is mandatory.

Example:
{'name':'Player Position', 'type':'fields',
  'fields':[
         {'name':'X', 'type':'uint', 'length': 2}
         {'name':'Y', 'type':'uint', 'length': 2}
         {'name':'Z', 'type':'uint', 'length': 1}
   ]
}

### FIELDSFOR

**Type:** `String`

### HEX

**Type:** `String`

Hex type is equivalent to unsigned integers but the contents is displayed as 0x hex.
Length is mandatory and can range between 1 and 4 bytes.
      
Example:
{'name':'Hue', 'type':'hex', 'length': 2}

### INT

**Type:** `String`

Integers type used for positive and negative integers.
Length is mandatory and can range between 1 and 4 bytes.
      
Example:
{'name':'Z Level', 'type':'int', 'length': 2}

### MODELID

**Type:** `String`

ModelID type like Item.ItemdID, Mobile.Body, etc.
Length is fixed to 2 bytes and is displayed as 0x hex.
      
Example:
{'name':'Item ID', 'type':'modelID'}
{'name':'Mobile Body', 'type':'modelID'}
{'name':'Static ID', 'type':'modelID'}

### PACKETID

**Type:** `String`

Common type present in every packet, packetID, length is fixed to 1 byte.
           
Example:
{'name':'packetID', 'type':'packetID'}

### SERIAL

**Type:** `String`

Serial type, length is fixed to 4 bytes and is displayed as 0x hex.
      
Example:
{'name':'Target Serial', 'type':'serial'}

### SKIP

**Type:** `String`

Skip a certain amount of data.
Length is mandatory.
      
Example:
{'name':'unused', 'type':'skip', 'length': 40}

### SUBPACKET

**Type:** `String`

A special field which denotes the beginning of a subpacket. 
'length' is ignored, 'type' is optional, 'subpacket' is mandatory.

Example:
{'name':'action', 'type':'subpacket',
  'subpacket':{
    'name':'my subpacket'
    'fields':[
        ...
    ]
  }

}

### TEXT

**Type:** `String`

Text reads bytes as text.
Length is mandatory.
      
Example:
{'name':'Name', 'type':'text', 'length': 20}

### UINT

**Type:** `String`

Unsigned integers type used for positive integers.
Length is mandatory and can range between 1 and 4 bytes.
      
Example:
{'name':'Z Level', 'type':'uint', 'length': 2}

### UTF8

**Type:** `String`

Text reads bytes as UTF8 text.
Length is mandatory.
      
Example:
{'name':'Pet name', 'type':'utf8', 'length': 40}

### VALID_TYPES

**Type:** `String[][]`

List of valid types

## Methods

### IsValid

```python
IsValid(typename: String)
```

Check if the name of type is a valid Template filed type.

**Parameters:**

- `typename` (String): Name of the types

**Returns:** `Boolean` - True: is resognized. - False: not recognized.

