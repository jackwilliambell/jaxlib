"""basetypes.py

Copyright (c) 2018, 2019 Jack William Bell. License: MIT

Base types are a set of basic data types that
are easy to serialize and are either a standard 
type of nearly every programming languge or are
easy to implement/emulate if not.

Base types include low-level types like boolean and 
int, along with a set of common data structures and
a type you can use to specify the serialized state of  
more complex objects. See 'packables'.

These types and their Python representations are:

* null - types.NoneType

* bool - types.BooleanType

* int - types.IntType, types.LongType

* float - types.FloatType

* date - datetime.datetime

* string - types.StringType, types.UnicodeType

* url - urllib.request.Request

* blob - types.BufferType

* list - types.ListType (list members must be base 
types, types.TupleType supported by converting to
a list)

* dictionary - types.DictType (dictionary keys must be strings
and values must be base types)

* propertysheet - jaxtools.basetypes.PropertySheet (any dictionary 
using string keys may be converted to a property sheet and vice 
versa)

* packedstate - jaxtools.basetypes.PackedState

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

    def __init__(self, parent=None, properties=None, immutable=False):
        """Initializes a new instance of the PropertySheet class,
optionally with a parent and/or initial properties."""
        self._parent = parent

        self._immutable = immutable

        self.clearSheet()

        if properties:
            self.mergeProperties(properties)

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
        del self._properties[propertyKey]

    def clone(self):
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
    
    def __init__(self, stateId, properties):
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
            
    def toDict(self):
        """Creates a dictionary from the PackedState instance, including 
        converting any contained PackedState or PropertySheet values."""
        raise NotImplementedError("Not yet implemented...")


def isPropertySheet(val):
    """Returns true if the passed value is a 
    property sheet, otherwise returns false."""
    return isinstance(val, PropertySheet)


def isPackedState(val):
    """Returns true if the passed value is a 
    packed state, otherwise returns false."""
    return isinstance(val, PackedState)


def checkBaseType(val, baseType):
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
            # Otherwise, it it a base type at all?.
            elif not isBaseType(v):
                return False
    else:
        return False  # Not a list
    
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
            # Otherwise, it it a base type at all?.
            elif not isBaseType(v):
                return False
    else:
        return False # Not a list
    
    return True

def isBaseType(val):
    """Returns true if the passed value is a valid base type,
    otherwise returns false."""

    # This if statement is structured this way for a reason. Look at
    # the code using it above before changing it, to make sure you
    # don't break anything or simply do something non-optimal.
    if isNone(val) or isBool(val) or isString(val) or isInt(val) or  \
        isNum(val) or isPropertySheet(val) or isPackedState(val):
        return True
    elif (isList(val) or isTuple(val)) and isBaseTypeList(val):
        return True
    elif isDict(val) and isBaseTypeDict(val):
        return True

    return False
