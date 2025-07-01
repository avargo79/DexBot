# Spells

The Spells class allow you to cast any spell and use abilities, via scripting.

## Properties

No properties available.

## Methods

### Cast

#### Overload 1

```python
Cast(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast spell using the spell name. See the skill-specific functions to get the full list of spell names.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Name of the spell to cast.
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
Cast(SpellName: String, mobile: Mobile, wait: Boolean = True, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 3

```python
Cast(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastBushido

```python
CastBushido(SpellName: String, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Bushido spell using the spell name.

**Parameters:**

- `SpellName` (String): Honorable Execution
Confidence
Counter Attack
Lightning Strike
Evasion
Momentum Strike
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastChivalry

#### Overload 1

```python
CastChivalry(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Chivalry spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Cleanse By Fire
Close Wounds
Consecrate Weapon
Dispel Evil
Divine Fury
Enemy Of One
Holy Light
Noble Sacrifice
Remove Curse
Sacred Journey
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastChivalry(SpellName: String, mobile: Mobile, wait: Boolean = True)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
CastChivalry(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastCleric

#### Overload 1

```python
CastCleric(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Cleric spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Bark Skin : Turns the druid's skin to bark, increasing physical, poison and energy resistence while reducing fire resistence.
Circle Of Thorns : Creates a ring of thorns preventing an enemy from moving.
Deadly Spores : The enemy is afflicted by poisonous spores.
Enchanted Grove : Causes a grove of magical trees to grow, hiding the player for a short time.
Firefly : Summons a tiny firefly to light the Druid's path. The Firefly is a weak creature with little or no combat skills.
Forest Kin : Summons from a list of woodland spirits that will fight for the druid and assist him in different ways.
Grasping Roots : Summons roots from the ground to entangle a single target.
Hibernate : Causes the target to go to sleep.
Hollow Reed : Increases both the strength and the intelligence of the Druid.
Hurricane : Calls forth a violent hurricane that damages any enemies within range.
Lure Stone : Creates a magical stone that calls all nearby animals to it.
Mana Spring : Creates a magical spring that restores mana to the druid and any party members within range.
Mushroom Gateway : A magical circle of mushrooms opens, allowing the Druid to step through it to another location.
Pack Of Beasts : Summons a pack of beasts to fight for the Druid. Spell length increases with skill.
Restorative Soil : Saturates a patch of land with power, causing healing mud to seep through . The mud can restore the dead to life.
Shield Of Earth : A quick-growing wall of foliage springs up at the bidding of the Druid.
Spring Of Life : Creates a magical spring that heals the Druid and their party.
Swarm Of Insects : Summons a swarm of insects that bite and sting the Druid's enemies.
Treefellow : Summons a powerful woodland spirit to fight for the Druid.
Volcanic Eruption : A blast of molten lava bursts from the ground, hitting every enemy nearby.
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastCleric(SpellName: String, mobile: Mobile, wait: Boolean = True, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 3

```python
CastCleric(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastDruid

#### Overload 1

```python
CastDruid(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Druid spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Angelic Faith : Turns you into an angel, boosting your stats. At 100 Spirit Speak you get +20 Str/Dex/Int. Every 5 points of SS = +1 point to each stat, at a max of +24. Will also boost your Anatomy, Mace Fighting and Healing, following the same formula.
Banish Evil : Banishes Undead targets. Auto kills rotting corpses, lich lords, etc. Works well at Doom Champ. Does not produce a corpse however
Dampen Spirit : Drains the stamina of your target, according to the description
Divine Focus : Heal for more, but may be broken.
Hammer of Faith : Summons a War Hammer with Undead Slayer on it for you
Purge : Cleanses Poison. Better than Cure
Restoration : Resurrection. Brings the target back with 100% HP/Mana
Sacred Boon : A HoT, heal over time spell, that heals 10-15 every few seconds
Sacrifice : Heals your party members when you take damage. Sort of like thorns, but it heals instead of hurts
Smite : Causes energy damage
Touch of Life : Heals even if Mortal Strike or poison are active on the target
Trial by Fire : Attackers receive damage when they strike you, sort of like a temporary RPD buff
- `target` (UInt32): target to use the druid spell on
- `wait` (Boolean)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastDruid(SpellName: String, mobile: Mobile, wait: Boolean = True)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
CastDruid(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastLastSpell

#### Overload 1

```python
CastLastSpell(target: UInt32, wait: Boolean = True)
```

Cast again the last casted spell, on last target.

**Parameters:**

- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)

**Returns:** `Void`

#### Overload 2

```python
CastLastSpell(m: Mobile, wait: Boolean = True)
```

**Parameters:**

- `m` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
CastLastSpell(wait: Boolean = True)
```

**Parameters:**

- `wait` (Boolean)

**Returns:** `Void`

### CastLastSpellLastTarget

```python
CastLastSpellLastTarget()
```

Cast again the last casted spell, on last target.

**Returns:** `Void`

### CastMagery

#### Overload 1

```python
CastMagery(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Magery spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Clumsy
Create Food
Feeblemind
Heal
Magic Arrow
Night Sight
Reactive Armor
Weaken
Agility
Cunning
Cure
Harm
Magic Trap
Magic Untrap
Protection
Strength
Bless
Fireball
Magic Lock
Poison
Telekinesis
Teleport
Unlock
Wall of Stone
Arch Cure
Arch Protection
Curse
Fire Field
Greater Heal
Lightning
Mana Drain
Recall
Blade Spirits
Dispel Field
Incognito
Magic Reflection
Mind Blast
Paralyze
Poison Field
Summon Creature
Dispel
Energy Bolt
Explosion
Invisibility
Mark
Mass Curse
Paralyze Field
Reveal
Chain Lightning
Energy Field
Flamestrike
Gate Travel
Mana Vampire
Mass Dispel
Meteor Swarm
Polymorph
Earthquake
Energy Vortex
Resurrection
Summon Air Elemental
Summon Daemon
Summon Earth Elemental
Summon Fire Elemental
Summon Water Elemental
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastMagery(SpellName: String, mobile: Mobile, wait: Boolean = True)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
CastMagery(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastMastery

#### Overload 1

```python
CastMastery(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Mastery spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Inspire
Invigorate
Resilience
Perseverance
Tribulation
Despair
Death Ray
Ethereal Blast
Nether Blast
Mystic Weapon
Command Undead
Conduit
Mana Shield
Summon Reaper
Enchanted Summoning
Anticipate Hit
Warcry
Intuition
Rejuvenate
Holy Fist
Shadow
White Tiger Form
Flaming Shot
Playing The Odds
Thrust
Pierce
Stagger
Toughness
Onslaught
Focused Eye
Elemental Fury
Called Shot
Saving Throw
Shield Bash
Bodyguard
Heighten Senses
Tolerance
Injected Strike
Potency
Rampage
Fists Of Fury
Knockout
Whispering
Combat Training
Boarding
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastMastery(SpellName: String, mobile: Mobile, wait: Boolean = True)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
CastMastery(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastMysticism

#### Overload 1

```python
CastMysticism(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Mysticism spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Animated Weapon
Healing Stone
Purge
Enchant
Sleep
Eagle Strike
Stone Form
SpellTrigger
Mass Sleep
Cleansing Winds
Bombard
Spell Plague
Hail Storm
Nether Cyclone
Rising Colossus
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastMysticism(SpellName: String, mobile: Mobile, wait: Boolean = True)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
CastMysticism(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastNecro

#### Overload 1

```python
CastNecro(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Necromany spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Curse Weapon
Pain Spike
Corpse Skin
Evil Omen
Blood Oath
Wraith Form
Mind Rot
Summon Familiar
Horrific Beast
Animate Dead
Poison Strike
Wither
Strangle
Lich Form
Exorcism
Vengeful Spirit
Vampiric Embrace
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastNecro(SpellName: String, mobile: Mobile, wait: Boolean = True)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
CastNecro(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastNinjitsu

#### Overload 1

```python
CastNinjitsu(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Ninjitsu spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Animal Form
Backstab
Surprise Attack
Mirror Image
Shadow jump
Focus Attack
Ki Attack
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastNinjitsu(SpellName: String, mobile: Mobile, wait: Boolean = True, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 3

```python
CastNinjitsu(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### CastSpellweaving

#### Overload 1

```python
CastSpellweaving(SpellName: String, target: UInt32, wait: Boolean = True, waitAfter: Int32 = 0)
```

Cast a Spellweaving spell using the spell name.
Optionally is possible to specify the Mobile or a Serial as target of the spell. Upon successful casting, the target will be executed automatiaclly by the server.
NOTE: The "automatic" target is not supported by all shards, but you can restort to the Target class to handle it manually.

**Parameters:**

- `SpellName` (String): Arcane Circle
Gift Of Renewal
Immolating Weapon
Attune Weapon
Thunderstorm
Natures Fury
Summon Fey
Summoniend
Reaper Form
Wildfire
Essence Of Wind
Dryad Allure
Ethereal Voyage
Word Of Death
Gift Of Life
Arcane Empowerment
- `target` (UInt32): Optional: Serial or Mobile to target (default: null)
- `wait` (Boolean): Optional: Wait server to confirm. (default: True)
- `waitAfter` (Int32)

**Returns:** `Void`

#### Overload 2

```python
CastSpellweaving(SpellName: String, mobile: Mobile, wait: Boolean = True)
```

**Parameters:**

- `SpellName` (String)
- `mobile` (Mobile)
- `wait` (Boolean)

**Returns:** `Void`

#### Overload 3

```python
CastSpellweaving(SpellName: String, waitAfter: Int32 = 0)
```

**Parameters:**

- `SpellName` (String)
- `waitAfter` (Int32)

**Returns:** `Void`

### Interrupt

```python
Interrupt()
```

Interrupt the casting of a spell by performing an equip/unequip.

**Returns:** `Void`

