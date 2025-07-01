# PacketLogger

RazorEnhanced packet logger.

## Properties

### PathToString

**Type:** `Dictionary[PacketPath, String]`

### StringToPath

**Type:** `Dictionary[String, PacketPath]`

## Methods

### AddBlacklist

```python
AddBlacklist(packetID: Int32)
```

Add the packetID to the blacklist. Packets in the backlist will not be logged. (See PacketLogger.DiscardAll() )

**Parameters:**

- `packetID` (Int32): PacketID to blacklist

**Returns:** `Void`

### AddTemplate

```python
AddTemplate(packetTemplate: String)
```

Add a custom template for RazorEnhanced packet logger.
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

**Parameters:**

- `packetTemplate` (String): Add a PacketTemplate, check ./Config/packets/ folder.

**Returns:** `Void`

### AddWhitelist

```python
AddWhitelist(packetID: Int32)
```

Add the packetID to the whitelist. Packets in the whitelist are always. (See PacketLogger.DiscardAll() )

**Parameters:**

- `packetID` (Int32): PacketID to whitelist

**Returns:** `Void`

### DiscardAll

```python
DiscardAll(discardAll: Boolean)
```

Packet logger will discard all packets, except the one in the whitelist.  (See PacketLogger.AddWhitelist() )

**Parameters:**

- `discardAll` (Boolean): True: Log only the packet in the whitelist - False: Log everything, but the packets in the blacklist

**Returns:** `Void`

### DiscardShowHeader

```python
DiscardShowHeader(showHeader: Boolean)
```

Packet logger will show the headers of discarded packets.

**Parameters:**

- `showHeader` (Boolean): True: Always show headers - False: Hide everything.

**Returns:** `Void`

### ListenPacketPath

```python
ListenPacketPath(packetPath: String = , active: Boolean = True)
```

Packet logger will discard all packets, except the one in the whitelist.  (See PacketLogger.AddWhitelist() ) 
If the packetPath is not set or not resognized, the function simply returns the current active paths.

**Parameters:**

- `packetPath` (String): Possible values:
   ClientToServer
   ServerToClient
   RazorToServer (TODO)
   RazorToClient (TODO)
   PacketVideo   (TODO)
- `active` (Boolean)

**Returns:** `String[][]` - List of strings of currently active packet paths.

### RemoveTemplate

```python
RemoveTemplate(packetID: Int32 = -1)
```

Remove a PacketTemplate for RazorEnhanced packet logger.

**Parameters:**

- `packetID` (Int32): Remove a spacific packetID. (Default: -1 Remove All)

**Returns:** `Void`

### Reset

```python
Reset()
```

Reset the packet logger to defaults.

**Returns:** `Void`

### SendToClient

#### Overload 1

```python
SendToClient(packetData: Byte[][])
```

Send a packet to the client.

**Parameters:**

- `packetData` (Byte[][])

**Returns:** `Void`

#### Overload 2

```python
SendToClient(packetData: List[Byte])
```

**Parameters:**

- `packetData` (List[Byte])

**Returns:** `Void`

#### Overload 3

```python
SendToClient(packetData: PythonList)
```

**Parameters:**

- `packetData` (PythonList)

**Returns:** `Void`

### SendToServer

#### Overload 1

```python
SendToServer(packetData: Byte[][])
```

Send a packet to the server.

**Parameters:**

- `packetData` (Byte[][])

**Returns:** `Void`

#### Overload 2

```python
SendToServer(packetData: List[Byte])
```

**Parameters:**

- `packetData` (List[Byte])

**Returns:** `Void`

#### Overload 3

```python
SendToServer(packetData: PythonList)
```

**Parameters:**

- `packetData` (PythonList)

**Returns:** `Void`

### SetOutputPath

```python
SetOutputPath(outputpath: String = None)
```

Set the RazorEnhanced packet logger. Calling it without a path it rester it to the default path.

**Parameters:**

- `outputpath` (String): (Optional) Custom output path (Default: reset to ./Desktop/Razor_Packets.log)

**Returns:** `String` - The path to the saved file.

### Start

#### Overload 1

```python
Start(outputpath: String = None, appendLogs: Boolean = False)
```

Start the RazorEnhanced packet logger.

**Parameters:**

- `outputpath` (String): Custom output path (Default: ./Desktop/Razor_Packets.log)
- `appendLogs` (Boolean): True: Append - False: Overwrite (Default: False)

**Returns:** `String` - The path to the saved file.

#### Overload 2

```python
Start(appendLogs: Boolean = False)
```

**Parameters:**

- `appendLogs` (Boolean)

**Returns:** `String`

### Stop

```python
Stop()
```

Stop the RazorEnhanced packet logger.

**Returns:** `String` - The path to the saved file.

