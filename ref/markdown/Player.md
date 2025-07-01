# Player

The Player class represent the currently logged in character.

## Properties

### AR

**Type:** `Int32`

Resistance to Phisical damage.

### Backpack

**Type:** `Item`

Player backpack, as Item object.

### Bank

**Type:** `Item`

Player bank chest, as Item object.

### Body

**Type:** `Int32`

Player Body or MobileID (see: Mobile.Body)

### Buffs

**Type:** `List[String]`

List of Player active buffs:
   Meditation
   Agility
   Animal Form
   Arcane Enpowerment
   Arcane Enpowerment (new)
   Arch Protection
   Armor Pierce
   Attunement
   Aura of Nausea
   Bleed
   Bless
   Block
   Bload Oath (caster)
   Bload Oath (curse)
   BloodWorm Anemia
   City Trade Deal
   Clumsy
   Confidence
   Corpse Skin
   Counter Attack
   Criminal
   Cunning
   Curse
   Curse Weapon
   Death Strike
   Defense Mastery
   Despair
   Despair (target)
   Disarm (new)
   Disguised
   Dismount Prevention
   Divine Fury
   Dragon Slasher Fear
   Enchant
   Enemy Of One
   Enemy Of One (new)
   Essence Of Wind
   Ethereal Voyage
   Evasion
   Evil Omen
   Faction Loss
   Fan Dancer Fan Fire
   Feeble Mind
   Feint
   Force Arrow
   Berserk
   Fly
   Gaze Despair
   Gift Of Life
   Gift Of Renewal
   Healing
   Heat Of Battle
   Hiding
   Hiryu Physical Malus
   Hit Dual Wield
   Hit Lower Attack
   Hit Lower Defense
   Honorable Execution
   Honored
   Horrific Beast
   Hawl Of Cacophony
   Immolating Weapon
   Incognito
   Inspire
   Invigorate
   Invisibility
   Lich Form
   Lighting Strike
   Magic Fish
   Magic Reflection
   Mana Phase
   Mass Curse
   Medusa Stone
   Mind Rot
   Momentum Strike
   Mortal Strike
   Night Sight
   NoRearm
   Orange Petals
   Pain Spike
   Paralyze
   Perfection
   Perseverance
   Poison
   Poison Resistance
   Polymorph
   Protection
   Psychic Attack
   Consecrate Weapon
   Rage
   Rage Focusing
   Rage Focusing (target)
   Reactive Armor
   Reaper Form
   Resilience
   Rose Of Trinsic
   Rotworm Blood Disease
   Rune Beetle Corruption
   Skill Use Delay
   Sleep
   Spell Focusing
   Spell Focusing (target)
   Spell Plague
   Splintering Effect
   Stone Form
   Strangle
   Strength
   Surge
   Swing Speed
   Talon Strike
   Vampiric Embrace
   Weaken
   Wraith Form

### BuffsInfo

**Type:** `List[BuffInfo]`

Returns a list with every detailed active buff

### ColdResistance

**Type:** `Int32`

Resistance to Cold damage.

### Connected

**Type:** `Boolean`

Retrieves Connected State

### Corpses

**Type:** `HashSet[Item]`

Each Death Player corpse item is added here

### DamageChanceIncrease

**Type:** `Int32`

Get total Damage Chance Increase.

### DefenseChanceIncrease

**Type:** `Int32`

Get total Defense Chance Increase.

### Dex

**Type:** `Int32`

Stats value for Dexterity.

### DexterityIncrease

**Type:** `Int32`

Get total Dexterity Increase.

### Direction

**Type:** `String`

Player current direction, as text.

### EnergyResistance

**Type:** `Int32`

Resistance to Energy damage.

### EnhancePotions

**Type:** `Int32`

Get total Enhance Potions.

### Fame

**Type:** `Int32`

Fame has to be reverse engineered from the title so it is just ranges:
0: neutaral - 3 is highest fame

### FasterCastRecovery

**Type:** `Int32`

Get total Faster Cast Recovery.

### FasterCasting

**Type:** `Int32`

Get total Faster Casting.

### Female

**Type:** `Boolean`

Player is a female.

### FireResistance

**Type:** `Int32`

Resistance to Fire damage.

### Followers

**Type:** `Int32`

Player current amount of pet/followers.

### FollowersMax

**Type:** `Int32`

Player maximum amount of pet/followers.

### Gold

**Type:** `Int32`

Player total gold, in the backpack.

### HasPrimarySpecial

**Type:** `Boolean`

### HasSecondarySpecial

**Type:** `Boolean`

### HasSpecial

**Type:** `Boolean`

Player have a special abilities active.

### HitChanceIncrease

**Type:** `Int32`

Get total Hit Chance Increase.

