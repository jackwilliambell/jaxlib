"""

"""

from jaxtools.basetypes import *


##
## Base Type Reader helpers
##

class ChildReader(BaseTypeReader):
    """Simple implementation of BaseTypeReader that iterates a single object
    from a parent reader passed in the constructor. Also passed in the constructor
    is the first base type element to iterate, after which it iterates the parent reader.
    The first element is required and must be a valid element. If the first element
    is not a collection, packable, or pair then it only iterates the first element
    and never iterates from the parent reader."""
    def __init__(self, parentReader, firstElem):
        self._parentReader = parentReader
        # TODO: Error if firstElem is not a valid element.
        self._first = firstElem
        # TODO: If firstElem is not a collection, packable or pair, set depth to 0.
        self._depth = 1

    def __next__(self):
        if self._depth < 1 and not self._first == None:
            # TODO: Raise exception for EOF
            pass

        elem = None
        if not self._first == None:
            elem = self._parentReader.next()
        else:
            elem = self._first
            self._first = None

        if elem[0] == BaseTypeIds.END:
            # Decrement depth.
            self._depth = self._depth - 1

        # TODO: Increment depth for collections and packables. Consider
        #   how to handle pairs.

        return elem


class GenericReader(BaseTypeReader):
    """Simple implementation of BaseTypeReader that uses a generic iterator passed to
    the instance in the constructor. Assumes the passed in iterator follows the rules
    for a BaseTypeReader."""

    def __init__(self, iterator):
        self._iterator = iterator

    def __next__(self):
        return self._iterator.next()


class ReaderCallback(metaclass=ABCMeta):
    """An Abstract Base Class for base type reader SAX-style callbacks implementations, as used by
    the readWithCallbacks() function."""
    @abstractmethod
    def onValue(self, baseTypeId, value):
        """Called when a value is returned by the reader. Returns true to continue reading,
        otherwise returns false. May raise an exception."""
        return False

    @abstractmethod
    def onPairStart(self, name):
        """Called when a pair is started by the reader. Returns true to continue reading,
        otherwise returns false. May raise an exception."""
        return False

    @abstractmethod
    def onListStart(self):
        """Called when a list is started by the reader. Returns true to continue reading,
        otherwise returns false. May raise an exception."""
        return False

    @abstractmethod
    def onDictionaryStart(self):
        """Called when a dictionary is started by the reader. Returns true to continue reading,
        otherwise returns false. May raise an exception."""
        return False

    @abstractmethod
    def onPackableStart(self, packableHeader):
        """Called when a packable is started by the reader. Returns true to continue reading,
        otherwise returns false. May raise an exception."""
        return False

    @abstractmethod
    def onEnd(self):
        """Indicates the end of a collection or packable read. Returns true to continue reading,
        otherwise returns false. May raise an exception."""
        return False


def readWithCallbacks(reader, readerCallback):
    """Helper function for reading using SAX-style callbacks with a BaseTypeReader instance.
    Returns true on success, otherwise returns false. All callback functions must return either
    true or false and, if false is returned, this function will return fase and reading will stop."""
    for elem in reader:
        if elem[0] == BaseTypeIds.END:
            if not readerCallback.onEnd():
                return False
        elif elem[0] == BaseTypeIds.PAIR:
            if not readerCallback.onPairStart(elem[1]):
                return False
        elif elem[0] == BaseTypeIds.LIST:
            if not readerCallback.onListStart():
                return False
        elif elem[0] == BaseTypeIds.DICTIONARY:
            if not readerCallback.onDictionaryStart():
                return False
        elif elem[0] == BaseTypeIds.PACKABLE:
            if not readerCallback.onPackableStart(elem[1]):
                return False
        else:
            # Assume a value if we got here.
            if not readerCallback.onValue(elem[0], elem[1]):
                return False

    return True


def readObject(reader, packableFactory=None):
    """Helper function for reading a collection or packable object from a BaseTypeReader instance.
    If the reader contents contain packables, you will need to provide a compatible packable
    factory instance.

    Reads one object at a time. If the reader contains more data after the end marker for the
    object you will need to read again."""
    raise NotImplementedError("TODO.") # NOTE: Implement using a ReaderCallback instance. (See above.)


##
## Base Type Writer helpers
##

def writeObject(writer, obj):
    """Helper function for writing a collection or packable object to a BaseTypeWriter instance.

    Writes one object at a time. If you want to write another object to the same writer you will
    need to write again."""
    raise NotImplementedError("TODO.")