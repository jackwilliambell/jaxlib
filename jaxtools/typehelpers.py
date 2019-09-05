"""typehelpers.py
Copyright (c) 2015, 2019 Jack William Bell. All rights reserved.

Various helper functions for dealing with types. Many
of these could be inlined easily, but even the most
idiomatic implementations might not result in easily
readable code. If nothing else, copying the source
here will be faster than doing a web search.

NOTE: In most cases your code should simply attempt to use a
type within a try/catch block, as 'easier to ask forgiveness
than permission' is the most idiomatic way of writing Python.
These functions are meant for the rare cases where 'Duck Typing'
isn't a valid choice."""

from builtins import str
import collections

def isNone(val):
    """Returns true if the passed value is the Python None
    type, otherwise false.
    
    **Parameters:**
    
    * val - value to test
    
    **Returns:**
    
    True if the passed value is None, otherwise false."""
    return val is None

def isBool(val):
    """Returns true if the passed value is the Python booleanf
    type, otherwise false.
    
    **Parameters:**
    
    * val - value to test
    
    **Returns:**
    
    True if the passed value is a boolean, otherwise false."""
    return isinstance(val, bool)

def isString(val):
    """Returns true if the passed value is a Python string
(ASCII or Unicode) type, otherwise false.

**Parameters:**

* val - The name of the file to open; must be a
valid file for the current diretory context

**Returns:**

True if the passed value is a list, otherwise false."""
    return isinstance(val, str)

def isInt(val):
    """Returns true if the passed value is a Python integer
value, otherwise false. (Returns true for any numeric type that is
an integer value, with no decimal places.)

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is an integer value, otherwise false."""
    # Does it have the right interface?
    if isinstance(val, int):
        return True
    elif isinstance(val, float):
        # Is it an integer?
        return val.is_integer()
    
    return False

def isNum(val):
    """Returns true if the passed value is a Python numeric
value, otherwise false. (Returns true for any numeric type.)

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is a numeric value, otherwise false."""
    # Does it have the right interface?
    if isinstance(val, int):
        return True
    elif isinstance(val, float):
        return True
    
    return False

def isTuple(val):
    """Returns true if the passed value is a Python tuple type,
otherwise false.

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is a tuple, otherwise false."""
    return isinstance(val, tuple)

def isList(val):
    """Returns true if the passed value is a Python list type,
otherwise false.

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is a list, otherwise false."""
    return isinstance(val, list)

def isDict(val):
    """Returns true if the passed value is a python
dictionary type, otherwise false.

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is a dictionary, otherwise false."""
    return isinstance(val, dict)

def isIterable(val):
    """Returns true if the passed value is an iterable
type, otherwise false.

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is iterable, otherwise false."""
    if not isinstance(val, str ):
        return isinstance(val, collections.Iterable)
    
    return False

