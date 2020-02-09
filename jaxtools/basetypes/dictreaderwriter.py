"""

"""

from basetypes.readerwriterhelpers import *


class DictReader(BaseTypeReader):
    """TODO"""

    def __init__(self, dict=None):
        """"""
        pass


class DictWriter(BaseTypeWriter):
    """BaseTypeWriter implementation that writes to a Python dictionary, including packing packables."""

    def __init__(self, dict=None):
        """Initializes the DictWriter. You can pass an optional dictionary to use, otherwise
        one is created."""
        # Did we get a dict to use?
        if not isDict(dict):
            dict = {}

        # Set up the initial state.
        self._dict = dict
        self._collectionStack = []
        self._list = None
        self._dict = None
        self._keyName = None
        self._closed = False

    def getDict(self):
        """Returns the underlying dictionary being written to."""
        return self._dict

    def _writeValue(self, value):
        if self._closed:
            raise ValueError("Writer is closed.")

        if self._keyName and self._list: # Are we in a list and have a key?
            # Add a pair to the current list.
            self._list.append((self._keyName, value))
            # Clear the current key for the next write.
            self._keyName = None
        elif self._list:  # Are we in a list, but no key?
            # Add value to the current list.
            self._list.append(value)
        elif self._keyName and self._dict: # Are we in a dict and have a key?
            # Add value to the current dict using the current key.
            self._dict.add(self._keyName, value)
            # Clear the current key for the next write.
            self._keyName = None
        elif self._dict:
            # Dicts require a key.
            raise InvalidKeyError
        else:
            # Can't write if we aren't in a collection.
            raise NotInACollectionError

    def writeNullValue(self):
        """Writes a null value."""
        self._writeValue(None)

    def writeBoolValue(self, value):
        """Writes a boolean value. The passed value must be a boolean or convertible to a boolean."""
        if isBool(value):
            if value:
                self._writeValue(True)
            else:
                self._writeValue(False)
        else:
            raise InvalidTypeError

    def writeIntValue(self, value):
        """Writes a integer value. The passed value must be a integer or convertible to a integer."""
        if isInt(value):
            self._writeValue(value)
        else:
            raise InvalidTypeError

    def writeFloatValue(self, value):
        """Writes a float value. The passed value must be a float or convertible to a float."""
        raise NotImplementedError("Not yet inplemented. Need type check.")

    def writeDateValue(self, value):
        """Writes a date value. The passed value must be a datetime or convertible to a datetime."""
        raise NotImplementedError("TODO. Need type check.")

    def writeStringValue(self, value):
        """Writes a string value. The passed value must be a string or convertible to a string."""
        if isString(value):
            self._writeValue(value)
        else:
            raise InvalidTypeError

    def writeUrlValue(self, value):
        """Writes a url value. The passed value must be a url or convertible to a url."""
        raise NotImplementedError("TODO. Need type check.")

    def writeTagValue(self, value):
        """Writes a tag value. The passed value must be a tag or convertible to a tag."""
        raise NotImplementedError("TODO. Need type check.")

    def writeBlobValue(self, value):
        """Writes a blob value. The passed value must be a blob or convertible to a blob."""
        raise NotImplementedError("TODO. Need type check.")

    def writePairStart(self, name):
        """Writes the name portion of a pair, after which the next write *must be* the value portion, do
        not call writeEnd() after writing the value, as you would with a collection or packable write."""
        if self._keyName:
            raise InvalidKeyError("Pair already started. Pairs cannot be nested.")

        # Set the current key.
        self._keyName = name

    def writeListStart(self):
        """Signals the start of a list, after which all writes are list members until you call
        writeEnd()."""
        pass

    def writeDictionaryStart(self):
        """Signals the start of a list, after which all writes are dictionary members in the form
        of writePairStart() and pair value writes until you call writeEnd()."""
        pass

    def writePackableStart(self, packableHeader):
        """Signals the start of a packable, after which all writes are object properties in the form
        of writePairStart() and pair value writes until you call writeEnd()."""
        pass

    def writeEnd(self):
        """Indicates the end of a collection or packable write."""
        pass

    def close(self):
        """Closes the writer and releases its resources."""
        self._closed = True


# TODO: Subclass of DictWriter named 'TypeEncoderDictWriter' that encodes type information in the
#  data set using tuples of (typeTag, value) instead of the raw value.