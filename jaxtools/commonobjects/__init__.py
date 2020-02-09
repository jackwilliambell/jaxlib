"""
TODO: Docs

"""

# TODO: Add the following common objects: Table, FormattedText, Document,
#       NumberRange, DateRange, Calendar, Timeline, others?

class PropertyMeta(object):
    """Provides Metadata"""
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


# TODO: Refactor to inherit from Packable.
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
    contain a property with that key. By the same token, if
    the sheet has a property with the same key as a property
    in the parent, the sheet's property value overrides the
    parent's property value.

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
            #   better performance. OTOH, this is easy to read. (JWB)
            for k in properties.keys():
                # TODO: THis copies, not clones. Probably should clone storage and
                #  collection types for safety. Might be good to have a re-usable
                #  library function for that. Also note: some types (strings) are
                #  immutable and others (property bags) can be immutable, so there's
                #  no safety reason to clone them and there is the extra cost. Think
                #  on this.
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
        #  deep test for complex types. (JWB)
        if (propertyValue == default):
            self.clearProperty(propertyKey)
        else:
            val = None
            try:
                val = self._properties[propertyKey]
            except KeyError:
                pass

            # TODO: Make sure the equality operator does a
            #  deep test for complex types. (JWB)
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

# TODO: Either refactor for new design or remove entirely.
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