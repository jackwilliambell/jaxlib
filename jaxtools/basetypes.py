"""# Base Types

Base types are a set of basic data types that
are easy to serialize and are either a standard 
type of nearly every programming languge or are
easy to implement/emulate if not.

Base types include low-level value types like boolean and
int along with a storage types like string and blob, a
set of common data structures like list and dictionary,
and a type you can use to specify and contain the
serialized state of more complex objects. See 'packables'.

## List of base types

These types and their Python representations are:

* null - types.NoneType

* bool - types.BooleanType

* int - types.IntType, types.LongType

* float - types.FloatType

* datetime - datetime.datetime

* string - types.StringType, types.UnicodeType

* urn - urllib.request.Request

* blob - types.BufferType

* list - types.ListType (list members must be base types,
types.TupleType supported by converting to a list)

* dictionary - types.DictType (dictionary keys must be strings
and values must be base types)

* propertysheet - jaxtools.basetypes.PropertySheet (any base type
dictionary may be converted to a property sheet and vice
versa)

* packedstate - jaxtools.basetypes.PackedState (may be converted to
a base type dictionary with predefined string keys and vice versa)

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

(NOTE: Python strings on a 64-bit machines may use hundreds of gigabytes
of memory, but that does not mean APIs you pass them to will work properly.)

## Collection base types

The set of base types include four collection types: list, dictionary,
propertysheet, and packstate. Of these, list and dictionary are
'classic' collection types while propertysheet and packstate are
special cases of the base type dictionary and can be converted
to and from base type dictionaries. For the purposes of discussing
collections in base types we will consider propertysheet and
packstate to be dictionaries.

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

Created by Jack William Bell on 2016-10-16.

Copyright (c) 2016, 2018 Jack William Bell. License: MIT"""

from enum import Enum

from jaxtools.typehelpers import isNone, isBool, isString, isInt, \
    isNum, isTuple, isList, isDict


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
    PROPERTYSHEET = 32
    PACKEDSTATE = 33
    UNKNOWN = 255


class PropertySheet(object):
    """A property sheet is a string-keyed map of Base Type
values. Its 'underlying' dictionary is only accessible via the
class methods and not as a Python map. This is intentional.

The class methods allow you to perform various operations 
on the the properties in sheets. But only via mutating the 
property values using merge and get/set/clear semantics,
where your code provides a property key and a default value 
(where applicable).

Conceptually this class provides a 'property bag'. It only
stores non-default property values and returns a default value
if the property does not exist in the bag. It provides 
no way to get a list of the keys or values; if you don't 
know what you want from it or what the default value for
that thing should be, this isn't the right data structure 
for you.    

NOTE: Get operations provide read-only access to a 
parent property sheet when the current instance does not 
contain the specified key. The parent sheet must be 
supplied at instance creation, but may be 'None' if the
sheet has no parent. This allows for upward chaining
of properties if the sheet your are accessing does not
contain a property with that key.

NOTE: Property sheets cannot be iterated nor can you get
a list of the keys. However, the toDict() method returns
a copy of the property sheet in the form of a Python
dictionary, which you can iterate. This is not a 
recommended use case.

TODO: Add schema validation. (JWB)

Property sheet keys are strings. Property sheet values are
restricted to Base Types. See 'Base Types'."""

    def __init__(self, parent=None, properties=None, immutable=False, safeCopy=True):
        """Initializes a new instance of the PropertySheet class,
        optionally with a parent and/or initial properties."""
        self._parent = parent

        self._immutable = immutable

        self.clearSheet()

        if properties:
            self.mergeProperties(properties)

    @staticmethod
    def toDictionary(propertysheet, safeCopy=True):
        """Creates a dictionary from the passed property sheet,
        data is deep-copied."""
        raise NotImplementedError("Not yet implemented...")

    @staticmethod
    def fromDictionary(dictionary, safeCopy=True):
        """Creates a property sheet from the passed dictionary,
        data is deep-copied."""
        raise NotImplementedError("Not yet implemented...")

    def forceImmutable(self):
        """Forces the property sheet to be immutable."""
        self._immutable = True

    def isImmutable(self):
        """Returns true if the property sheet is immutable,
        otherwise returns false."""
        return self._immutable

    def mergeProperties(self, properties):
        """Merges the contents of a dictionary or property sheet
        into the current property sheet.

        NOTE: Only string-keyed base-type values are merged.
        Invalid values are ignored."""
        if self._immutable:
            raise ValueError("Cannot merge properties. Property sheet is immutable.")

        if isDict(properties):
            # TODO: Consider reworking this as a comprehension for
            # better performance. OTOH, this is easy to read. (JWB)
            for k in properties.keys():
                if isString(k) and isBaseType(properties[k]):
                    self._properties[k] = properties[k]
        elif isinstance(properties, PropertySheet):
            self.mergeProperties(properties._properties)
        else:
            raise TypeError("'properties' argument must be a PropertySheet or a dictionary.")

    def clearSheet(self):
        """Clears all properties in the sheet."""
        if self._immutable:
            raise ValueError("Cannot clear sheet. Property sheet is immutable.")

        self._properties = {}

    def getProperty(self, propertyKey, default=None):
        """Returns the value of the property specified by the
        property key. If no property exists for the key or the property
        value is 'None', the default value is returned."""
        val = None
        try:
            val = self._properties[propertyKey]
        except KeyError:
            pass

        if val == None and self._parent != None:
            val = self._parent.getProperty(propertyKey, default)

        return val if (val != None) else default

    def setProperty(self, propertyKey, propertyValue, default=None):
        """Sets the value of the property specified by the
        property key. If the property value is the same as
        the default value, the property is cleared instead. Raises
        a ValueError exception if the property sheet is immutable.
        Raises a KeyError exception if the key is not a string."""
        if self._immutable:
            raise ValueError("Cannot set property. Property sheet is immutable.")

        if not isString(propertyKey):
            raise KeyError("Key must be a string.")

        # TODO: Make sure the equality operator does a
        # deep test for complex types. (JWB)
        if (propertyValue == default):
            self.clearProperty(propertyKey)
        else:
            val = None
            try:
                val = self._properties[propertyKey]
            except KeyError:
                pass

            # TODO: Make sure the equality operator does a
            # deep test for complex types. (JWB)
            if val != propertyValue:
                # TODO: Check value type. (JWB)
                self._properties[propertyKey] = propertyValue

    def clearProperty(self, propertyKey):
        """Removes the key from the property sheet."""
        if self._immutable:
            raise ValueError("Cannot clear property. Property sheet is immutable.")

        del self._properties[propertyKey]

    def clone(self, safeCopy=True):
        """Returns a new PropertySheet instance containing the
        same properties and parent as the current instance. All contained
        complex objects are deep-copied and contained property sheets are
        recursively cloned. Changes made to the new instance will not be
        reflected in the current instance and vice-versa. Using this method
        on deeply nested property sheets is not recommended."""
        raise NotImplementedError("Not yet implemented...")