### HitPointsIncrease

**Type:** `Int32`

Get total Hit Points Increase.

### HitPointsRegeneration

**Type:** `Int32`

Get total Hit Points Regeneration.

### Hits

**Type:** `Int32`

Current hit points.

### HitsMax

**Type:** `Int32`

Maximum hit points.

### InParty

**Type:** `Boolean`

Player is in praty.

### Int

**Type:** `Int32`

Stats value for Intelligence.

### IntelligenceIncrease

**Type:** `Int32`

Get total Intelligence Increase.

### IsGhost

**Type:** `Boolean`

Player is a Ghost

### Karma

**Type:** `Int32`

Karma has to be reverse engineered from the title so it is just ranges:
-5: most evil, 0: neutaral, 5 most good

### KarmaTitle

**Type:** `String`

This is the title string returned from the server

### LowerManaCost

**Type:** `Int32`

Get total Lower Mana Cost.

### LowerReagentCost

**Type:** `Int32`

Get total Lower Reagent Cost.

### Luck

**Type:** `Int32`

Player total luck.

### Mana

**Type:** `Int32`

Current mana.

### ManaIncrease

**Type:** `Int32`

Get total Mana Increase.

### ManaMax

**Type:** `Int32`

Maximum mana.

### ManaRegeneration

**Type:** `Int32`

Get total Mana Regeneration.

### Map

**Type:** `Int32`

Player current map, or facet.

### MaxWeight

**Type:** `Int32`

Player maximum weight.

### MaximumHitPointsIncrease

**Type:** `Int32`

Get total Maximum Hit Points Increase.

### MaximumStaminaIncrease

**Type:** `Int32`

Get total Maximum Stamina Increase.

### MobileID

**Type:** `Int32`

Player MobileID or Body (see: Mobile.MobileID)

### Mount

**Type:** `Item`

Player current Mount, as Item object.
NOTE: On some server the Serial return by this function doesn't match the mount serial.

### Name

**Type:** `String`

Player name.

### Notoriety

**Type:** `Byte`

Player notoriety
    1: blue, innocent
    2: green, friend
    3: gray, neutral
    4: gray, criminal
    5: orange, enemy
    6: red, hostile 
    6: yellow, invulnerable

### Paralized

**Type:** `Boolean`

Player is Paralized. True also while frozen because of casting of spells.

### Pets

**Type:** `List[Mobile]`

Finds all neutral pets in the area that can be renamed.
This isn't the server information on your pets, but its good enough for most cases

### PoisonResistance

**Type:** `Int32`

Resistance to Poison damage.

### Poisoned

**Type:** `Boolean`

Player is Poisoned

### Position

**Type:** `Point3D`

Current Player position as Point3D object.

### PrimarySpecial

**Type:** `UInt32`

### Quiver

**Type:** `Item`

Player quiver, as Item object.

### ReflectPhysicalDamage

**Type:** `Int32`

Get total Reflect Physical Damage.

### SecondarySpecial

**Type:** `UInt32`

### Serial

**Type:** `Int32`

Player unique Serial.

### SpellDamageIncrease

**Type:** `Int32`

Get total Spell Damage Increase.

### Stam

**Type:** `Int32`

Current stamina.

### StamMax

**Type:** `Int32`

Maximum stamina.

### StaminaIncrease

**Type:** `Int32`

Get total Stamina Increase.

### StaminaRegeneration

**Type:** `Int32`

Get total Stamina Regeneration.

### StatCap

**Type:** `Int32`

Get the stats cap.

### StaticMount

**Type:** `Int32`

Retrieves serial of mount set in Filter/Mount GUI.

### Str

**Type:** `Int32`

Stats value for Strenght.

### StrengthIncrease

**Type:** `Int32`

Get total Strength Increase.

### SwingSpeedIncrease

**Type:** `Int32`

Get total Swing Speed Increase.

### Visible

**Type:** `Boolean`

Player is visible, false if hidden.

### WarMode

**Type:** `Boolean`

Player has war mode active.

### Weight

**Type:** `Int32`

Player current weight.

### YellowHits

**Type:** `Boolean`

Player HP bar is not blue, but yellow.

## Methods

### Area

```python
Area()
```

Get the name of the area in which the Player is currently in. (Ex: Britain, Destard, Vesper, Moongate, etc)
Regions are defined inside by Config/regions.json.

**Returns:** `String` - Name of the area. Unknown if not recognized.

### Attack

#### Overload 1

```python
Attack(serial: Int32)
```

Attack a Mobile.

**Parameters:**

- `serial` (Int32): Serial or Mobile to attack.

**Returns:** `Void`

#### Overload 2

```python
Attack(mobile: Mobile)
```

**Parameters:**

- `mobile` (Mobile)

