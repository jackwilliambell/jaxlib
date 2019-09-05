"""Applies the basic idea of map/reduce to a hierarchical 
tree structure consisting of directories and files. This
can be, but is not limited to, a computer file system. 
Other storage systems may be created with custom 
implementations of the WalkerContext class. 

The following WalkerContext implemetations are provided:

* OsWalkerContext - Computer file system walkers. [not implemented]

* DictWalkerContext - Dictionary walker that treats contained
dictionaries as 'directories' and everything else as a 
'file-like object'. [not implemented]

Originally created by Jack William Bell on 2015-12-08.

Copyright (c) 2015, 2018 Jack William Bell. All rights reserved."""

import sys
import os
from properties import PropertySheet

class WalkerContext(PropertySheet):
	"""An Abstract Base Class for walking through a  
hierarchical dataset (for example, a file system 
directory) using the Visitor pattern, while allowing
CRUD (Create Read Update Delete) actions to the 
directory contents as the Visitor processes each 
directory.

**Public Instance Attributes:**

* parent - The WalkerContext instance of the parent directory. 
[read only]

* dirpath - The subdirectory path of the context. [read only]

* dirnames - A list of the subdirectory names of the context.
If this list is changed during walk() processing, the changed 
list is used for processing the context subdirectories.

* filenames - A list of the file names of the context.

**Description:**


Each WalkerContext instance represents a single 
directory, providing access to directory, subdirectories,
and file metadata and contents. The walk() method 
starts from the current directory and 'walks' 
downwards through the subdirectories calling 
the passed WalkerVisitor instance for each one.

As each directory is passed to the WalkerVisitor
instance a new WalkerContext is created for it with
the parent directories WalkerContext linked and 
available via the getParent() method."""

	def __init__(self, parent, dirpath, dirnames, filenames,
				propertyOverrides=None):
		"""Creates a new instance of the WalkerContext
class using the passed parameters.

**Parameters:**

* parent - The parent context to use. [not required]

* dirpath - A subdirectory path to use as the root 
directory of the new context, if not provided the 
current context root is used. [not required]

* dirnames - [not required]

* filenames - [not required]

* propertyOverrides - A PropertySheet instance  
specifying custom properties to to be used for the  
new context. [not required]

**Returns:**

A new instance of the WalkerContext class."""
		super(PropertySheet, self).__init__(parent)
		
		self.parent = parent
		self.dirpath = dirpath
		self.dirnames = dirnames
		self.filenames = filenames
		
		self.mergeProperties(propertyOverrides)
	
	def open(self, filename, mode):
		"""Abstract method that opens a file in the current 
context with the passed name. Raises an exception 
if the file does not exist.

**Parameters:**

* filename - The name of the file to open. Must be a
valid file for the current diretory context.

* mode - Same as the 'mode' parameter of the Python
open() function. [not required, defaults to 'r']

**Returns:**

A 'File-Like Object'. This may be an actual operating 
system file or it may be some other object implementing
basic Python file operations.

**Description:**"""
		raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")
	
	def createChild(self, dirpath, dirnames, filenames,
					propertyOverrides=None):
		"""Creates a new WalkerContext instance of the same type 
as the current context, using the current context as 
the parent. May be overridden to return a different 
context type, but this is not recommended. (See 
makeWalkContext().)

**Parameters:**

* dirpath - A subdirectory path to use as the root 
directory of the new context, if not provided the 
current context root is used. [not required]

* dirnames - [not required]

* filenames - [not required]

* propertyOverrides - A PropertySheet instance  
specifying custom properties to to be used for the  
new context. [not required]

**Returns:**

A new WalkerContext object instance."""
		return self.__class__(self, dirpath, dirnames, filenames,
					propertyOverrides=propertyOverrides)
		
	def makeWalkContext(self, dirpath, dirnames, filenames):
		"""Called each time a new directory is processed during a walk, 
before the walker visitor is invoked on that directory. Returns
the walker context to be passed to the visitor. The default 
implementation returns simply calls the createChild() with no
property overrides, but makeWalkContext() may be overridden
to return any valid walker context.

**Parameters:**

* dirpath - A subdirectory path to use as the root 
directory of the new context, if not provided the 
current context root is used.

* dirnames

* filenames

**Returns:**

A new WalkerContext object instance.

**Description:**

The default implementation simply calls the createChild() with no
property overrides. However, you can overrides this method to 
return any valid walker context. A common override use case is 
to do the same thing, but pass property overrides appropriate
to the new context and the use case. 

If your use case modifies the new context based upon its contents 
the best way is to create that new context first and then use it to 
access its own contents; changing properties or other context 
state before returning the modified context.

Another use case is to return a completely different subclass of
WalkerContext based on the subdirectory or its contents. This can
be a two step process where you first create a normal child 
context and then use it to access subdirectory contents in
order to determine the new context type.

NOTE: Although the walk() method should call this method, it may 
be called outside of walk processing."""
		return self.createChild(dirpath, dirnames, filenames)
	
	def walk(self, walkerVisitor, dirPath=None, properties=None):
		"""Abstract method that performs the actual 
directory walking. Must be implemented for 
each context type. For an example of how to 
implement, see the OsWalkerContext and 
DictWalkerContext classes.

**Parameters:**

* walkerVisitor - A WalkerVisitor implementation
to use for each subdirectory, including the root.
[required]

* dirPath - A subdirectory path to start walking 
from, if not provided the root directory of the 
context is used. [not required]

* properties - A PropertySheet instance specifying 
custom properties to to be merged into the current
properties for the walk. [not required]

**Returns:**

Nothing.

**Description:**

The walk() method creates a child WalkerContext 
instance (see the createChild() method) using the
passed directory path or the root of the current 
WalkerContext. It then passes that child context
to the passed WalkerVisitor. Afterwards it 
iterates through any subdirectories and their 
subdirectories in a manner similar to the Python
os.walk() function.

Each time a subdirectory is processed during the walk, 
the visit() method of the Visitor is called with a new 
child context object specific to that directory. 

Since the Visitor can mutate context properties and
contents, this means subdirectory processing is done
with those changes in place. 
 	
The Visitor can process the files in any order and 
can use the properties to control how a directory 
context is processed. These properties may be 
built in stages and the each subdirectory's custom
property values may be used to control processing of
its subdirectories. (For example, the Visitor might 
first process all the files known to contain only 
metadata of some kind, using those to mutate properties
and change which subdirectories will be processed. Then 
the Visitor might process all the remaining files.)

Properties of the parent context remain available when
subdirectories are processed and can be 

A default meta can be supplied at object creation, 
acting as the root parent meta for each walk() call."""
		raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")
		
		
