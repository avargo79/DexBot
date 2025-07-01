# DexBot API Reference

Generated on: 2025-06-30 20:11:59

## Available Classes

- [AutoLoot](AutoLoot.md)
- [AutoLoot.AutoLootItem](AutoLoot.AutoLootItem.md)
- [BandageHeal](BandageHeal.md)
- [BuyAgent](BuyAgent.md)
- [CUO](CUO.md)
- [DPSMeter](DPSMeter.md)
- [Dress](Dress.md)
- [Friend](Friend.md)
- [Gumps](Gumps.md)
- [Gumps.GumpData](Gumps.GumpData.md)
- [HotKeyEvent](HotKeyEvent.md)
- [Item](Item.md)
- [Items](Items.md)
- [Items.Filter](Items.Filter.md)
- [Journal](Journal.md)
- [Journal.JournalEntry](Journal.JournalEntry.md)
- [Misc](Misc.md)
- [Misc.Context](Misc.Context.md)
- [Misc.MapInfo](Misc.MapInfo.md)
- [Mobile](Mobile.md)
- [Mobiles](Mobiles.md)
- [Mobiles.Filter](Mobiles.Filter.md)
- [Mobiles.TrackingInfo](Mobiles.TrackingInfo.md)
- [Organizer](Organizer.md)
- [PacketLogger](PacketLogger.md)
- [PacketLogger.FieldTemplate](PacketLogger.FieldTemplate.md)
- [PacketLogger.FieldType](PacketLogger.FieldType.md)
- [PacketLogger.PacketTemplate](PacketLogger.PacketTemplate.md)
- [PathFinding](PathFinding.md)
- [PathFinding.Route](PathFinding.Route.md)
- [Player](Player.md)
- [Point2D](Point2D.md)
- [Point3D](Point3D.md)
- [Property](Property.md)
- [Restock](Restock.md)
- [Scavenger](Scavenger.md)
- [SellAgent](SellAgent.md)
- [Sound](Sound.md)
- [Spells](Spells.md)
- [Statics](Statics.md)
- [Statics.TileInfo](Statics.TileInfo.md)
- [Target](Target.md)
- [Tile](Tile.md)
- [Timer](Timer.md)
- [Trade](Trade.md)
- [Trade.TradeData](Trade.TradeData.md)
- [Vendor](Vendor.md)
- [Vendor.BuyItem](Vendor.BuyItem.md)

## Usage

This documentation is automatically generated from the RazorEnhanced API. Each class provides methods and properties for interacting with Ultima Online through the RazorEnhanced scripting engine.

## Classes Overview

### [AutoLoot](AutoLoot.md)

The Autoloot class allow to interact with the Autoloot Agent, via scripting.

### [AutoLoot.AutoLootItem](AutoLoot.AutoLootItem.md)

### [BandageHeal](BandageHeal.md)

### [BuyAgent](BuyAgent.md)

The BuyAgent class allow you to interect with the BuyAgent, via scripting.

### [CUO](CUO.md)

The CUO_Functions class contains invocation of CUO code using reflection
DANGER !!

### [DPSMeter](DPSMeter.md)

The DPSMeter class implements a Damage Per Second meter which can be useful to tune meta-builds.(???)

### [Dress](Dress.md)

### [Friend](Friend.md)

### [Gumps](Gumps.md)

The Gumps class is used to read and interact with in-game gumps, via scripting.
NOTE
----
During development of scripts that involves interecting with Gumps, is often needed to know gumpids and buttonids.
For this purpose, can be particularly usefull to use *Inspect Gumps* and *Record*, top right, in the internal RE script editor.

### [Gumps.GumpData](Gumps.GumpData.md)

### [HotKeyEvent](HotKeyEvent.md)

@nodoc

### [Item](Item.md)

The Item class represent a single in-game Item object. Examples of Item are: Swords, bags, bandages, reagents, clothing.
While the Item.Serial is unique for each Item, Item.ItemID is the unique for the Item apparence, or image. Sometimes is also called ID or Graphics ID.
Item can also be house foriture as well as decorative items on the ground, like lamp post and banches.
However, for Item on the ground that cannot be picked up, they might be part of the world map, see Statics class.

### [Items](Items.md)

The Items class provides a wide range of functions to search and interact with Items.

### [Items.Filter](Items.Filter.md)

