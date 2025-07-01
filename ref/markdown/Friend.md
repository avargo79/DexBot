# Friend



## Properties

No properties available.

## Methods

### AddFriendTarget

```python
AddFriendTarget()
```

**Returns:** `Void`

### AddPlayer

```python
AddPlayer(friendlist: String, name: String, serial: Int32)
```

Add the player specified to the Friend list named in FriendListName parameter

**Parameters:**

- `friendlist` (String): Name of the the Friend List. (See Agent tab)
- `name` (String): Name of the Friend want to add.
- `serial` (Int32): Serial of the Friend you want to add.

**Returns:** `Void`

### ChangeList

```python
ChangeList(friendlist: String)
```

Change friend list, List must be exist in friend list GUI configuration

**Parameters:**

- `friendlist` (String): Name of the list of friend.

**Returns:** `Void`

### GetList

```python
GetList(friendlist: String)
```

Retrive list of serial in list, List must be exist in friend Agent tab.

**Parameters:**

- `friendlist` (String): Name of the list of friend.

**Returns:** `List[Int32]`

### IsFriend

```python
IsFriend(serial: Int32)
```

Check if Player is in FriendList, returns a bool value.

**Parameters:**

- `serial` (Int32): Serial you want to check

**Returns:** `Boolean` - True: if is a friend - False: otherwise

### RemoveFriend

```python
RemoveFriend(friendlist: String, serial: Int32)
```

Remove the player specified from the Friend list named in FriendListName parameter

**Parameters:**

- `friendlist` (String): Name of the the Friend List. (See Agent tab)
- `serial` (Int32): Serial of the Friend you want to remove.

**Returns:** `Boolean`