**Returns:** `Void`

### AttackLast

```python
AttackLast()
```

Attack last target.

**Returns:** `Void`

### AttackType

#### Overload 1

```python
AttackType(graphic: Int32, rangemax: Int32, selector: String, color: List[Int32] = None, notoriety: List[Byte] = None)
```

**Parameters:**

- `graphic` (Int32)
- `rangemax` (Int32)
- `selector` (String)
- `color` (List[Int32])
- `notoriety` (List[Byte])

**Returns:** `Boolean`

#### Overload 2

```python
AttackType(graphics: List[Int32], rangemax: Int32, selector: String, color: List[Int32] = None, notoriety: List[Byte] = None)
```

**Parameters:**

- `graphics` (List[Int32])
- `rangemax` (Int32)
- `selector` (String)
- `color` (List[Int32])
- `notoriety` (List[Byte])

**Returns:** `Boolean`

### BuffTime

```python
BuffTime(buffname: String)
```

**Parameters:**

- `buffname` (String)

**Returns:** `Int32`

### BuffsExist

```python
BuffsExist(buffname: String, okayToGuess: Boolean = True)
```

Check if a buff is active, by buff name.

**Parameters:**

- `buffname` (String): Meditation
Agility
Animal Form
Arcane Enpowerment
Arcane Enpowerment (new)
Arch Protection
Armor Pierce
Attunement
Aura of Nausea
Bleed
Bless
Block
Bload Oath (caster)
Bload Oath (curse)
BloodWorm Anemia
City Trade Deal
Clumsy
Confidence
Corpse Skin
Counter Attack
Criminal
Cunning
Curse
Curse Weapon
Death Strike
Defense Mastery
Despair
Despair (target)
Disarm (new)
Disguised
Dismount Prevention
Divine Fury
Dragon Slasher Fear
Enchant
Enemy Of One
Enemy Of One (new)
Essence Of Wind
Ethereal Voyage
Evasion
Evil Omen
Faction Loss
Fan Dancer Fan Fire
Feeble Mind
Feint
Force Arrow
Berserk
Fly
Gaze Despair
Gift Of Life
Gift Of Renewal
Healing
Heat Of Battle
Hiding
Hiryu Physical Malus
Hit Dual Wield
Hit Lower Attack
Hit Lower Defense
Honorable Execution
Honored
Horrific Beast
Hawl Of Cacophony
Immolating Weapon
Incognito
Inspire
Invigorate
Invisibility
Lich Form
Lighting Strike
Magic Fish
Magic Reflection
Mana Phase
Mass Curse
Medusa Stone
Mind Rot
Momentum Strike
Mortal Strike
Night Sight
NoRearm
Orange Petals
Pain Spike
Paralyze
Perfection
Perseverance
Poison
Poison Resistance
Polymorph
Protection
Psychic Attack
Consecrate Weapon
Rage
Rage Focusing
Rage Focusing (target)
Reactive Armor
Reaper Form
Resilience
Rose Of Trinsic
Rotworm Blood Disease
Rune Beetle Corruption
Skill Use Delay
Sleep
Spell Focusing
Spell Focusing (target)
Spell Plague
Splintering Effect
Stone Form
Strangle
Strength
Surge
Swing Speed
Talon Strike
Vampiric Embrace
Weaken
Wraith Form
- `okayToGuess` (Boolean)

**Returns:** `Boolean` - True: if the buff is active - False: otherwise.

### ChatAlliance

#### Overload 1

```python
ChatAlliance(msg: String)
```

Send message to the alliace chat.

**Parameters:**

- `msg` (String): Message to send.

**Returns:** `Void`

#### Overload 2

```python
ChatAlliance(msg: Int32)
```

**Parameters:**

- `msg` (Int32)

**Returns:** `Void`

### ChatChannel

#### Overload 1

```python
ChatChannel(msg: String)
```

Send an chat channel message.

**Parameters:**

- `msg` (String): Message to send.

**Returns:** `Void`

#### Overload 2

```python
ChatChannel(msg: Int32)
```

**Parameters:**

- `msg` (Int32)

**Returns:** `Void`

### ChatEmote

#### Overload 1

```python
ChatEmote(color: Int32, msg: Int32)
```

**Parameters:**

- `color` (Int32)
- `msg` (Int32)

**Returns:** `Void`

#### Overload 2

```python
ChatEmote(color: Int32, msg: String)
```

Send an emote in game.

**Parameters:**

- `color` (Int32): Color of the text
- `msg` (String): Message to send.

**Returns:** `Void`

### ChatGuild

#### Overload 1

```python
ChatGuild(msg: String)
```

Send message to the guild chat.

**Parameters:**

- `msg` (String): Message to send.

**Returns:** `Void`

#### Overload 2

