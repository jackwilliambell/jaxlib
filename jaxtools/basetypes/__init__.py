"""Created by Jack William Bell on 2016-10-16, last updated 2019-12-10.

Copyright (c) 2016, 2018, 2019 Jack William Bell. License: MIT

# Base Types

Base types are a set of basic data types, all of which are easy to serialize and are
either a standard type of nearly every programming languge or are easy to
implement/emulate if not.

Base types include low-level value types like boolean and int, storage types like
string and blob, a set of common data structures like color and geolocation,
collections like list and dictionary, and the Packable type – more complex objects can
inherit from to support easy serialization/deserialization.

## Goals

* Provide a predictable machine and language-independent way to store data and to
transfer data between applications

* Restrict data values to a small, but comprehensive, set of known types; where the
types are easy to serialize and are either a standard type of nearly every programming
languge or are easy to implement/emulate if not

* Provide a predictable machine and language-independent way to ensure data interchange
by serializing to and deserializing from standard data interchange formats such as JSON
and YAML or even common wire data transfer formats like HTTP MIME types and
'multipart/form-data' - Object types not directly supported by standard data
interchange formats must remain serializable to the syntax of those formats using
format-appropriate rules and representations

* Provide a rich set of object types not directly supported by the standard data
interchange formats, but which do enable common use cases and arbitrary object types

* Provide a predictable machine and language-independent way to represent the state of
arbitrary objects; so long as the object's state can be represented in base types (See
'packables')

* Provide a predictable machine and language-independent way to represent the state of
Common Objects (CO); IE objects with similar state and implementations, but not using
the same classes or even the same programming language (See 'packables')

* Provide a high level of safety when deserializing objects from unknown sources

## Non-goals

* Base types are not meant for general computation, so usages other than data storage
or data interchange may be non-optimal; especially for structure and collection types

* No attempt is made to optimize for processing speed or memory and some base type APIs
may be particuarily slow when used with large/deeply nested collections or packable
objects

* Base types do not support every possible object type

* Base types do not support every possible data interchange format

## Tags

TODO: describe the tags and how they are used.

## Schemas

TODO: describe schemas and how they are used.

## Serialization

When serializing base type values to a data interchange format you should always use
the corresponding types supported by that format. If the format does not support a
particular type (for example, JSON doesn't directly support int or datetime primitives)
you should use a commonly accepted way of encoding the data (for example, with JSON use
int and float both as JSON number types and convert datetime to a JSON string using ISO
8601 format). You may need to provide a 'hint' (as an element attribute, as part of a
structure, or even added to the key value) to specify the type when deserializing. A
better option is to serialize appropriately for the type and deserialize using a
schema. Using 'recognizers' to intuit the base types from encoded data interchange
types is not recommended.

Value base types are most likely to be supported by a data interchange format's
primitive types. Storage base type support may only be in the form of strings, but
other storage types have common string representations and there are common ways of
encoding blobs to strings (most notably Base64). Structure base types should be in the
form of lists or tuples (if supported by the data interchange format) using the
definition for each type; there is no need to use a dictionary and specify structure
type field keys. Collection base types may be supported directly by the data
interchange format; if not some commonly accepted encoding may be used. The packable
base type is supported by writing the object contents out to a dictionary with a header
and an associated schema and reversing the process by reading the dictionary in.

## Value base types

Value types are a commonly used subset of primitive data values. All value types may be
represented in memory with a known byte size, making their memory requirements
predictable. The set of base types includes five value types: null, bool, int, float,
and datetime.

In general all value types will work the same for all APIs and when transferred to
another base type software implementation.

The value types, their tags, and their Python representations are:

* null – "tag:bt.co,2019:null" – types.NoneType

* bool – "tag:bt.co,2019:bool" – types.BooleanType

* int – "tag:bt.co,2019:int" – types.IntType, types.LongType

* float – "tag:bt.co,2019:float" – types.FloatType

* datetime – "tag:bt.co,2019:datetime" – datetime.datetime

## Storage base types

Storage base types consist of simple and commonly used types that contain zero to N
bytes of data and their storage requirements are not predictable. They may provide
methods to access their contents by offset or by some structured chunk. The set of base
types includes four storage types: string, urn, tag, and blob.

While there is no design limit to the upper size of storage types, in practice the
total number of bytes you can store in each storage type is determined by the
programming language and the implementation of the type. Moreover, particularity large
storage types may fail to work properly or cause exceptions when passed to some APIs or
when transferred to another base type software implementation.

In general it is best to avoid very large byte sizes in storage types, if possible, and
to test carefully if not. As a rule of thumb, storage types with less than 256K total
bytes are probably fine while storage types which exceed that limit may be problematic.

(NOTE: Python strings on a 64-bit machine may use hundreds of gigabytes of memory, but
that does not mean APIs you pass them to will work properly.)

The value types, their tags, and their Python representations are:

* string – "tag:bt.co,2019:string" – types.StringType, types.UnicodeType

* urn – "tag:bt.co,2019:urn" – TODO: Consider use cases. Create a URN type? Make URI
instead?

* tag – "tag:bt.co,2019:tag" – jaxtools.basetypes.Tag

* blob – "tag:bt.co,2019:blob" – types.BufferType

## Structure base types

Structure base types consist of simple and commonly used data structures with a wide
variety of use cases. Because some structure types may contain storage or collection
base types as field values, their memory requirements are not predictable. (See also,
storage base types and collection base types.)

There are currently only a limited set of structure base types. In the future more may
be added to the official set. You can also create custom structure types using
collection types with a schema.

Structure types are data only and are not objects in the sense that they have methods.
In most cases structure types are likely to require conversion to a different, but
similar, form before they may be used with local APIs. They may include data members
not required for local usage. They may be used in ways different than the usage alluded
to by their name.

The value types, their tags, and their Python representations (more detail below) are:

* pair – "tag:bt.co,2019:pair" – types.TupleType of two members: name and value

* geolocation – "tag:bt.co,2019:geolocation" – types.TupleType of three members:
lattitude, longitude, altitude

* color – "tag:bt.co,2019:color" – types.TupleType of three to seven members:
(required) red, green, blue; (optional) alpha, hue, saturation

* predicate – "tag:bt.co,2019:predicate" – types.TupleType of three members: object,
verb, subject

### Pair

Pairs are represented as a 2-tuple where the first member of the pair *must be* a
non-empty string and the second member *must be* a base type value other than a pair;
in other words a pair cannot directly contain another pair and pairs cannot be nested.
However, a pair may contain a list or a dictionary base type value, which themselves
contain pairs.

### Geolocation

TODO: from 1 to 3: - lattitude (float from -90 to +90) - longitude (float from -180 to
+180) - altitude (float, units in meters, zero is sea level)

### Color

TODO: where only the first three are required and the other four are each additionally
optional (meaning you can have a five member color including Hue and without
Saturation, but if you want Saturation without Hue it will be a six member color and
you will need to set the Hue value to 'not supplied'), these are from 1 to 7: - Red
(integer from 0 to 255) - Green (integer from 0 to 255) - Blue (integer from 0 to 255)
- Alpha (float from 0 to 1, negative value means 'not supplied') - Hue (float from 0 to
1, negative value means 'not supplied') - Saturation (float from 0 to 1, negative value
means 'not supplied') - Luminosity (float from 0 to 1, negative value means 'not
supplied')

### Predicate

TODO: from 1 to 3: - object (any value or storage base type) - verb (tag, may be empty)
- subject (any value or storage base type)

## Collection base types

The set of base types include two collection types: list and dictionary. By their
nature, collection base type memory requirements are not predictable. Moreover, base
type collections can be nested. Lists may contain lists and dictionaries as list
members and dictionaries may contain lists and dictionaries as keyed values. While
there is no design limit to this nesting, in practice deeply nested collections may
fail to work properly or cause exceptions when passed to some APIs or when transferred
to another base type software implementation.

NOTE: from a logical standpoint a dictionary is a list of pairs where the name portion
of the pair is the dictionary key and must be unique. For this reason, a dictionary
entry cannot contain a pair as a value because pairs cannot be directly nested. See
also, structure base types.

Particularity large collections, with or without nesting, may also fail to work
properly or cause exceptions when passed to some APIs. Also, large value types as
collection members, such as very large strings or blobs, may cause problems as well.

In general it is best to avoid large and/or deeply nested collections if possible and
to test carefully if not. As a rule of thumb, collections with less than 1K members or
8 deep nesting are probably fine while collections which exceed those limits may be
problematic.

* list – "tag:bt.co,2019:list" – types.ListType (except all list members must be base
types and types.TupleType is supported by converting to a list)

* dictionary – "tag:bt.co,2019:dictionary" – types.DictType (except dictionary keys
must be strings and values must be base types)

## Packable base type

There is one 'packable' base type, which is simply an object that supports the Packable
interface and can be 'packed' and 'unpacked'.

* packable – "tag:bt.co,2019:packable" – jaxtools.basetypes.Packable
"""

