#!/usr/bin/env python
# encoding: utf-8
"""# replhelpers.py

Various helper functions for working in 
Read/Execute/Print/Loop (REPL) environments.
For example, in the Python command line.

Created by Jack William Bell on 2018-01-15.

Copyright (c) 2015 Jack William Bell. All rights reserved."""

import sys

def printdoc(obj):
	"""## printdoc() function

Prints the document string for an object."""
	try:
		print(obj.__doc__)
	except:
		print("Could not access object doc string. Error: " + 
			  str(sys.exc_info()[0]))

def printalldocs(obj):
	"""## printalldocs function

Prints all document strings for an object and its 
public attributes."""
	printdoc(obj)
	try:
		for attr in dir(obj):
			try:
				if (not attr.startswith('_')) or attr == "__init__":
					print("\nAttribute: '" + attr + "'")
					printdoc(getattr(obj, attr))
			except:
				print("Could not access object attribute. Error: " + 
					  str(sys.exc_info()[0]))
	except:
		print("Could not access object attributes. Error: " + 
			  str(sys.exc_info()[0]))

def describe(obj):
	"""## describe() function

Prints out everything publically known about an object."""
	print("Type: " + str(type(obj)))
	objs = str(obj)
	if len(objs) > 48:
		objs = objs[0:45] + "..."
	print("String value: " + '"' + objs + '"') 
	printalldocs(obj)