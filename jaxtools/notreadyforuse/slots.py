"""slots.py

Copyright (c) 2016, 2018 Jack William Bell. License: MIT

Slots are a way of organizing objects dynamically, essentially by 'plugging
them in' to named slots and making them available by that name. Some slot 
names may be reserved, meaning they cannot be overridden. 

If the current instance does not contain a requested named slot, but does 
have a parent Slots instance, the request is deferred to the parent. This 
supports overriding slots locally if they are not reserved, while using the 
parent instance if they are reserved.
"""


class Slots(object):
	"""Holds a set of named Pluggables which are 'plugged into' slots. Some slot 
names are reserved and cannot be overridden.

TODO: Add functionality to support getting a list of slot names, which will
require merging parent and parent/parent slot names with current slot names. (JWB)

TODO: Add ability to test if a slot name is reserved. (JWB)
"""
	def __init__(self, parent=None, pluggables={}, reservedSlots=[]):
		""" 

TODO: Modify to allow a previously created Slots instance or a dictionary for the
pluggables argument. Currently only dictionary. (JWB)"""
		
		# Verify arguments.
		if parent and not isSlots(parent):
			# TODO: Throw exception. (JWB)
			pass
		self._parent = parent
		
		## TODO: Check pluggables, support either dict or other slots. (JWB)

		#TODO: Verify no pluggable slot names are in the reservedSlots list.
		# See put method or else determine this is desired behavior. (JWB)
		self._pluggables = pluggables
		self._reservedSlots = reservedSlots
					
	def get(self, slotName, default=None):
		""" Return the pluggable object bound to the slot or the passed default object. """
		result = None
		try:
			result = self._pluggables[slotName]
		except:
			if self._parent != None:
				result = self._parent.get(slotName)
		return result
		
	def bind (self, slotName, pluggable):
		""" Bind a pluggable object to a slot. """
		if slotName and pluggable:
			if not slotName in self.reservedSlots:
				self._pluggables[slotName] = pluggable
			else:
				# TODO: Throw exception. (JWB)
				pass
		else:
			# TODO: Throw exception. (JWB)
			pass
            
	def free (self, slotName, default=None):
		""" Free a slot, removing the pluggable object and returning it. """
    
		result = None
		try:
			result = self._pluggables[slotName]
            del self._pluggables[slotName] # Remove it.
		except: 
			if self._parent != None:
				result = self._parent.get(slotName)
		return result
        
		if slotName:
			if not slotName in self.reservedSlots:
				delete self._pluggables[slotName]
			else:
				# TODO: Throw exception. (JWB)
				pass
		else:
			# TODO: Throw exception. (JWB)
			pass
            
    def slots (self):
        
	# TODO: delete slot, get list of slot names, etc. (JWB)

def isSlots(val):
	"""Returns true if the passed value is a 
slots instance, otherwise returns false."""
	return isinstance(val, Slots)