```python
ChatGuild(msg: Int32)
```

**Parameters:**

- `msg` (Int32)

**Returns:** `Void`

### ChatParty

```python
ChatParty(msg: String, recepient_serial: Int32 = 0)
```

Send message in arty chat. If a recepient_serial is specified, the message is private.

**Parameters:**

- `msg` (String): Text to send.
- `recepient_serial` (Int32): Optional: Target of private message.

**Returns:** `Void`

### ChatSay

#### Overload 1

```python
ChatSay(color: Int32, msg: String)
```

Send message in game.

**Parameters:**

- `color` (Int32): Color of the text
- `msg` (String): Message to send.

**Returns:** `Void`

#### Overload 2

```python
ChatSay(color: Int32, msg: Int32)
```

**Parameters:**

- `color` (Int32)
- `msg` (Int32)

**Returns:** `Void`

#### Overload 3

```python
ChatSay(msg: String)
```

Send message in game using 1153 for color.

**Parameters:**

- `msg` (String): Message to send.

**Returns:** `Void`

### ChatWhisper

#### Overload 1

```python
ChatWhisper(color: Int32, msg: String)
```

Send an wishper message.

**Parameters:**

- `color` (Int32): Color of the text
- `msg` (String): Message to send.

**Returns:** `Void`

#### Overload 2

```python
ChatWhisper(color: Int32, msg: Int32)
```

**Parameters:**

- `color` (Int32)
- `msg` (Int32)

**Returns:** `Void`

### ChatYell

#### Overload 1

```python
ChatYell(color: Int32, msg: String)
```

Send an yell message.

**Parameters:**

- `color` (Int32): Color of the text
- `msg` (String): Message to send.

**Returns:** `Void`

#### Overload 2

```python
ChatYell(color: Int32, msg: Int32)
```

**Parameters:**

- `color` (Int32)
- `msg` (Int32)

**Returns:** `Void`

### CheckLayer

```python
CheckLayer(layer: String)
```

Check if a Layer is equipped by the Item.

**Parameters:**

- `layer` (String): Layers:
   RightHand
   LeftHand
   Shoes
   Pants
   Shirt
   Head
   Gloves
   Ring
   Neck
   Hair
   Waist
   InnerTorso
   Bracelet
   FacialHair
   MiddleTorso
   Earrings
   Arms
   Cloak
   OuterTorso
   OuterLegs
   InnerLegs
   Talisman

**Returns:** `Boolean` - True: the Layer is occupied by an Item - False: otherwise.

### ClearCorpseList

```python
ClearCorpseList()
```

Clear the Player corpse item list

**Returns:** `Void`

### DistanceTo

#### Overload 1

```python
DistanceTo(target: UOEntity)
```

Returns the distance between the Player and a Mobile or an Item.

**Parameters:**

- `target` (UOEntity): The other Mobile or Item

**Returns:** `Int32` - Distance in number of tiles.

#### Overload 2

```python
DistanceTo(target: Int32)
```

**Parameters:**

- `target` (Int32)

**Returns:** `Int32`

### EmoteAction

```python
EmoteAction(action: String)
```

**Parameters:**

- `action` (String)

**Returns:** `Void`

### EquipItem

#### Overload 1

```python
EquipItem(serial: Int32)
```

Equip an Item

**Parameters:**

- `serial` (Int32): Serial or Item to equip.

**Returns:** `Void`

#### Overload 2

```python
EquipItem(item: Item)
```

**Parameters:**

- `item` (Item)

**Returns:** `Void`

### EquipLastWeapon

```python
EquipLastWeapon()
```

Equip the last used weapon

**Returns:** `Void`

### EquipUO3D

#### Overload 1

```python
EquipUO3D(serials: List[Int32])
```

**Parameters:**

- `serials` (List[Int32])

**Returns:** `Void`

#### Overload 2

```python
EquipUO3D(_serials: PythonList)
```

Equip a python list of item by using UO3D packet.

**Parameters:**

- `_serials` (PythonList)

**Returns:** `Void`

### Fly

```python
Fly(status: Boolean)
```

Enable or disable Gargoyle Flying.

**Parameters:**

- `status` (Boolean): True: Gargoyle Fly ON - False: Gargoyle fly OFF

**Returns:** `Void`

### GetBuffInfo

```python
GetBuffInfo(buffName: String, okayToGuess: Boolean = True)
```

Check if buff information is active by buff name and returns it.

**Parameters:**

- `buffName` (String): buff name
- `okayToGuess` (Boolean)

**Returns:** `BuffInfo` - Buff information

### GetItemOnLayer

```python
GetItemOnLayer(layer: String)
```

Returns the Item associated with a Mobile Layer.

**Parameters:**

