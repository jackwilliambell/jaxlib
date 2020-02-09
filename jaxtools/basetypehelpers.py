"""

"""

from jaxtools.basetypes import *

##
## Type Helper functions.
##

def isValueTypeId(id):
    """"""
    return id in (BaseTypeIds.NULL, BaseTypeIds.BOOL, BaseTypeIds.INT, BaseTypeIds.FLOAT)


def isStorageTypeId(id):
    """"""
    return id in (BaseTypeIds.DATE, BaseTypeIds.STRING, BaseTypeIds.URL, BaseTypeIds.TAG,
                  BaseTypeIds.BLOB)


def isStructureTypeId(id):
    """"""
    return id in (BaseTypeIds.PAIR) # TODO: Add color, geolocation, predicate


def isCollectionTypeId(id):
    """"""
    return id in (BaseTypeIds.DICTIONARY, BaseTypeIds.LIST)


def isPackableTypeId(id):
    """"""
    return id == BaseTypeIds.PACKABLE


def isEndTypeId(id):
    """"""
    return id == BaseTypeIds.END