from enum import Enum

from datetime import datetime, date as dt

from abc import ABCMeta, abstractmethod

from jaxtools.python.typehelpers import isNone, isBool, isString, isInt, isFloat, \
    isTuple, isList, isDict, isDateTime, isDate

##
## Tag type.
##

class Tag(object):
    """Tags are objects based on RFC 4151: the 'tag' URI Scheme.

    See also: https://taguri.org/
    """
    def __init__(self, tagUri=None, authority=None, date=None,
                 specific=None, fragment=None):
        # Do we have a tag URI?
        if isString(tagUri):
            # Attempt to parse the tag URI. Start by splitting on colons to get
            # the three main bits.
            colonSplit = tagUri.split(':')
            if len(colonSplit) == 3 and colonSplit[0].lower() == 'tag':
                # Split the tagging entity on commas.
                commaSplit = colonSplit[1].split(',')
                if len(commaSplit) == 2:
                    if authority is None:
                        authority = commaSplit[0]
                    if date is None:
                        # Attempt to convert the date three different ways.
                        try:
                            date = datetime.strptime(commaSplit[1], '%Y-%m-%d').date()
                        except:
                            try:
                                date = datetime.strptime(commaSplit[1], '%Y-%m').date()
                            except:
                                try:
                                    date = datetime.strptime(commaSplit[1], '%Y').date()
                                except:
                                    # Could not convert date.
                                    raise ValueError("tagUri not a valid RFC 4151 Tag URI (date).")
                else:
                    raise ValueError("tagUri not a valid RFC 4151 Tag URI (tagging entity).")
                # Split the rest into the specific name and a (possible) fragment.
                hashSplit = colonSplit[2].split('#')
                if len(hashSplit) > 2:
                    raise ValueError("tagUri not a valid RFC 4151 Tag URI (fragment).")
                if len(hashSplit) >= 1 and specific is None:
                    specific = hashSplit[0]
                if len(hashSplit) == 2 and fragment is None:
                    fragment = hashSplit[1]
            else:
                raise ValueError("tagUri not a valid RFC 4151 Tag URI.")
        elif tagUri is not None:
            raise TypeError("tagUri not a string.")

        # Do we have a date at this point?
        if date is None:
            # Default to current year.
            date = dt(datetime.now().date().year, 1, 1)

        # Double-check each argument type, since they could have been parsed from
        # the tag string or they could have been passed separately.
        # TODO: Consider if we want to check for empty strings on any of these.
        if not isString(authority):
            raise TypeError("Invalid argument type (authority).")
        if not isDate(date):
            raise TypeError("Invalid argument type (date).")
        if not isString(specific):
            raise TypeError("Invalid argument type (specific).")
        if not isString(fragment) and fragment is not None:
            raise TypeError("Invalid argument type (fragment).")

        # If we made it all the way here we are good!
        self.authority = authority
        self.date = date
        self.specific = specific
        self.fragment = fragment

    def __str__(self):
        if self.fragment is None:
            return "tag:{}:{}".format(self.taggingEntityString(), self.specific)

        return "tag:{}:{}#{}".format(self.taggingEntityString(),
                                     self.specific, self.fragment)

    def dateString(self):
        if self.date.day == 1:
            if self.date.month == 1:
                return "{}".format(self.date.year)
            else:
                return "{}-{}".format(self.date.year, self.date.month)

        return "{}-{}-{}".format(self.date.year, self.date.month, self.date.day)

    def taggingEntityString(self):
        return "{},{}".format(self.authority, self.dateString())

