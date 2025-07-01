# PacketLogger.PacketTemplate

Rapresents a general purpose template system for packets. 
The templates allow to format packets in the logger, making them readable.
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

### dynamicLength

**Type:** `Boolean`

Advanced settings for PacketReader. Ask Crezdba about DLLImport.Razor.IsDynLength(buff[0])

### fields

**Type:** `List[PacketLogger.FieldTemplate]`

List of fields present in this Packet.

### name

**Type:** `String`

A readable name for the packet, optional but useful.

### packetID

**Type:** `Int32`

packetID, mandatory.

### showHexDump

**Type:** `Boolean`

If showHexDump is true the packet logger will show also the hex dump.

### version

**Type:** `Int32`

Template version,optional

## Methods

No methods available.

