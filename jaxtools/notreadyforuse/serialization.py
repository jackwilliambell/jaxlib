"""basetypes.py

TODO: Refactor completely or remove entirely!

Copyright (c) 2015, 2019 Jack William Bell. License: MIT

Provides DictionaryWriter and DictionaryReader base classes for
common serialization and deserialization of python dicts, where the
dicts qualify as Base Type dictionaries. This means the dictionary
keys must be strings the and values must also be base types.

Implementations of these classes need to write the contents
of a dictionary out to a sink or read the contents of a dictionary in
from a source. How the data is serialized when written or read is up to
the implementation, as is the source and the sink.

For example, an implementation of DictionaryWriter might use the Python
JSON module to convert the data to a string and then write the string
out to a file, with a matching implementation of DictionaryReader that
reverses this process.

Conversely, implementations of DictionaryWriter and DictionaryReader may
store the data in a database, send the data over a network, or do anything
else matching the pattern. Implementations are also free to:

1. Interpret the hints any way they like (for example, a file name to write
to/read from)

2. Filter/change the data (for example, not serialize a known value or add
a timestamp)

3. Throw an exception based on the data contents.

Also provided are the following DictionaryWriter and DictionaryReader
implementations:

* EvalStringWriter/Reader - serialize to/from a string using
ast.literal_eval()/str(); has the same limitations as ast.literal_eval()

* EvalFileDictWriter/Reader – serialize to/from a file using
ast.literal_eval()/str(); has the same limitations as ast.literal_eval()

"""

from ast import literal_eval
from jaxtools.basetypes import isBaseTypeDict

##
## Base Classes
##

class DictionaryWriter(object):
    """An abstract Base Class that supports creating writing the contents of
    a base type dictionary out to some external destination. The destination can be a
    string, a buffer, a file, a network connection; anything you can serialize
    the property sheet to.

    The implementations determine (a) how the data is converted to
    serializable form and (b) how and where the data is written."""

    def writeProperties(self, dict, hints):
        """Writes the passed property sheet out as implemented."""
        assert (isBaseTypeDict(dict)), "'dict' must be a Base Type Dictionary."
        raise NotImplementedError("Abstract method, must be implemented if subclass supports it.")


class DictionaryReader(object):
    """An abstract Base Class that supports reading and recreating a
    base type dictionary from an external source. The source can be a string,
    a buffer, a file, a network connection; anything you can deserialize a
    dictionary from.

    The implementations determine (a) how the data is converted from
    serializable form and (b) how and from where the data is read."""

    def readProperties(self, hints):
        """Reads and returns a property sheet, as implemented."""
        raise NotImplementedError("Abstract method, must be implemented if subclass supports it.")
