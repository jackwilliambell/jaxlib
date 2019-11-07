"""# Base Types

Base types are a set of basic data types that
are easy to serialize and are either a standard 
type of nearly every programming languge or are
easy to implement/emulate if not.

Base types include low-level value types like boolean and
int along with a storage types like string and blob, a
set of common data structures like list and dictionary,
and the Packable type, which more complex objects can inherit
from to support easy serialization/deserialization.

## List of base types

These types, their tags, and their Python representations are:

* null - types.NoneType

* bool - types.BooleanType

* int - types.IntType, types.LongType

* float - types.FloatType

* datetime - datetime.datetime

* string - types.StringType, types.UnicodeType

* urn - urllib.request.Request

* TODO: Add 'tag' type with a name, date, other? See user-defined tags as used in YAML.

* blob - types.BufferType

* pair - types.TupleType of two members, (except the first member of the pair *must*
be a string and values must be base types; a base type dictionary is essentially a
list of pairs)

* list - types.ListType (except list members must be base types,
types; TupleType supported by converting to a list)

* dictionary - types.DictType (except dictionary keys must be strings
and values must be base types)

* packable - jaxtools.basetypes.Packable

## Goals

* Restrict data values to a small, but comprehensive, set of known
types; where the types are easy to serialize and are either a standard
type of nearly every programming languge or are easy to
implement/emulate if not

* Provide a predictable machine and language-independent way to store
data and to transfer data between applications

* Provide a predictable machine and language-independent way to ensure
data interchange by serializing to and deserializing from common wire
data transfer formats such as JSON and YAML or even HTTP MIME types
such as 'multipart/form-data'

* Provide a predictable machine and language-independent way to
represent the state of common objects; IE objects with similar state
and implementations, but not using the same classes or even the same
programming language (See 'packables')

## Non-goals

* Base types are not meant for general computation, so usages other
than data storage or data interchange may be non-optimal; especially
for collection types

* No attempt is made to optimize for processing speed or memory and
some base type APIs may be particuarily slow when used with large or
deeply nested collections (See isBaseType() and the to/from dictionary
methods of propertysheet and packedstate)

## Value base types

The set of base types includes five value types: null, bool, int,
float, and date. All value types may be represented in memory with
a known byte size, making their memory requirements predictable.

In general all value types will work the same for all APIs and
when transferred to another base type software implementation.

## Storage base types

The set of base types includes three storage types: string, url, and
blob. Storage types contain zero to N bytes and their memory
requirements are not predictable.

While there is no design limit to the upper size of storage types, in
practice the total number of bytes you can store in each storage type
is determined by the programming language and the implementation of the
type. Moreover, particularity large storage types may fail to work
properly or cause exceptions when passed to some APIs or when
transferred to another base type software implementation.

In general it is best to avoid very large byte sizes in storage types
if possible and to test carefully if not. As a rule of thumb, storage
types with less than 256K total bytes are probably fine while storage
types which exceed that limit may be problematic.

(NOTE: Python strings on a 64-bit machine may use hundreds of gigabytes
of memory, but that does not mean APIs you pass them to will work properly.)

TODO: Add tag type here. Also implement tag type or otherwise define it.

## Collection base types

TODO: pair is not a collection type. Move and rewrite it's explanation. May
  need to come up with new type nomeclature.

The set of base types include three collection types: pair, list and
dictionary. By their nature, collection base type memory requirements are not
predictable. Moreover, base type collections can be nested. Pairs and dictionaries
can contain pairs, lists and dictionaries as values and lists can contain pairs,
lists and dictionaries as list members. While there is no design limit to this
nesting, in practice deeply nested collections may fail to work properly
or cause exceptions when passed to some APIs or when transferred to
another base type software implementation.

Particularity large collections, with or without nesting, may also fail
to work properly or cause exceptions when passed to some APIs. Also, large
value types as collection members, such as very large strings or blobs, may
cause problems as well.

In general it is best to avoid large and/or deeply nested collections if
possible and to test carefully if not. As a rule of thumb, collections with
less than 1K members or 8 deep nesting are probably fine while collections
which exceed those limits may be problematic.

## Packable base type

There is one 'packable' base type, which is simply an object that supports
the Packable interface and can be 'packed' and 'unpacked'.

Created by Jack William Bell on 2016-10-16.

Copyright (c) 2016, 2018 Jack William Bell. License: MIT"""

from enum import Enum

from jaxtools.typehelpers import isNone, isBool, isString, isInt, \
    isNum, isTuple, isList, isDict, isFunction

##
## Base Type Enumeration.
##

class BaseTypeIds(Enum):
    """Enumeration of the base type IDs."""
    NULL = 0
    BOOL = 1
    INT = 4
    FLOAT = 8
    DATE = 16
    STRING = 17
    URL = 18
    TAG = 19
    BLOB = 20
    PAIR = 24
    TRIPLET = 25
    LIST = 32
    DICTIONARY = 33
    PACKABLE = 48
    END = 255