class PackedState(object):
    """Represents the state of a Packable object. Can be 'unpacked'
    to a new object using any class that supports the same state
    format design. How it is unpacked is implementation dependent.
    See Packables for more details.

    **Description:**

    Provides two public attributes:

    * stateId - A string value uniquely specifying the state design
    and interface of the packed object; should be a URL linking the
    class and state specification, but can be any string (if not a
    URL it is recommended you use Java-style namespaced class names)

    * properties - A property sheet or Dictionary containing the
    packed object's state

    NOTE: These attributes are read only. Attempting to set them
    will raise an exception.

    NOTE: The state may be immutable or mutable. If it is mutable it
    can be modified by setting or clearing properties. Generally this
    is a really bad idea. Don't do it."""

    def __init__(self, stateId, properties, safeCopy=True):
        """Sets up the new PackedState instance with the passed
        State ID and State Property Sheet."""
        # Verify types.
        if not isString(stateId):
            raise TypeError("The stateId argument must be a String or Unicode instance")
        if not isPropertySheet(properties):
            raise TypeError("The state argument must be a PropertySheet instance")

        # We are good.
        self.stateId = stateId
        self.properties = properties

    def __setattr__(self, name, value):
        if name in ("stateId", "properties"):
            raise AttributeError("Cannot set immutable attribute %s.")
        else:
            super().__setattr__(name, value)

    @staticmethod
    def toDictionary(packedstate, safeCopy=True):
        """Creates a dictionary from the passed packed state,
        data is deep-copied."""
        raise NotImplementedError("Not yet implemented...")

    @staticmethod
    def fromDictionary(dictionary, safeCopy=True):
        """Creates a packed state from the passed dictionary,
        data is deep-copied."""
        raise NotImplementedError("Not yet implemented...")


def isPropertySheet(val):
    """Returns true if the passed value is a
    property sheet, otherwise returns false."""
    return isinstance(val, PropertySheet)


def isPackedState(val):
    """Returns true if the passed value is a
    packed state, otherwise returns false."""
    return isinstance(val, PackedState)


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


def isBaseType(val):
    """Returns true if the passed value is a valid base type,
    otherwise returns false."""

    # This if statement is structured this way for a reason. Look at
    # the code using it above before changing it, to make sure you
    # don't break anything or simply do something non-optimal.
    if isNone(val) or isBool(val) or isString(val) or isInt(val) or  \
        isNum(val) or isPropertySheet(val) or isPackedState(val):
        # TODO: Add date, url, and blob checks
        return True
    elif (isList(val) or isTuple(val)) and isBaseTypeList(val):
        return True
    elif isDict(val) and isBaseTypeDict(val):
        return True

    return False

# TODO: Consider adding callback function params to the following conversion
#  functions for converting datetime and urn. Maybe for all type?

# TODO: Consider if this should use a callback strategy instead; as currently
#   designed it will consume a lot of memory and CPU for deeply nested collection
#   types. Using a callback converter as part of serialization lets you reduce
#   the overhead to performing them one at a time. Think this through carefully.

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