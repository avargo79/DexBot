# Journal

The Journal class provides access to the message Journal.

## Properties

No properties available.

## Methods

### Clear

#### Overload 1

```python
Clear(toBeRemoved: String)
```

Removes all matching entry from the Jorunal.

**Parameters:**

- `toBeRemoved` (String)

**Returns:** `Void`

#### Overload 2

```python
Clear()
```

Removes all entry from the Jorunal.

**Returns:** `Void`

### FilterText

```python
FilterText(text: String)
```

Store a string that if matched, will block journal message ( case insensitive )

**Parameters:**

- `text` (String): Text to block. case insensitive, and will match if the incoming message contains the text

**Returns:** `Void` - void

### GetJournalEntry

#### Overload 1

```python
GetJournalEntry(afterTimestap: Double = -1)
```

Get a copy of all Journal lines as JournalEntry. The list can be filtered to include *only* most recent events.

**Parameters:**

- `afterTimestap` (Double): Timestap as UnixTime, the number of seconds elapsed since 01-Jan-1970. (default: -1, no filter)

**Returns:** `List[Journal.JournalEntry]` - List of JournalEntry

#### Overload 2

```python
GetJournalEntry(afterJournalEntry: Journal.JournalEntry = None)
```

Get a copy of all Journal lines as JournalEntry. The list can be filtered to include *only* most recent events.

**Parameters:**

- `afterJournalEntry` (Journal.JournalEntry): A JournalEntry object (default: null, no filter)

**Returns:** `List[Journal.JournalEntry]` - List of JournalEntry

### GetLineText

```python
GetLineText(text: String, addname: Boolean = False)
```

Search and return the most recent line Journal containing the given text. (case sensitive)

**Parameters:**

- `text` (String): Text to search.
- `addname` (Boolean): Prepend source name. (default: False)

**Returns:** `String` - Return the full line - Empty string if not found.

### GetSpeechName

```python
GetSpeechName()
```

Get list of speakers.

**Returns:** `List[String]` - List of speakers as text.

### GetTextByColor

```python
GetTextByColor(color: Int32, addname: Boolean = False)
```

Returns all the lines present in the Journal for a given color.

**Parameters:**

- `color` (Int32): Color of the source.
- `addname` (Boolean): Prepend source name. (default: False)

**Returns:** `List[String]` - A list of Journal as lines of text.

### GetTextByName

```python
GetTextByName(name: String, addname: Boolean = False)
```

Returns all the lines present in the Journal for a given source name. (case sensitive)

**Parameters:**

- `name` (String): Name of the source.
- `addname` (Boolean): Prepend source name. (default: False)

**Returns:** `List[String]` - A list of Journal as lines of text.

### GetTextBySerial

```python
GetTextBySerial(serial: Int32, addname: Boolean = False)
```

Returns all the lines present in the Journal for a given serial.

**Parameters:**

- `serial` (Int32): Serial of the source.
- `addname` (Boolean): Prepend source name. (default: False)

**Returns:** `List[String]` - A list of Journal as lines of text.

### GetTextByType

```python
GetTextByType(type: String, addname: Boolean = False)
```

Returns all the lines present in the Journal for a given type. (case sensitive)

**Parameters:**

- `type` (String): Regular
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
- `addname` (Boolean): Prepend source name. (default: False)

**Returns:** `List[String]` - A list of Journal as lines of text.

### RemoveFilterText

```python
RemoveFilterText(text: String)
```

Remove a stored a string that if matched, would block journal message ( case insensitive )

**Parameters:**

- `text` (String): Text to no longer block. case insensitive

**Returns:** `Void` - void

### Search

```python
Search(text: String)
```

Search in the Journal for the occurrence of text. (case sensitive)

**Parameters:**

- `text` (String): Text to search.

**Returns:** `Boolean` - True: Text is found - False: otherwise

### SearchByColor

```python
SearchByColor(text: String, color: Int32)
```

Search in the Journal for the occurrence of text, for a given color. (case sensitive)

**Parameters:**

- `text` (String): Text to search.
- `color` (Int32): Color of the message.

**Returns:** `Boolean` - True: Text is found - False: otherwise

### SearchByName

```python
SearchByName(text: String, name: String)
```

Search in the Journal for the occurrence of text, for a given source. (case sensitive)

**Parameters:**

- `text` (String): Text to search.
- `name` (String): Name of the source.

**Returns:** `Boolean` - True: Text is found - False: otherwise

### SearchByType

```python
SearchByType(text: String, type: String)
```

Search in the Journal for the occurrence of text, for a given type. (case sensitive)

**Parameters:**

- `text` (String): Text to search.
- `type` (String): Regular
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

**Returns:** `Boolean` - True: Text is found - False: otherwise

### WaitByName

```python
WaitByName(name: String, delay: Int32)
```

Pause script and wait for maximum amount of time, for a specific source to appear in Jorunal. (case sensitive)

**Parameters:**

- `name` (String): Name of the source.
- `delay` (Int32): Maximum pause in milliseconds.

**Returns:** `Boolean`

### WaitJournal

#### Overload 1

```python
WaitJournal(text: String, delay: Int32)
```

Pause script and wait for maximum amount of time, for a specific text to appear in Journal. (case sensitive)

**Parameters:**

- `text` (String): Text to search.
- `delay` (Int32): Maximum pause in milliseconds.

**Returns:** `Boolean` - True: Text is found - False: otherwise

#### Overload 2

```python
WaitJournal(msgs: List[String], delay: Int32)
```

**Parameters:**

- `msgs` (List[String])
- `delay` (Int32)

**Returns:** `String`