- `layer` (String): Layers:
   RightHand
   LeftHand
   Shoes
   Pants
   Shirt
   Head
   Gloves
   Ring
   Neck
   Hair
   Waist
   InnerTorso
   Bracelet
   FacialHair
   MiddleTorso
   Earrings
   Arms
   Cloak
   OuterTorso
   OuterLegs
   InnerLegs
   Talisman

**Returns:** `Item` - Item for the layer. Return null if not found or Layer invalid.

### GetPropStringByIndex

```python
GetPropStringByIndex(index: Int32)
```

Get a single line of Properties of the Player, from the tooltip, as text.

**Parameters:**

- `index` (Int32): Line number, start from 0.

**Returns:** `String` - Single line of text.

### GetPropStringList

```python
GetPropStringList()
```

Get the list of Properties of the Player, as list of lines of the tooltip.

**Returns:** `List[String]` - List of text lines.

### GetPropValue

```python
GetPropValue(name: String)
```

Get the numeric value of a specific Player property, from the tooltip.

**Parameters:**

- `name` (String): Name of the property.

**Returns:** `Int32` - n: value of the propery 
0: property not found.
1: property found, but not numeric.

### GetRealSkillValue

```python
GetRealSkillValue(skillname: String)
```

Get the base/real value of the skill for the given the skill name.

**Parameters:**

- `skillname` (String): Alchemy
Anatomy
Animal Lore
Item ID
Arms Lore
Parry
Begging
Blacksmith
Fletching
Peacemaking
Camping
Carpentry
Cartography
Cooking
Detect Hidden
Discordance
EvalInt
Healing
Fishing
Forensics
Herding
Hiding
Provocation
Inscribe
Lockpicking
Magery
Magic Resist
Mysticism
Tactics
Snooping
Musicianship
Poisoning
Archery
Spirit Speak
Stealing
Tailoring
Animal Taming
Taste ID
Tinkering
Tracking
Veterinary
Swords
Macing
Fencing
Wrestling
Lumberjacking
Mining
Meditation
Stealth
Remove Trap
Necromancy
Focus
Chivalry
Bushido
Ninjitsu
Spell Weaving
Imbuing

**Returns:** `Double` - Value of the skill.

### GetSkillCap

```python
GetSkillCap(skillname: String)
```

Get the skill cap for the given the skill name.

**Parameters:**

- `skillname` (String): Alchemy
Anatomy
Animal Lore
Item ID
Arms Lore
Parry
Begging
Blacksmith
Fletching
Peacemaking
Camping
Carpentry
Cartography
Cooking
Detect Hidden
Discordance
EvalInt
Healing
Fishing
Forensics
Herding
Hiding
Provocation
Inscribe
Lockpicking
Magery
Magic Resist
Mysticism
Tactics
Snooping
Musicianship
Poisoning
Archery
Spirit Speak
Stealing
Tailoring
Animal Taming
Taste ID
Tinkering
Tracking
Veterinary
Swords
Macing
Fencing
Wrestling
Lumberjacking
Mining
Meditation
Stealth
Remove Trap
Necromancy
Focus
Chivalry
Bushido
Ninjitsu
Spell Weaving
Imbuing

**Returns:** `Double` - Value of the skill cap.

### GetSkillStatus

```python
GetSkillStatus(skillname: String)
```

Get lock status for a specific skill.

**Parameters:**

- `skillname` (String): Alchemy
Anatomy
Animal Lore
Item ID
Arms Lore
Parry
Begging
Blacksmith
Fletching
Peacemaking
Camping
Carpentry
Cartography
Cooking
Detect Hidden
Discordance
EvalInt
Healing
Fishing
Forensics
Herding
Hiding
Provocation
Inscribe
Lockpicking
Magery
Magic Resist
Mysticism
Tactics
Snooping
Musicianship
Poisoning
Archery
Spirit Speak
Stealing
Tailoring
Animal Taming
Taste ID
Tinkering
Tracking
Veterinary
Swords
Macing
Fencing
Wrestling
Lumberjacking
Mining
Meditation
Stealth
Remove Trap
Necromancy
Focus
Chivalry
Bushido
Ninjitsu
Spell Weaving
Imbuing

**Returns:** `Int32` - Lock status:
     0: Up     
     1: Down 
     2: Locked 
    -1: Error

### GetSkillValue

```python
GetSkillValue(skillname: String)
```

Get the value of the skill, with modifiers, for the given the skill name.

**Parameters:**

