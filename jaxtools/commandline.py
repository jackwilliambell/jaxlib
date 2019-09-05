"""commandline.py

Created by Jack William Bell on 2018-04-10.
Copyright (c) 2018 Jack William Bell. License: MIT"""

import sys
import cmd
from docopt import docopt, DocoptExit
import commands
	
# TODO: Use CommandContext via composition, not inheritance. (JWB)
class CommandLineProcessor(cmd.Cmd, CommandContext):
	"""A Command Line Processor that combines the functionality of the
Python cmd module with jaxtools.commands. Supports both standard cmd 
module 'do_CmdName' functions and jaxtool command exectors."""
	
    prompt = '$ '

	def __init__(self, parent=None, commandSlots={}, reservedSlots=[], properties={}, 
				 threadpoolSize=16, processpoolSize=4):
		# Invoke the CommandContext class init directly.
		CommandContext.__init__(self, parent, commandSlots, reservedSlots, 
								properties, threadpoolSize, processpoolSize)

    def do_exit(self, arg):
        """Exit processing."""

        print('Good Bye!')
		exit()
		

	def verify(self, commandName, command):
		"""
		"""
		# TODO: Implement. Figure out if we just return false or if we want to return
		# more information about what is wrong.
		return False	

	def listOptions(self, commandName):
		# TODO: Implement. (JWB)
		return {}

	def getDoc(self, commandName):
		# TODO: Implement. (JWB)
		return ""

	def getExplanation(self, commandName):
		# TODO: Implement. (JWB)
		return ""

	def getUsage(self, commandName):
		# TODO: Implement. (JWB)
		return ""

	def makeHelpString(self, formatter=None):
		# TODO: Implement. (JWB)
		return ""

#
# Example command context subclass.
#
#@explain("""TODO
#	""")
#@options({
#		'monster': {'aliases': ('m', 'name', 'n'), 'type': 'string', 'hint': 'name', 'doc': 'Specify a monster by name.'},
#		'voltage': {'aliases': ('v'), 'type': 'integer', 'hint': 'volts', 'doc': 'Specify a voltage to use.'},
#		'duration': {'aliases': ('d'), 'type': 'integer', 'hint': 'seconds', 'doc': 'Specify a number of seconds.'},
#		})
# class MonsterHandler(CommandContext):
#	"""TODO
#	"""
#
#		@explain("""Attempts to deliver a shock to a monster. Often used to 'start' the monster
#		or to deliver a punishment. 
#		
#		NOTE: Punishing a monster may be dangerous, as it increases the chance the monster will
#		turn against you.""")
#		@usage({'required': ['monster'], 'optional': ['voltage', 'duration'], 'args': False})
#		def exec_shock(context, options, args, inputHeaders, inputIterator):
#			"""Sends an electric shock to the specified monster.
#			"""
#			context.log("It lives!")
#			return CommandResult(0) # Always return an exit code. '0' always means success.		