##
## Base Type IDs and Tags.
##

class BaseTypeIds(Enum):
    """Enumeration of the base type IDs."""
    NULL = 0
    BOOL = 1
    INT = 4
    FLOAT = 8
    DATETIME = 9
    STRING = 64
    URN = 65
    TAG = 66
    BLOB = 67
    PAIR = 128
    COLOR = 129
    GEOLOCATION = 130
    PREDICATE = 131
    LIST = 256
    DICTIONARY = 257
    PACKABLE = 384
    END = 65535


BaseTypeTags = {
    # TODO: Use a real dsn name instead of 'bt.co', which may be in use.
    BaseTypeIds.NULL: Tag(tagUri="tag:bt.co,2019:null"),
    BaseTypeIds.BOOL: Tag(tagUri="tag:bt.co,2019:bool"),
    BaseTypeIds.INT: Tag(tagUri="tag:bt.co,2019:int"),
    BaseTypeIds.FLOAT: Tag(tagUri="tag:bt.co,2019:float"),
    BaseTypeIds.DATETIME: Tag(tagUri="tag:bt.co,2019:date"),
    BaseTypeIds.STRING: Tag(tagUri="tag:bt.co,2019:string"),
    BaseTypeIds.URN: Tag(tagUri="tag:bt.co,2019:urn"),
    BaseTypeIds.TAG: Tag(tagUri="tag:bt.co,2019:tag"),
    BaseTypeIds.BLOB: Tag(tagUri="tag:bt.co,2019:blob"),
    BaseTypeIds.PAIR: Tag(tagUri="tag:bt.co,2019:pair"),
    BaseTypeIds.COLOR: Tag(tagUri="tag:bt.co,2019:color"),
    BaseTypeIds.GEOLOCATION: Tag(tagUri="tag:bt.co,2019:geolocation"),
    BaseTypeIds.PREDICATE: Tag(tagUri="tag:bt.co,2019:predicate"),
    BaseTypeIds.LIST: Tag(tagUri="tag:bt.co,2019:list"),
    BaseTypeIds.DICTIONARY: Tag(tagUri="tag:bt.co,2019:dictionary"),
    BaseTypeIds.PACKABLE: Tag(tagUri="tag:bt.co,2019:packable"),
    BaseTypeIds.END: Tag(tagUri="tag:bt.co,2019:end")
}