- `skillname` (String): Alchemy
Anatomy
Animal Lore
Item ID
Arms Lore
Parry
Begging
Blacksmith
Fletching
Peacemaking
Camping
Carpentry
Cartography
Cooking
Detect Hidden
Discordance
EvalInt
Healing
Fishing
Forensics
Herding
Hiding
Provocation
Inscribe
Lockpicking
Magery
Magic Resist
Mysticism
Tactics
Snooping
Musicianship
Poisoning
Archery
Spirit Speak
Stealing
Tailoring
Animal Taming
Taste ID
Tinkering
Tracking
Veterinary
Swords
Macing
Fencing
Wrestling
Lumberjacking
Mining
Meditation
Stealth
Remove Trap
Necromancy
Focus
Chivalry
Bushido
Ninjitsu
Spell Weaving
Imbuing

**Returns:** `Double` - Value of the skill.

### GetStatStatus

```python
GetStatStatus(statname: String)
```

Get lock status for a specific stats.

**Parameters:**

- `statname` (String): Strength
Dexterity
Intelligence

**Returns:** `Int32` - Lock status:
     0: Up     
     1: Down 
     2: Locked

### GuildButton

```python
GuildButton()
```

Press the Guild menu button in the paperdoll.

**Returns:** `Void`

### HeadMessage

#### Overload 1

```python
HeadMessage(color: Int32, msg: String)
```

Display a message above the Player. Visible only by the Player.

**Parameters:**

- `color` (Int32): Color of the Text.
- `msg` (String): Text of the message.

**Returns:** `Void`

#### Overload 2

```python
HeadMessage(color: Int32, msg: Int32)
```

**Parameters:**

- `color` (Int32)
- `msg` (Int32)

**Returns:** `Void`

### InRange

#### Overload 1

```python
InRange(entity: UOEntity, range: Int32)
```

Check if the mobile or item is within a certain range (&lt;=).

**Parameters:**

- `entity` (UOEntity)
- `range` (Int32): Maximum distance in tiles.

**Returns:** `Boolean` - True: Item is in range - False: otherwise.

#### Overload 2

```python
InRange(serial: Int32, range: Int32)
```

Check if the serial is within a certain range (&lt;=).

**Parameters:**

- `serial` (Int32)
- `range` (Int32): Maximum distance in tiles.

**Returns:** `Boolean` - True: serial is in range - False: otherwise.

### InRangeItem

#### Overload 1

```python
InRangeItem(item: Int32, range: Int32)
```

Check if the Item is within a certain range (&lt;=).

**Parameters:**

- `item` (Int32): Serial or Item object.
- `range` (Int32): Maximum distance in tiles.

**Returns:** `Boolean` - True: Item is in range - False: otherwise.

#### Overload 2

```python
InRangeItem(item: Item, range: Int32)
```

**Parameters:**

- `item` (Item)
- `range` (Int32)

**Returns:** `Boolean`

### InRangeMobile

#### Overload 1

```python
InRangeMobile(mobile: Int32, range: Int32)
```

Check if the Mobile is within a certain range (&lt;=).

**Parameters:**

- `mobile` (Int32): Serial or Mobile object.
- `range` (Int32): Maximum distance in tiles.

**Returns:** `Boolean` - True: Mobile is in range - False: otherwise.

#### Overload 2

```python
InRangeMobile(mobile: Mobile, range: Int32)
```

Check if the mobile is within a certain range (&lt;=).

**Parameters:**

- `mobile` (Mobile)
- `range` (Int32): Maximum distance in tiles.

**Returns:** `Boolean` - True: Item is in range - False: otherwise.

### InvokeVirtue

#### Overload 1

```python
InvokeVirtue(virtue: String)
```

Invoke a virtue by name.

**Parameters:**

- `virtue` (String): Honor
Sacrifice
Valor
Compassion
Honesty
Humility
Justice
Spirituality

**Returns:** `Void`

#### Overload 2

```python
InvokeVirtue(virtue: Int32)
```

Invoke a virtue by name.

**Parameters:**

- `virtue` (Int32): Honor
Sacrifice
Valor
Compassion
Honesty
Humility
Justice
Spirituality

**Returns:** `Void`

### KickMember

```python
KickMember(serial: Int32)
```

Kick a member from party by serial. Only for party leader

**Parameters:**

- `serial` (Int32): Serial of the Mobile to remove.

**Returns:** `Void`

### LeaveParty

```python
LeaveParty(force: Boolean = False)
```

Leaves a party.

**Parameters:**

- `force` (Boolean): True: Leave the party invite even you notin any party.

**Returns:** `Void`

### MapSay

#### Overload 1

```python
MapSay(msg: String)
```

Send message in the Map chat.

**Parameters:**

- `msg` (String): Message to send

**Returns:** `Void`

#### Overload 2

```python
MapSay(msg: Int32)
```

**Parameters:**

- `msg` (Int32)

**Returns:** `Void`

### OpenPaperDoll

```python
OpenPaperDoll()
```

Open Player's Paperdoll

**Returns:** `Void`