class WalkerVisitor(object):
	"""An Abstract Base Class for processing 
the contents of a single directory. Used by the 
walk() function of the WalkerContext class to 
process a directory tree by invokiing the Visitor 
for each directory and subdirectory.

Provides a single method, visit(), which
is expected to process the contents of the
current directory described by the passed directory
context"""
	def __init__(self):
		pass
		
	def visit(self, directoryContext):
		"""Processes the passed directory context. How that 
directory is processed is implementation dependent. 

**Parameters:**

* directoryContext - A WalkerContext instance of the
current directory, used to process that directory. [required]

**Returns:**

Nothing.

**Description:**

Implementations will process the contents of the directory
described by the passed directory context. If an error
occurs or you wish to stop walk processing for any 
reason you must throw an exception.

The implementation may change the context properties.
If it does, those changes are reflected in the 
properties available to the subdirectory contexts
when they are processed during the walk. However 
changed properties are not passed back up to 
parent contexts.

The implementation may change the subdirectory 
contents using the context methods. If it does, 
those changes occur before subdirectories are 
processed.

The context subdirectories list (dirnames) may be 
modified by deleting any subdirectories you do not 
wish to process when the walk continues. If you do 
not want to process any subdirectories at all, simply 
delete all of them. This does not affect the actual
subdirectories, although those may also be removed
using context methods before the walk does 
subdirectory processing."""
		raise NotImplementedError("Abstract method, must be implemented if subclass supports it..")