##
## Required Type Helper functions. (There are more type helpers in typehelpers.py.)
##

def isBaseTypePair(val):
    """"""
    if isTuple(val) and len(val) == 2:
        return isString(val[0]) and isBaseType(val[1])

    return False


# TODO: Add color, geolocation, predicate 'is' checks.

def isBaseTypeTag(val):
    """Returns true if the passed value is a tag object, otherwise returns false."""
    return isinstance(val, Tag)

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


def isBaseTypePackable(val):
    """Returns true if the passed value is a packable object, otherwise returns false."""
    return isinstance(val, Packable)


_baseTypeCheckers = {
    BaseTypeIds.NULL: isNone,
    BaseTypeIds.BOOL: isBool,
    BaseTypeIds.INT: isInt,
    BaseTypeIds.FLOAT: isFloat,
    BaseTypeIds.DATETIME: isDateTime,
    BaseTypeIds.STRING: isString,
    #BaseTypeIds.URN: isString, # TODO: Fix
    BaseTypeIds.TAG: isBaseTypeTag,
    #BaseTypeIds.BLOB: isString, # TODO: Fix
    BaseTypeIds.PAIR: isBaseTypePair,
    # TODO: Add color, geolocation, predicate
    BaseTypeIds.LIST: isBaseTypeList,
    BaseTypeIds.DICTIONARY: isBaseTypeDict,
    BaseTypeIds.PACKABLE: isBaseTypePackable
}