### PartyAccept

```python
PartyAccept(from_serial: Int32 = 0, force: Boolean = False)
```

Accept an incoming party offer. In case of multiple party oebnding invitation, from_serial is specified,

**Parameters:**

- `from_serial` (Int32): Optional: Serial to accept party from.( in case of multiple offers )
- `force` (Boolean): True: Accept the party invite even you are already in a party.

**Returns:** `Boolean` - True: if you are now in a party - False: otherwise.

### PartyCanLoot

```python
PartyCanLoot(CanLoot: Boolean)
```

Set the Party loot permissions.

**Parameters:**

- `CanLoot` (Boolean)

**Returns:** `Void`

### PartyInvite

```python
PartyInvite()
```

Invite a person to a party. Prompt for a in-game Target.

**Returns:** `Void`

### PathFindTo

#### Overload 1

```python
PathFindTo(x: Int32, y: Int32, z: Int32)
```

Go to the given coordinates using Client-provided pathfinding.

**Parameters:**

- `x` (Int32): X map coordinates or Point3D
- `y` (Int32): Y map coordinates
- `z` (Int32): Z map coordinates

**Returns:** `Void`

#### Overload 2

```python
PathFindTo(Location: Point3D)
```

Go to the position supplied using Client-provided pathfinding.

**Parameters:**

- `Location` (Point3D)

**Returns:** `Void`

#### Overload 3

```python
PathFindTo(Location: Point3D)
```

Go to the position supplied using Client-provided pathfinding.

**Parameters:**

- `Location` (Point3D)

**Returns:** `Void`

### QuestButton

```python
QuestButton()
```

Press the Quest menu button in the paperdoll.

**Returns:** `Void`

### Run

```python
Run(direction: String)
```

Run one step in the specified direction and wait for the confirmation of the new position by the server.
If the character is not facing the direction, the first step only "turn" the Player in the required direction.

Info:
Walking:  5 tiles/sec (~200ms between each step)
Running: 10 tiles/sec (~100ms between each step)

**Parameters:**

- `direction` (String): North
South
East
West
Up
Down
Left
Right

**Returns:** `Boolean` - True: Destination reached - False: Coudn't reach the destination.

### SetSkillStatus

```python
SetSkillStatus(skillname: String, status: Int32)
```

Set lock status for a specific skill.

**Parameters:**

- `skillname` (String): Alchemy
Anatomy
Animal Lore
Item ID
Arms Lore
Parry
Begging
Blacksmith
Fletching
Peacemaking
Camping
Carpentry
Cartography
Cooking
Detect Hidden
Discordance
EvalInt
Healing
Fishing
Forensics
Herding
Hiding
Provocation
Inscribe
Lockpicking
Magery
Magic Resist
Mysticism
Tactics
Snooping
Musicianship
Poisoning
Archery
Spirit Speak
Stealing
Tailoring
Animal Taming
Taste ID
Tinkering
Tracking
Veterinary
Swords
Macing
Fencing
Wrestling
Lumberjacking
Mining
Meditation
Stealth
Remove Trap
Necromancy
Focus
Chivalry
Bushido
Ninjitsu
Spell Weaving
Imbuing
- `status` (Int32): Lock status:
     0: Up     
     1: Down 
     2: Locked

**Returns:** `Void`

### SetStatStatus

```python
SetStatStatus(statname: String, status: Int32)
```

Set lock status for a specific skill.

**Parameters:**

- `statname` (String): Strength
Dexterity
Intelligence
- `status` (Int32): Lock status:
     0: Up     
     1: Down 
     2: Locked

**Returns:** `Void`

### SetStaticMount

```python
SetStaticMount(serial: Int32)
```

Sets serial of mount set in Filter/Mount GUI.

**Parameters:**

- `serial` (Int32)

**Returns:** `Void`

### SetWarMode

```python
SetWarMode(warflag: Boolean)
```

Set war Mode on on/off.

**Parameters:**

- `warflag` (Boolean): True: War - False: Peace

**Returns:** `Void`

### SpellIsEnabled

```python
SpellIsEnabled(spellname: String)
```

Check if spell is active using the spell name (for spells that have this function).

**Parameters:**

- `spellname` (String): Name of the spell.

**Returns:** `Boolean` - True: the spell is enabled - False: otherwise,.

### SumAttribute

```python
SumAttribute(attributename: String)
```

Scan all the equipped Item, returns the total value of a specific property. (ex: Lower Reagent Cost )
NOTE: This function is slow.

**Parameters:**

- `attributename` (String): Name of the property.

**Returns:** `Single` - The total value as number.

### ToggleAlwaysRun

```python
ToggleAlwaysRun()
```

Toggle on/off the awlays run flag. 
NOTE: Works only on OSI client.

