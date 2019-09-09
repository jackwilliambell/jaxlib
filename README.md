*jaxtools* is a module containing an eclectic set of Python objects and functions which I will use in just about every Python project I do. You can use it as well, but your mileage may vary.

# Requirements

*jaxtools* has no external requirements by design. Some of the code was originally created with Python 2.7, but most later developement used Python 3+. While some portions of *jaxtools* may work with Python 2.6+, no effort has been made to make it compatible.

# Features

* Single package namespace: you can import every module as 'from modulename import *' and get no name collisions from within *jaxtools*

* Concrete implementations of high-level design patterns like Command, Walker/Visitor and Object Factory

* A unique (and very safe) serialization strategy using dependency injection for readers and writers and Object Factory implementations; allowing you to use local I/O functionality and local versions of classes when deserializing objects

* Support for creating command-line apps, compatible with *docopt*
    - *docopt*: http://docopt.org/

* Support for creating REPLs, improving on the *cmd* module but using dependency injection for terminal control, compatible with terminal IO libraries like *curses*, *prompt*toolkit* and *urwid*
    - *prompt_toolkit*: https://github.com/prompt-toolkit/python-prompt-toolkit
    - *urwid*: http://urwid.org/

# Caveats

* I'm using my own naming conventions and design practices over doing things the more Pythonic way (FWIW, I use the same conventions and practices with C and C++) 

* The functions and classes use each other in a deep way, it may be difficult to pull selected APIs out from the package and use them without all the rest of it

* I'm using this library to experiment with a YAML/Markdown-based docstring format of my own design; it should be easily readable, but won't work with standard documentation generators

# Status

At this time *jaxtools* is not ready for prime time or even taking a quick look at. So go away until this notice disappears.
 
 *jaxtools* being actively worked on to use with another project. I am currently moving over bits of code from an earlier version of *jaxtools* and from other modules and refactoring them for consistency and better coding practices. 
 
 ## TODO
 
 * Get basics working with some tests and tag with version number, use same version in metadata
    - Determin version number format (I like date-based, but don't know if it's valid for metadata)
 
 * Set up for and upload to Pypi
    - see: http://www.discoversdk.com/blog/how-to-create-a-new-python-module
    - see: https://www.codementor.io/arpitbhayani/host-your-python-package-using-github-on-pypi-du107t7ku
    - see: https://code.tutsplus.com/tutorials/how-to-write-package-and-distribute-a-library-in-python--cms-28693
    - more: https://docs.python-guide.org/shipping/packaging/
    - more: https://github.com/pypa/wheel - https://pythonwheels.com/
 
 