def checkBaseType(baseTypeEnum, val):
    """Returns true if the passed value is a valid type for the
    passed Base Types enumeration."""
    try:
        return _baseTypeCheckers[baseTypeEnum](val)
    except:
        pass

    return False


def getBaseTypeId(val):
    """Returns the base type ID of the passed value. Throws a
    TypeError exception if the passed value is not a valid base type."""

    # Test value using every checker until one returns true or
    # no checker returns true.
    for id in _baseTypeCheckers.keys():
        try:
            if _baseTypeCheckers[id](val):
                return id
        except:
            pass

    raise TypeError("Invalid Base Type.")


def isBaseType(val):
    """Returns true if the passed value is a valid base type,
    otherwise returns false."""

    # Test value using every checker until one returns true or
    # no checker returns true.
    for id in _baseTypeCheckers.keys():
        try:
            if _baseTypeCheckers[id](val):
                return True
        except:
            pass

    return False

##
## Packables.
##

# TODO: PackableHeader type.

class Packable(metaclass=ABCMeta):
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

    @abstractmethod
    def getStateId(self):
        """Implementations must return the State ID associated
        with the Packable object's state design and interface."""
        pass

    @abstractmethod
    def pack(self, baseTypeWriter, hints):
        """Implementations must write the current state of the instance to
        the passed property writer, following a state design
        associated with the State ID. To reduce state size, make
        sure to use default values when writing properties. Hints
        may be used to affect how the packing is done or may be
        ignored."""
        pass

    @abstractmethod
    def unpack(self, baseTypeReader, hints):
        """Implementations must set the current state of the instance by
        reading from the passed property reader, following a state design
        associated with the State ID. To reduce state size, make
        sure to set default values before reading properties. Hints
        may be used to affect how the unåpacking is done or may be
        ignored."""
        pass


class PackableFactory(metaclass=ABCMeta):
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

    @abstractmethod
    def makeObject(self, stateId, hints):
        """Creates a clean instance of a packable object for
        the passed state ID, optionally using the hints."""
        pass

    def makePackable(self, baseTypeReader, hints):
        """Creates a restored instance of a packable object
        from the passed packed propertyWriter instance and hints."""
        obj = self.makeObject(baseTypeReader.getStateId(), hints)
        obj.unpack(baseTypeReader, hints)
        return obj


##
## Base Type reader/writer APIs.
##

