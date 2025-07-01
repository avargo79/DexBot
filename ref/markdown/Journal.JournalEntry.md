# Journal.JournalEntry

The JournalEntry class rapresents a line in the Journal.

## Properties

### Color

**Type:** `Int32`

Color of the text.

### Name

**Type:** `String`

Name of the source, can be a Mobile or an Item.

### Serial

**Type:** `Int32`

Name of the source, can be a Mobile or an Item.

### Text

**Type:** `String`

Actual content of the Journal Line.

### Timestamp

**Type:** `Double`

Timestamp as UnixTime, the number of seconds elapsed since 01-Jan-1970.

### Type

**Type:** `String`

Regular
System
Emote
Label
Focus
Whisper
Yell
Spell
Guild
Alliance
Party
Encoded
Special

## Methods

### Copy

```python
Copy()
```

**Returns:** `Journal.JournalEntry`