**Returns:** `Void`

### TrackingArrow

```python
TrackingArrow(x: UInt16, y: UInt16, display: Boolean, target: UInt32 = 0)
```

Display a fake tracking arrow

**Parameters:**

- `x` (UInt16): X coordinate.
- `y` (UInt16): Y coordinate.
- `display` (Boolean): True = On, False = off
- `target` (UInt32): object serial targeted

**Returns:** `Void`

### UnEquipItemByLayer

```python
UnEquipItemByLayer(layer: String, wait: Boolean = True)
```

Unequip the Item associated with a specific Layer.

**Parameters:**

- `layer` (String): Layers:
   RightHand
   LeftHand
   Shoes
   Pants
   Shirt
   Head
   Gloves
   Ring
   Neck
   Hair
   Waist
   InnerTorso
   Bracelet
   FacialHair
   MiddleTorso
   Earrings
   Arms
   Cloak
   OuterTorso
   OuterLegs
   InnerLegs
   Talisman
- `wait` (Boolean): Wait for confirmation from the server.

**Returns:** `Void`

### UnEquipUO3D

#### Overload 1

```python
UnEquipUO3D(_layers: List[String])
```

**Parameters:**

- `_layers` (List[String])

**Returns:** `Void`

#### Overload 2

```python
UnEquipUO3D(_layers: PythonList)
```

UnEquip a python list of layer names by using UO3D packet.

**Parameters:**

- `_layers` (PythonList)

**Returns:** `Void`

### UpdateKarma

```python
UpdateKarma()
```

Costly! 
Updates the Fame and Karma of the Mobile, but it can take as long as 1 second to complete.

**Returns:** `Boolean` - True if successful, False if not server packet received

### UseSkill

#### Overload 1

```python
UseSkill(skillname: String, target: Int32, wait: Boolean = True)
```

Use a specific skill, and optionally apply that skill to the target specified.

**Parameters:**

- `skillname` (String): Alchemy
Anatomy
Animal Lore
Item ID
Arms Lore
Parry
Begging
Blacksmith
Fletching
Peacemaking
Camping
Carpentry
Cartography
Cooking
Detect Hidden
Discordance
EvalInt
Healing
Fishing
Forensics
Herding
Hiding
Provocation
Inscribe
Lockpicking
Magery
Magic Resist
Mysticism
Tactics
Snooping
Musicianship
Poisoning
Archery
Spirit Speak
Stealing
Tailoring
Animal Taming
Taste ID
Tinkering
Tracking
Veterinary
Swords
Macing
Fencing
Wrestling
Lumberjacking
Mining
Meditation
Stealth
Remove Trap
Necromancy
Focus
Chivalry
Bushido
Ninjitsu
Spell Weaving
Imbuing
- `target` (Int32): Optional: Serial, Mobile or Item to target. (default: null)
- `wait` (Boolean): Optional: True: wait for confirmation from the server (default: False)

**Returns:** `Void`

#### Overload 2

```python
UseSkill(skillname: String, target: Item, wait: Boolean = True)
```

**Parameters:**

- `skillname` (String)
- `target` (Item)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
UseSkill(skillname: String, target: Mobile, wait: Boolean = True)
```

**Parameters:**

- `skillname` (String)
- `target` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 4

```python
UseSkill(skillname: String, wait: Boolean)
```

**Parameters:**

- `skillname` (String)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 5

```python
UseSkill(skillname: String)
```

**Parameters:**

- `skillname` (String)

**Returns:** `Void`

### UseSkillOnly

```python
UseSkillOnly(skillname: String, wait: Boolean)
```

**Parameters:**

- `skillname` (String)
- `wait` (Boolean)

**Returns:** `Void`

### Walk

```python
Walk(direction: String)
```

**Parameters:**

- `direction` (String)

**Returns:** `Boolean`

### WeaponClearSA

```python
WeaponClearSA()
```

Disable any active Special Ability of the weapon.

**Returns:** `Void`

### WeaponDisarmSA

```python
WeaponDisarmSA()
```

Toggle Disarm Ability.

**Returns:** `Void`

### WeaponPrimarySA

```python
WeaponPrimarySA()
```

Toggle on/off the primary Special Ability of the weapon.

**Returns:** `Void`

### WeaponSecondarySA

```python
WeaponSecondarySA()
```

Toggle on/off the secondary Special Ability of the weapon.

**Returns:** `Void`

### WeaponStunSA

```python
WeaponStunSA()
```

Toggle Stun Ability.

**Returns:** `Void`

### Zone

```python
Zone()
```

Get the type of zone in which the Player is currently in.
Regions are defined inside by Config/regions.json.

**Returns:** `String` - Towns
Dungeons
Guarded
Forest
Unknown