class BaseTypeReader(metaclass=ABCMeta):
    """An Abstract Base Class for base type reader implementations, where the elements
    are iterated as tuples consisting of the base type ID and the base type value, if
    the element is not a pair, collection or packable type.

    If the element is a pair type the tuple contains the pair base type ID and the pair name,
    the next element iterated after this 'header' is the pair value, but no 'END" marker is
    required, as with collection and packable types. The value is subject to nesting such
    that pair values which are collection or packable types have their own headers and
    'END' markers.

    If the element is a list type the tuple contains only the list base type ID and
    every element iterated after this 'header' is a member of the list, until an 'END'
    base type ID is sent to indicate the end of the list. The value is subject to nesting such
    that list elements which are collection or packable types have their own headers and
    'END' markers.

    If the element is a dictionary type the tuple contains the dictionary base type ID and
    the elements iterated after this 'header' are the member of the dictionary in the form
    of a pair name/value sets, until an 'END' base type ID is sent to indicate the end of the
    dictionary. The value is subject to nesting such that dictionary elements where the values
    are collection or packable types have their own headers and 'END' markers.

    If the element is a packable type the tuple contains the packable base type ID and the packable
    header and every element iterated after this 'header' is a member of the property list of the
    packed object in the form of a pair element, until an 'END' base type ID is sent to indicate
    the end of the packable. The value is subject to nesting such that packable properties where
    the property values are collection or packable types have their own head-ers and 'END' markers.

    TODO: Implementation notes and rules for iterating."""

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass

    def close(self):
        """Closes the reader and releases its resources. Default implementation
        does nothing, override only if required by the use case."""
        pass


class BaseTypeWriter(metaclass=ABCMeta):
    """An Abstract Base Class for base type reader implementations, where collections and
    packable types are written using a start/end syntax. Works as the converse of a BaseTypeReader
    implementation."""

    @abstractmethod
    def writeNullValue(self):
        """Writes a null value."""
        pass

    @abstractmethod
    def writeBoolValue(self, value):
        """Writes a boolean value. The passed value must be a boolean or convertible to a boolean."""
        pass

    @abstractmethod
    def writeIntValue(self, value):
        """Writes a integer value. The passed value must be a integer or convertible to a integer."""
        pass

    @abstractmethod
    def writeFloatValue(self, value):
        """Writes a float value. The passed value must be a float or convertible to a float."""
        pass

    @abstractmethod
    def writeDateValue(self, value):
        """Writes a date value. The passed value must be a datetime or convertible to a datetime."""
        pass

    @abstractmethod
    def writeStringValue(self, value):
        """Writes a string value. The passed value must be a string or convertible to a string."""
        pass

    @abstractmethod
    def writeUrlValue(self, value):
        """Writes a url value. The passed value must be a url or convertible to a url."""
        pass

    @abstractmethod
    def writeTagValue(self, value):
        """Writes a tag value. The passed value must be a tag or convertible to a tag."""
        pass

    @abstractmethod
    def writeBlobValue(self, value):
        """Writes a blob value. The passed value must be a blob or convertible to a blob."""
        pass

    @abstractmethod
    def writePairStart(self, name):
        """Writes the name portion of a pair, after which the next write *must be* the value portion, do
        not call writeEnd() after writing the value, as you would with a collection or packable write."""
        pass

    @abstractmethod
    def writeListStart(self):
        """Signals the start of a list, after which all writes are list members until you call
        writeEnd()."""
        pass

    @abstractmethod
    def writeDictionaryStart(self):
        """Signals the start of a list, after which all writes are dictionary members in the form
        of writePairStart() and pair value writes until you call writeEnd()."""
        pass

    @abstractmethod
    def writePackableStart(self, packableHeader):
        """Signals the start of a packable, after which all writes are object properties in the form
        of writePairStart() and pair value writes until you call writeEnd()."""
        pass

    @abstractmethod
    def writeEnd(self):
        """Indicates the end of a collection or packable write."""
        pass

    def close(self):
        """Closes the writer and releases its resources. Default implementation
        does nothing, override only if required by the use case."""
        pass


class NotInACollectionError(Exception):
    """Error raised when writing a collection member, but a collection has not been 'started'
    in the writer."""
    pass


class InvalidKeyError(Exception):
    """Error raised when writing a dict member with a missing key or starting a pair with
    an invalid key."""
    pass


class InvalidTypeError(Exception):
    """Error raised when writing a value that is not a base type."""
    pass