##
## Helper functions.
##

def checkBaseType(val, baseTypeEnum):
    """Returns true if the passed value is a valid type for the
    passed Base Types enumeration."""
    raise NotImplementedError("Not yet implemented...")


def isBaseTypeList(val):
    """Returns true if the passed value is a list where all members
    are valid base types."""
    # Is it a list?
    if isList(val) or isTuple(val):
        # Iterate.
        for v in val:
            # If the value is a list, recurse for failure.
            if (isList(v) or isTuple(v)) and not isBaseTypeList(v):
                return False
            # If the value is a dict, recurse for failure.
            elif isDict(v) and not isBaseTypeDict(v):
                return False
            # Otherwise, is the value a base type at all?.
            elif not isBaseType(v):
                return False
    else:
        return False  # Not a list.

    return True


def isBaseTypeDict(val):
    """Returns true if the passed value is a dictionary where all keys
    are strings and values are valid base types."""
    # Is it a dict?
    if isDict(val):
        # Iterate.
        for k, v in val.items():
            # If the key is not a string, it's invalid.
            if not isString(k):
                return False
            # If the value is a list, recurse for failure.
            elif (isList(v) or isTuple(v)) and not isBaseTypeList(v):
                return False
            # If the value is a dict, recurse for failure.
            elif isDict(v) and not isBaseTypeDict(v):
                return False
            # Otherwise, is the value a base type at all?.
            elif not isBaseType(v):
                return False
    else:
        return False  # Not a dict.

    return True


def isValueType(val):
    """"""
    return isNone(val) or isBool(val) or isInt(val) or isNum(val)

def isStorageType(val):
    """"""
    # TODO: Add date, url, tag, and blob checks
    return isString(val)


def isCollectionType(val):
    """"""
    if (isList(val) or isTuple(val)) and isBaseTypeList(val):
        return True
    elif isDict(val) and isBaseTypeDict(val):
        return True

    return False


def isPackableType(val):
    """Returns true if the passed value is a packable object, otherwise returns false."""
    return isinstance(val, Packable)


def isBaseType(val):
    """Returns true if the passed value is a valid base type,
    otherwise returns false."""

    # This if statement is structured this way for a reason. Look at
    # the code using it above before changing it, to make sure you
    # don't break anything or simply do something non-optimal.
    if isNone(val) or isBool(val) or isString(val) or isInt(val) or  \
        isNum(val) or isPackableType(val):
        # TODO: Add date, url, tag, and blob checks
        return True
    elif (isList(val) or isTuple(val)) and isBaseTypeList(val):
        return True
    elif isDict(val) and isBaseTypeDict(val):
        return True

    return False


##
## Packables.
##

class Packable(object):
    """An Abstract Base Class that supports 'packing'
    the state of an object to a PropertyWriter instance and
    'unpacking' the state of an object from a PropertyReader
    instance.

    **Description:**

    The process of 'packing' is simply writing any state
    values as named properties to a passed PropertyWriter instance following
    a known 'state design' that can later be unpacked by
    any class implementing the same state design. Each state
    design is associated with a particular State ID and
    state designs may be versioned within a State ID using a date.

    Different classes may support the same State ID, so long
    as they also support the same state design and interface;
    meaning they are interchangable and runtime Polymorphic. For
    classes that might be dangerous if unpacked using states from
    unknown sources it is generally a good idea to provide a
    known safe version of the Packable object to use locally.
    See PackableFactory class."""

    def getStateId(self):
        """Implementations must return the State ID associated
        with the Packable object's state design and interface."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def pack(self, propertyWriter, hints):
        """Implementations must write the current state of the instance to
        the passed property writer, following a state design
        associated with the State ID. To reduce state size, make
        sure to use default values when writing properties. Hints
        may be used to affect how the packing is done or may be
        ignored."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def unpack(self, propertyReader, hints):
        """Implementations must set the current state of the instance by
        reading from the passed property reader, following a state design
        associated with the State ID. To reduce state size, make
        sure to set default values before reading properties. Hints
        may be used to affect how the unåpacking is done or may be
        ignored."""
        raise NotImplementedError("Abstract method, must be implemented.")


