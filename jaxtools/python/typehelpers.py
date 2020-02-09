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
import datetime
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
    """Returns true if the passed value is the Python boolean
    type, otherwise false.

    NOTE: Does not return true if not an actual bool type. Other
    numeric types return false.
    
    **Parameters:**
    
    * val - value to test
    
    **Returns:**
    
    True if the passed value is a boolean, otherwise false."""
    return type(val) is bool


def isInt(val):
    """Returns true if the passed value is an int
    value, otherwise false.

    NOTE: Returns true only if the value is an int type. See
    isIntNum() for a less restrictive test.

    **Parameters:**

    * val - value to test

    **Returns:**

    True if the passed value is a int value, otherwise false."""
    return not isBool(val) and type(val) is int


def isFloat(val):
    """Returns true if the passed value is a float
    value, otherwise false.

    NOTE: Returns true only if the value is a float type. See
    isNum() for a less restrictive test.

    **Parameters:**

    * val - value to test

    **Returns:**

    True if the passed value is a float, otherwise false."""
    return type(val) is float


def isNum(val):
    """Returns true if the passed value is a Python numeric
    value, otherwise false. (Returns true for any numeric type.)

    NOTE: Returns true for any numeric type. Does not return true
    for bool type values.

    **Parameters:**

    * val - value to test

    **Returns:**

    True if the passed value is a numeric value, otherwise false."""
    if not isBool(val):
        return isinstance(val, (int, float))

    return False


def isIntNum(val):
    """Returns true if the passed value is a Python integer
    value, otherwise false. (Returns true for any numeric type that is
    an integer value, with no decimal places.)

    NOTE: Returns true for any numeric type that is an integer value
    (no decimals). Does not return true for bool type values.

    **Parameters:**

    * val - value to test

    **Returns:**

    True if the passed value is an integer value, otherwise false."""
    if not isBool(val):
        if isinstance(val, int):
            return True
        elif isinstance(val, float):
            # Is it an integer?
            return val.is_integer()

    return False


def isDateTime(val):
    """Returns true if the passed value is a Python datetime.datetime type,
otherwise false.

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is a datetime.datetime, otherwise false."""
    return isinstance(val, datetime.datetime)


def isDate(val):
    """Returns true if the passed value is a Python datetime.date type,
otherwise false.

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is a datetime.date, otherwise false."""
    return isinstance(val, datetime.date)


def isTime(val):
    """Returns true if the passed value is a Python datetime.time type,
otherwise false.

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is a datetime.date, otherwise false."""
    return isinstance(val, datetime.time)


def isString(val):
    """Returns true if the passed value is a Python string
(ASCII or Unicode) type, otherwise false.

**Parameters:**

* val - The name of the file to open; must be a
valid file for the current diretory context

**Returns:**

True if the passed value is a list, otherwise false."""
    return isinstance(val, str)


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


def isFunction(val):
    """Returns true if the passed value is a Function
type, otherwise false.

**Parameters:**

* val - value to test

**Returns:**

True if the passed value is a function, otherwise false."""
    return callable(val)