The Items.Filter class is used to store options to filter the global Item list.
Often used in combination with Items.ApplyFilter.

### [Journal](Journal.md)

The Journal class provides access to the message Journal.

### [Journal.JournalEntry](Journal.JournalEntry.md)

The JournalEntry class rapresents a line in the Journal.

### [Misc](Misc.md)

The Misc class contains general purpose functions of common use.

### [Misc.Context](Misc.Context.md)

The Context class holds information about a single entry in the Context Menu.

### [Misc.MapInfo](Misc.MapInfo.md)

The MapInfo class is used to store information about the Map location.

### [Mobile](Mobile.md)

The Mobile class represents an single alive entity. 
While the Mobile.Serial is unique for each Mobile, Mobile.MobileID is the unique for the Mobile apparence, or image. Sometimes is also called Body or Body ID.
Mobiles which dies and leave a corpse behind, they stop existing as Mobiles and instead leave a corpse as a Item object appears.

### [Mobiles](Mobiles.md)

The Mobiles class provides a wide range of functions to search and interact with Mobile.

### [Mobiles.Filter](Mobiles.Filter.md)

The Mobiles.Filter class is used to store options to filter the global Mobile list.
Often used in combination with Mobiles.ApplyFilter.

### [Mobiles.TrackingInfo](Mobiles.TrackingInfo.md)

The TrackingInfo class hold the latest information about.

### [Organizer](Organizer.md)

The Organizer class allow you to interect with the Scavenger Agent, via scripting.

### [PacketLogger](PacketLogger.md)

RazorEnhanced packet logger.

### [PacketLogger.FieldTemplate](PacketLogger.FieldTemplate.md)

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

### [PacketLogger.FieldType](PacketLogger.FieldType.md)

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

### [PacketLogger.PacketTemplate](PacketLogger.PacketTemplate.md)

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

### [PathFinding](PathFinding.md)

This class implements the PathFinding algorithm using A-Star.

### [PathFinding.Route](PathFinding.Route.md)

The Route class is used to configure the PathFinding.

### [Player](Player.md)

The Player class represent the currently logged in character.

### [Point2D](Point2D.md)

### [Point3D](Point3D.md)

### [Property](Property.md)

### [Restock](Restock.md)

The Restock class allow you to interact with the Restock Agent, via scripting.

### [Scavenger](Scavenger.md)

The Scavenger class allow you to interect with the Scavenger Agent, via scripting.

### [SellAgent](SellAgent.md)

The SellAgent class allow you to interect with the SellAgent, via scripting.

### [Sound](Sound.md)

The Sound class provides an api to manipulate Sounds. 
For now it just turns logging for sounds on / off or waits for a list of sounds
All the WeakRef stuff seems like overkill and a pia. 
The problem was if you started the wait and then killed the python script, the entry in the waiters list just stayed forever
The only way around this is to have a weakref stored in the list, then if the local var ManualResetEvent went out of scope, 
the WeakRef will go to null.  At end of loop we clean up all null entries so the list stays clean.

### [Spells](Spells.md)

The Spells class allow you to cast any spell and use abilities, via scripting.

### [Statics](Statics.md)

The Statics class provides access to informations about the Map, down to the individual tile.
When using this function it's important to remember the distinction between Land and Tile:
Land
----
For a given (X,Y,map) there can be only 1 (0 zero) Land item, and has 1 specific Z coordinate.
Tile
----
For a given (X,Y,map) there can be any number of Tile items.

### [Statics.TileInfo](Statics.TileInfo.md)

The TileInfo class hold the values represeting Tile or Land items for a given X,Y coordinate.

### [Target](Target.md)

The Target class provides various methods for targeting Land, Items and Mobiles in game.

### [Tile](Tile.md)

Class representing an (X,Y) coordinate. Optimized for pathfinding tasks.

### [Timer](Timer.md)

Timer are normally used to display messages after a certain period of time. 
They are also often used to keep track of the maximum amount of time for an action to complete.

### [Trade](Trade.md)

### [Trade.TradeData](Trade.TradeData.md)

SecureTrades holds the information about a single tradeing window.

### [Vendor](Vendor.md)

@experimental
The Vendor class allow you to read the list items purchased last.

### [Vendor.BuyItem](Vendor.BuyItem.md)

The BuyItem class store informations about a recently purchased item.

