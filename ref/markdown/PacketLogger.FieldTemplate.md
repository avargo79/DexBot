# PacketLogger.FieldTemplate

Class representing the fields inside a packet template.
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

### fields

**Type:** `List[PacketLogger.FieldTemplate]`

List of subfields present in this Field.

### length

**Type:** `Int32`

Length in bytes. length &gt; 0 maybe a mandatory for some FieldType.

### name

**Type:** `String`

Dysplay Name of the field.

### subpacket

**Type:** `PacketLogger.PacketTemplate`

A subpacket Field.

### type

**Type:** `String`

Type of field. See FieldType for details on each type.

## Methods

No methods available.

