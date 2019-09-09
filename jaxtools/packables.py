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

from jaxtools.basetypes import PropertySheet, PackedState, \
	isPackedState, isPropertySheet
from jaxtools.typehelpers import isNone, isBool, isString, isInt, \
    isNum, isTuple, isList, isDict

class Packable(object):
	"""An Abstract Base Class that supports 'packing'
	the state of an object into a PropertySheet instance.
	It is expected that any class implementing Packable
	will also provide a constructor argument for 'unpacking'
	that state back into the object instance when it is
	created; putting the object into the same state as it was
	when the pack occurred.

	**Description:**

	The process of 'packing' is simply setting any state
	values as named properties in a property sheet following
	a known 'state design' that can later be unpacked by
	any class implementing the same state design. Each state
	design is associated with a particular State ID and
	state designs may be versioned within a State ID.

	Different classes may support the same State ID, so long
	as they also support the same state design and interface;
	meaning they are interchangable and runtime Polymorphic. For
	classes that might be dangerous if unpacked using states from
	unknown sources it is generally a good idea to provide a
	safe version of the Packable object to use. See PackableFactory
	class."""

	def getStateId(self):
		"""Implementations must return the State ID associated
		with the Packable object's state design and interface."""
		raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")

	def pack(self, properties, hints):
		"""Implementations must load the passed property sheet with
		the current state of the instance, following a state design
		associated with the State ID. To reduce state size, make
		sure to use default values when setting properties. Hints
		may be used to affect how the packing is done or may be
		ignored."""
		raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")

	def unpack(self, properties, hints):
		"""Implementations must set the current state of the instance
		from the passed property sheet, following a state design
		associated with the State ID. To reduce state size, make
		sure to use default values when getting properties. Hints
		may be used to affect how the unåpacking is done or may be
		ignored."""
		raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")


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

	def makePackable(self, stateId, properties, hints):
		"""Creates a restored instance of a packable object
		from the passed packed state and hints."""
		obj = self.makeObject(stateId, hints)
		obj.unpack(properties, hints)
		return obj


class DictionaryWriter(object):
	"""An abstract Base Class that supports creating writing the contents of
	a dictionary out to some external destination. The destination can be a
	string, a buffer, a file, a network connection; anything you can serialize
	the property sheet to.

	The implementations determine (a) how the data is converted to
	serializable form and (b) how the data is written."""

	def writeProperties(self, dict):
		"""Writes the passed property sheet out as implemented."""
		raise NotImplementedError("Abstract method, must be implemented if subclass supports it.")


class DictionaryReader(object):
	"""An abstract Base Class that supports reading and recreating a
	dictionary from an external source. The source can be a string,
	a buffer, a file, a network connection; anything you can deserialize a
	dictionary from.

	The implementations determine (a) how the data is converted from
	serializable form and (b) how the data is read."""

	def readProperties(self):
		"""Reads and returns a property sheet, as implemented."""
		raise NotImplementedError("Abstract method, must be implemented if subclass supports it.")


##
## Packable Helper functions.
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
	assert (isPackedState(state)), "State must be a PackedState instance."
	stateId = overrideStateId if overrideStateId else state.stateId()
	assert (isString(stateId)), "State Id must be a string."
	factory.makePackable(stateId, state.properties, hints)


def serializeIt(writer, factory, state, hints, overrideStateId=None):
	""""""

def deserializeIt(reader, factory, state, hints, overrideStateId=None):
	""""""
