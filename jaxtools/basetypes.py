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

* list - types.ListType (except list members must be base types,
types.TupleType supported by converting to a list)

* dictionary - types.DictType (except dictionary keys must be strings
and values must be base types)

* property jaxtools.basetypes.Property.

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

## Collection base types

The set of base types include two collection types: list and dictionary.
By their nature, collection base type memory requirements are not
predictable. Moreover, base type collections can be nested. Dictionaries
can contain lists and dictionaries as values and lists can contain lists
and dictionaries as list members. While there is no design limit to this
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

## Object base types

The set of base types includes two object types: property and packable.
TODO: Document

Created by Jack William Bell on 2016-10-16.

Copyright (c) 2016, 2018 Jack William Bell. License: MIT"""

from enum import Enum

from jaxtools.typehelpers import isNone, isBool, isString, isInt, \
    isNum, isTuple, isList, isDict, isFunction

##
## Base Type Enumeration.
##

class BaseTypes(Enum):
    """Enumeration of the base type IDs."""
    NULL = 0
    BOOL = 1
    INT = 2
    FLOAT = 8
    DATE = 9
    STRING = 16
    URL = 17
    BLOB = 24
    LIST = 25
    DICTIONARY = 26
    PACKABLE = 32
    UNKNOWN = 255

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


def isPackable(val):
    """Returns true if the passed value is a
    packed state, otherwise returns false."""
    return isinstance(val, Packable)


def isBaseType(val):
    """Returns true if the passed value is a valid base type,
    otherwise returns false."""

    # This if statement is structured this way for a reason. Look at
    # the code using it above before changing it, to make sure you
    # don't break anything or simply do something non-optimal.
    if isNone(val) or isBool(val) or isString(val) or isInt(val) or  \
        isNum(val) or isPackable(val):
        # TODO: Add date, url, and blob checks
        return True
    elif (isList(val) or isTuple(val)) and isBaseTypeList(val):
        return True
    elif isDict(val) and isBaseTypeDict(val):
        return True

    return False


##
## Properties and Packables implementation.
##

class PropertyMeta(object):
    """"""
    def __init__(self, name, type, validator=checkBaseType):
        if not isString(name):
            raise TypeError("'name' is not a valid type.")
        if not isinstance(type, BaseTypes):
            raise TypeError("'type' is not a BaseType enum value.")
        if not isFunction(validator):
            raise TypeError("'validator' is not a valid type.")

        self._name = name
        self._type = type
        self._validator = validator

    def getName(self):
        """"""
        return self._name

    def getType(self):
        """"""
        return self._type

    def validate(self, value):
        """"""
        return self._validator(value, self._type)


# TODO: Design. This is basically a set of uniquely named PropertyMeta objects. Consider
#       if it should also have other attributes, like a schema ID tag and hints.
class PropertySchema(object):
    """"""


# TODO: Consider if this should allow you to set an immutable flag.
class Property(object):
    """"""
    def __init__(self, value, propertyMeta=None):
        if not isinstance(propertyMeta, PropertyMeta):
            raise TypeError("'propertyMeta' is not a PropertyMeta instance or None.")

        self._meta = propertyMeta
        self.setValue(value)

    def getMetadata(self):
        return self._meta

    def getValue(self):
        """"""
        return self._value

    def setValue(self, value):
        """"""
        if self._meta == None or self._meta.validate(value):
            self._value = value
        else:
            raise ValueError("'value' failed validation.")


# TODO: Design. You would read an property's Property Meta, then
#       read the property's value (or something similar with callbacks?).
#       Must support drilling down by
#       providing the property value as a property reader for a
#       collection or object base type. Should support a schema somehow?
class PropertyReader(object):
    """"""


# TODO: Design. You would write one property (or set of property elements)
#       at a time. Must support drilling down by providing a way to
#       get a contained property writer for a collection or object base type.
#       Should support a schema somehow?
class PropertyWriter(object):
    """"""


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
        raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")

    def pack(self, propertyWriter, hints):
        """Implementations must write the current state of the instance to
        the passed property writer, following a state design
        associated with the State ID. To reduce state size, make
        sure to use default values when writing properties. Hints
        may be used to affect how the packing is done or may be
        ignored."""
        raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")

    def unpack(self, propertyReader, hints):
        """Implementations must set the current state of the instance by
        reading from the passed property reader, following a state design
        associated with the State ID. To reduce state size, make
        sure to set default values before reading properties. Hints
        may be used to affect how the unåpacking is done or may be
        ignored."""
        raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")

# TODO: Consider moving this elsewhere.
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
        raise NotImplementedError("Abstract method, must be implemented if subclass supports it.")

    def makePackable(self, propertyReader, hints):
        """Creates a restored instance of a packable object
        from the passed packed propertyWriter instance and hints."""
        obj = self.makeObject(propertyReader.getStateId(), hints)
        obj.unpack(propertyReader, hints)
        return obj


# TODO: Remove the below after making sure there aren't some ideas here we want
#       to preserve.

# TODO: As currently designed it consumes a lot of memory and CPU for deeply nested collection
#   types. Refactor to use a evented callback converter, similar to a SAX style parser,
#   and a similar writer strategy for deserializaton/serialization lets you reduce
#   the overhead to performing them one at a time. Think this through carefully.
#   https://en.wikipedia.org/wiki/Simple_API_for_XML
#   https://rapidjson.org/md_doc_sax.html

def convertToBaseType(val, safeCopy=True):
    """Converts the passed value to a matching base type, if possible.
    Throws an exception if the value cannot be converted. Always returns
    a copy of the value, including for storage and collection types, even
    when the value is already a base type.

    Uses the following strategies:

    * For value types it simply returns a copy of the value converted to
    the closest matching base type (may be the exact same value)

    * For storage types the following is performed:
        - If the value is a string and the string contains an ISO 8601
        formatted date value, the string is converted to a datetime
        - If the value is a string and the string contains a URN in
        RFC 1737/RFC 2141 format, the string is converted to a urn
        - TODO: Determine how blobs are converted, consider making
            the blob base type a bytearray
        - TODO: Consider if there any standard types that could be
            converted to strings or blobs

    * For collection types the following is performed:
        - If the value is a propertysheet or a packedstate, the value
        is cloned
        - If the value is a dictionary or a list it is recursively
        iterated and copied and every value/list member is converted
        appropriately
        - If the value is a dictionary containing the special keys
        for a propertysheet or a packedstate it is converted to
        a propertysheet or a packedstate, as appropriate
    """
    raise NotImplementedError("Not yet implemented...")

def convertToSerializableType(val, safeCopy=True):
    """Converts the passed base type value to a serializeable type, if possible.
    Throws an exception if the value cannot be converted. Always returns
    a copy of the value, including for storage and collection types, even
    when the value is already serializable.

    Uses the following strategies:

    * For value types it simply returns a copy of the value, except:
        - datetime is converted to a string in ISO 8601 format

    * For storage types the following is performed:
        - If the value is a URN it is converted into a string in
        RFC 1737/RFC 2141 format
        - TODO: Determine how blobs are converted
        - Strings are simply copied

    * For collection types the following is performed:
        - If the value is a propertysheet or a packedstate, the value
        is converted to a dictionary and the dictionary is recursively
        made serializable as below
        - If the value is a dictionary or a list it is recursively
        iterated and copied and every value/list member is converted
        appropriately
    """
    raise NotImplementedError("Not yet implemented...")