class PackableFactory(object):
    """An abstract Base Class that supports creating new
    instances of packable objects from a Packed State. These
    instances do not have to be of the same class as was
    packed so long as they support the same state format.
    PackableFactory implementations may be 'chained' using a
    parent factory such that if the current factory doesn't
    support the State ID of the Packed State, the parent may
    be invoked. If the parent does not supports the State ID
    it may invoke its parent, and so on.

    To create a PackableFactory, implement the makeObject()
    method to create an object instance based on the state ID."""

    def makeObject(self, stateId, hints):
        """Creates a clean instance of a packable object for
        the passed state ID, optionally using the hints."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def makePackable(self, propertyReader, hints):
        """Creates a restored instance of a packable object
        from the passed packed propertyWriter instance and hints."""
        obj = self.makeObject(propertyReader.getStateId(), hints)
        obj.unpack(propertyReader, hints)
        return obj


##
## Base Type reader/writer APIs.
##

class BaseTypeReader(object):
    """An Abstract Base Class for base type reader implementations, where the elements
    are iterated as tuples consisting of the base type ID and the base type value, if
    the element is not a pair, collection or packable type.

    If the element is a pair type the tuple contains only the base type ID and the pair name,
    the next element iterated after this 'header' is the pair value, but no 'END" marker is
    required, as for collection and packable types. The value is subject to nesting such
    that pair values which are collection or packable types have their own headers and
    'END' markers.

    If the element is a list type the tuple contains only the base type ID and
    every element iterated after this 'header' is a member of the list, until an 'END'
    base type ID is sent to indicate the end of the list. The value is subject to nesting such
    that list elements which are collection or packable types have their own headers and
    'END' markers.

    If the element is a dictionary type the tuple contains only the base type ID and
    the elements iterated after this 'header' are the member of the dictionary in the form
    of a pair name/value sets, until an 'END' base type ID is sent to indicate the end of the
    dictionary. The value is subject to nesting such that dictionary elements where the values
    are collection or packable types have their own headers and 'END' markers.

    If the element is a packable type the tuple contains the base type ID and the packable header
    and every element iterated after this 'header' is a member of the property list of the
    packed object in the form of a pair element, until an 'END' base type ID is sent to indicate
    the end of the packable. The value is subject to nesting such that packable properties where
    the property values are collection or packable types have their own headers and 'END' markers.

    TODO: Implementation notes and rules for iterating."""
    def __iter__(self):
        raise NotImplementedError("Abstract method, must be implemented.")

    def close(self):
        """Closes the reader and releases its resources."""
        pass # Abstract method, may be implemented.


# TODO: Rewrite this function to use a callback object inheriting from a ABC instead of
#   using discrete callback functions.
def readWithCallbacks(reader, onValueFunc, onListFunc, onDictFunc, onPackableFunc, onEndFunc):
    """Helper function for reading using SAX-style callbacks with a BaseTypeReader instance. All
    callback functions must return either true or false and, if false is returned, this function
    will exit and reading will stop."""
    raise NotImplementedError("TODO.")


def readObject(reader, packableFactory=None):
    """Helper function for reading a collection or packable object from a BaseTypeReader instance.
    If the reader contents contain packables, you will need to provide a compatible packable
    factory instance.

    Reads one object at a time. If the reader contains more data after the end marker for the
    object you will need to read again."""
    raise NotImplementedError("TODO.") # NOTE: Implement using a callback instance.


class BaseTypeWriter(object):
    """An Abstract Base Class for base type reader implementations, where collections and
    packable types are written using a start/end syntax. Works as the converse of a BaseTypeReader
    implementation."""

    def writeNullValue(self):
        """Writes a null value."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeBoolValue(self, value):
        """Writes a boolean value. The passed value must be a boolean or convertible to a boolean."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeIntValue(self, value):
        """Writes a integer value. The passed value must be a integer or convertible to a integer."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeFloatValue(self, value):
        """Writes a float value. The passed value must be a float or convertible to a float."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeDateValue(self, value):
        """Writes a date value. The passed value must be a datetime or convertible to a datetime."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeStringValue(self, value):
        """Writes a string value. The passed value must be a string or convertible to a string."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeUrlValue(self, value):
        """Writes a url value. The passed value must be a url or convertible to a url."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeTagValue(self, value):
        """Writes a tag value. The passed value must be a tag or convertible to a tag."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeBlobValue(self, value):
        """Writes a blob value. The passed value must be a blob or convertible to a blob."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writePairStart(self, name):
        """Writes the name portion of a pair, after which the next write is the value portion, do
        not call writeEnd() after writing the value, as you would with a collection or packable write."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeListStart(self):
        """Signals the start of a list, after which all writes are list members until you call
        writeEnd()."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeDictionaryStart(self):
        """Signals the start of a list, after which all writes are dictionary members in the form
        of writePairStart() and pair value writes until you call writeEnd()."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writePackableStart(self, packableHeader):
        """Signals the start of a packable, after which all writes are object properties in the form
        of writePairStart() and pair value writes until you call writeEnd()."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def writeEnd(self):
        """Indicates the end of a collection or packable write."""
        raise NotImplementedError("Abstract method, must be implemented.")

    def close(self):
        """Closes the writer and releases its resources."""
        pass # Abstract method, may be implemented.


def writeObject(writer, obj):
    """Helper function for writing a collection or packable object to a BaseTypeWriter instance.

    Writes one object at a time. If you want to write another object to the same writer you will
    need to write again."""
    raise NotImplementedError("TODO.")
