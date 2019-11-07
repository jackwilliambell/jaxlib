"""Provides simple object serialization to and from packed
state instances. (See Packedstate class in Base Types.) 
Serialized  objects may be de-serialized into the same class 
as they were serialized from or into a different class, if that
class supports the same state format. Using Packables requires 
implementing an abstract class and creating object factories.

**Description:**

Basically 'Packing' and 'Unpacking' are yet another way to  
save the state of a Python object and reconstitute it later.
This can never be as fast as Pickle (or most of the other 
solutions for that matter), but it can be safer than many 
(certainly safer than Pickle) because it requires the use 
of a 'Factory' object to create new instances and that 
factory can create your own implementations of the class 
which does not execute the same code as the originally 
packed object, but does support the same state properties. 
(AKA: the 'state format'.)

On the other hand, you are completely responsible for 
creating a factory that supports your packable class and
managing any potential problems created by different 
versions of that class. You also must explicitly pack
any contained packable objects and provide an appropriate
factory when unpacking them.

Packing is simply a process of adding properties 
representing your object's state to a passed property 
sheet. Unpacking is simply a process of loading
your object's state from a passed state property sheet.
From the perspective of a packable object that's all
there is to it. 

There are functions supporting packing and unpacking 
of types along with helper functions that let you directly 
pack or unpack packable objects to/from streams. Unlike
most state-management APIs Packables doesn't 
open or create those streams; you will need to write
your own code to manage files and other streams.

In general Packables is – and will stay – a very
simple-minded searialization API that puts all the
onus to make it work properly on the software developer.
If you aren't ready to deal with that, choose another
solution. On the other hand, the very simplicity of the
API allows you to use it in situations and in ways where
it might be difficult or impossible to adapt a more
powerful solution.

Another limitation of packables is that the state cannot
contain any values that aren't 'packable types'. Packable 
types include:

* Base Types supported by property sheets. (see Base Types)

* Any class implementing 'Packable', after packing it
to or unpacking it from a property sheet (see packIt() and
unpackIt() helper functions)

* Any other Python class you can convert to and from a 
type supported by property sheets.

It is highly recommended you go by the following rules when 
implementing packable classes:

* Your packable class must only require packable types for
its state or the factory class supporting it must support
creating and passing in non-packable types from hints

* Your packable class must always support unpacking from the 
constructor by providing a constructor argument for the 
state properties and, if supported, a constructor argument
for the hints

* In most cases you should provide a state property to indicate
the state format version, in case your state design changes, 
then check that version value when unpacking; either providing 
extra code to unpack older versions or raising an exception 
if the version isn't supported

* You must implement a factory for your packable class and, 
if your class might be dangerous when used with state data from
unknown sources, provide a second packable class and factory
with more limited functionality (alternatively, document 
everything thoroughly so others can create their own safe 
versions)

* Alternatively or in addition to the above, your packable 
class can support hints that limit or expand functionality 
when unpacking

Created by Jack William Bell on 2016-10-16.
Copyright (c) 2016, 2018 Jack William Bell. License: MIT"""

from jaxtools.basetypeids import PropertySheet, PackedState, \
    isPackableType, isPropertySheet
from jaxtools.typehelpers import isNone, isBool, isString, isInt, \
    isNum, isTuple, isList, isDict
from jaxtools.serialization import DictionaryWriter, DictionaryReader




##
## Packable Helper functions.
##
## TODO: Either get rid of these or refactor them for the new design.
##

def packIt(packable, hints, overrideStateId=None):
    """Helper function that packs a packable object using the
    passed class ID and hints. Returns a packed state containing the
    object state.

    **Parameters:**

    * packable - packable object to pack

    * hints - Dictionary of hint values giving extra information to the
    packable object to use when packing

    * overrideStateId - Optional state ID to use instead of the one
    provided by the packable object

    **Returns:**

    A packed state instance representing the current state of the packable
    object."""
    stateId = overrideStateId if overrideStateId else packable.getStateId()
    assert (isString(stateId)), "State Id must be a string."
    props = PropertySheet(immutable=False)
    packable.pack(props, hints)
    props.forceImmutable()
    return PackedState(stateId, props)


def unpackIt(factory, state, hints, overrideStateId=None):
    """Helper function that unpacks a packable object using
    the passed factory, packed state and hints. Returns the unpacked
    object.

    **Parameters:**

    * factory - PackableFactory implementation to make the new object

    * state - PackedState containing the object's state

    * hints - Dictionary of hint values giving extra information to the
    factory or packable object to use when unpacking

    * overrideStateId - Optional state ID to use instead of the one in
    the state.

    **Returns:**

    The unpacked object instance or None if the factory doesn't support
    the State ID."""
    assert (isPackableType(state)), "State must be a PackedState instance."
    stateId = overrideStateId if overrideStateId else state.stateId()
    assert (isString(stateId)), "State Id must be a string."
    factory.makePackable(stateId, state.properties, hints)


def serializeState(dictionaryWriter, state, hints, overrideStateId=None):
    """"""
    raise NotImplementedError("Abstract method, must be implemented if subclass supports it.")


def deserializeState(dictionaryReader, hints, overrideStateId=None):
    """"""
    raise NotImplementedError("Abstract method, must be implemented if subclass supports it.")

