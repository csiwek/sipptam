![ScreenShot](http://192.168.200.12/sipptam/blob/master/doc/sipptam_logo.png)

Package description  {#mainpage}
===================

# SIPp Test Automation Manager


This package provides a lot of miscellaneous things that probably should have been included in python's built-in
library but weren't, including:

- Timing execution of a function with a decorator
- An abstract class method
- A way to get the argument names and values of a function without using **kwargs or *args
- An improved ArgParser for parsing command line arguments
- A poor man's debug tracer when a better tracer isn't available (for example, when running a python script over ssh)
- A way to describe the argument and return types of functions, kind of similar to a statically typed language
- A module to get details about a python package (Is it built in? In what file is it? etc.)
- LIFO/Stack implementation
- Easy event logging
- Terminal/user interaction improvements

# Detailed functionality

## Timing execution of a function

	from Lang import timeIt	

`timeIt` is a function decorator, so with the function you want to time, do:

	@timeIt
	def myFunction(...):
		asdf

## An abstract class method

The built in `abc.abstractmethod` decorator won't work if used in conjunction with a `classmethod` decorator.
Use this abstract method decorator instead:

	from Lang import abstractmethod
	
	@classmethod
	@abstractmethod
	def myFunction(...):
		asdf

## Getting a function's arguments

Python provides `**kwargs` and `*args` to get a dictionary or list of a function's arguments, but this makes it hard
for IDEs and documentation generators to determine all possible arguments to the function. As an alternative to
`**kwargs` or `*args`, you can use the `getArgs()` method:

	from Lang import getArgs
	def myFunc(arg1, arg2):
		allArgs = getArgs()

This method uses python's built in `inspect` module to go up the stack and inspect arguments.

In the case above, `allArgs` will be a list of values, similar to as if `*args` was used. To get a dictionary of
argument names and values instead, similar to `**kwargs`, use `getArgs(useKwargFormat=True)`.

Note that `cls` and `self` are automatically ignored for class methods and instance methods.

## An improved ArgParser

In addition to the plethora of features in python's built in `ArgParser`, a few more are added in here:

- Improved help formatting, similar to `man`
- 3 way boolean (`True`, `False`, `None`)
- Required named parameters - the built in ArgParser only supports required positional arguments and optional named parameters

The new `ArgParser` uses the same interface as the old one, so see the built in `ArgParser` documentation.

Example:

	from Lang.ArgParser import ArgParser
    parser = ArgParser(argument_default=None, add_help=True, description="Adds a user to a linux machine")
    parser.add_argument("username")
	parser.add_argument("-p", "--password", required=False, help="Prompt for password if this is not given")
	parser.add_argument("-H", "--create-home", type=Bool3Way, required=True,
		help="Controls home directory creation for user. None uses the default behavior which varies between machines.")
	args = parser.parse_args()

## Poor man's debugger

Several arguments are available here. See the source for more details.

	from Lang.DebugTracer import setTraceOn
	setTraceOn()

## Describing a function's argument and return types

Some convenience classes are defined here that provide a thin, rough API for describing types. See the source in
`Lang.Function` for details.

## Details about python packages
Python can provide a lot of information about a package and a lot of different ways of loading packages, but
the functions and code to accomplish this is scattered. This `PkgUtil` module provides everything in one location.

	from PyPkgUtil import PkgUtil

### Is it built in?

A built in module is one who's source is not defined in a file.

	PkgUtil.isBuiltin(moduleObj)

### Is it included in a stock python distibution?

	PkgUtil.isStock(moduleObj)

### Is an object a module or a package?

	PkgUtil.isModule(obj)
	PkgUtil.isPackage(obj)

### Getting all modules and packages imported by a module

	PkgUtil.getSubs(moduleObj, isRecursive)

Returns a flat list with all modules and packages.

### Getting all packages imported by a module

	PkgUtil.getSubPackages(moduleObj, isRecursive)

Returns a flat list.

### Full module path -> Relative module path

Convert the full file path of a module to a relative path, which can be used for importing:

	relPath = PkgUtil.convert_fullPathToRelative(fullPath)

### Object -> Full path

Get the full file path of a module or package object:

	fullPath = PkgUtil.convert_objectToFullPath(obj)

### Full path -> Object

Get the module or package object from a full path, aka import a module or package at the specified path:

	obj = PkgUtil.convert_fullPathToObject(fullPath)

### Name string -> Object

Import an object by its name:

	obj = PkgUtil.convert_nameToObject("moduleName")

### Object -> Name string

Get the name of a module or package:

	name = PkgUtil.convert_objectToName(obj)

## LIFO/Stack

Python lists can be used as stacks, but they don't have the normal API that a stack does.

	from Lang.QueueStacks import LIFOstack
	stack = LIFOstack()
	stack.push("a")
	element = stack.peek()
	element = stack.pop()

## Event logging

Python has decent built in logging, but it doesn't follow standard object-oriented concepts where methods represent
actions, so the API is not ideal for recording different events in a heavily event based system, as there would need
to be a special, separate call to the logging API for every event. The logging API in `Lang.Logging` fixes this.

### Example using StdoutLogger

This is a very simplistic example of logging to stdout:

	from Lang.Logging import Logging, StdoutLogger
	log = Logging(StdoutLogger)
	log.notifyMyEvent("details", "in", "arguments", "here")

### Example using a custom logger and/or multiple loggers

When using multiple loggers, the function you call on the `Logging` instance will be called on every logger.

	from Lang.Logging import Logging, LoggerAbstract, StdoutLogger
	class MyFileLog(LoggerAbstract):
		def __init__(self, filePath):
			super(MyLogger, self).__init__()
			self._filePath = filePath
		def notifyFolderCheck(self, folder):
			with open(self._filePath, "a") as file_:
				file_.write("Checking folder: " + folder)
	
	log = Logging((StdoutLogger, MyFileLog))
	log.notifyFolderCheck("folder/path/here")

### Logging uncaught exceptions

When an uncaught exception happens, a special `notifyException` method will be called on each of your loggers
automatically if it exists, with the exception instance and a traceback instance as parameters. What you do with
these parameters is up to you, but here is an example:

	def notifyException(self, exceptionInstance, tracebackInstance):
		import traceback
		tracebackStr = "".join(traceback.format_tb(tracebackInstance))
		exceptionStr = str(exceptionInstance)
		print(tracebackStr)
		print()
		print(exceptionStr)

## Terminal improvements

### Asking a question to the user

	from Lang import Terminal
	if Terminal.askYesNo("Do you like Star Trek?") == True:
		print("Awesome!")
	else:
		print("Your nerd credit has been lowered")

### Using formatted text on the terminal

	from Lang.Terminal import FormattedText

`FormattedText` returns a subclass of the built in python `str` type. It adds terminal formatting codes when
the `str` function is called on it:

	boldStr = str(FormattedText("I'm in bold", bold=True))

`boldStr` will contain some funny looking characters which enable formatting, but these characters do not influence
any other function of the string. For example:

	char = boldStr[2]

will store `m` into `char`. Similarly, `len` and other functions will act the same as if the string were a direct
instantiation of `str`.
 
Many more text attributes are available, including coloring - see the source for more information.

### Tables

Printing tabular data to the terminal is very common. This implementation of a table has a couple extras with it.
Here is an example:

	from Terminal import Table
	table = Table()
	table.setColHeaders(("First Name", "Last Name Initial", "Number"))	# optional
	table.setColMaxLens([None] * 3)			# enables automatic column sizing for the 3 columns
	table.addRow(["Jesse", "C", str(1234)])	# explicitly convert all elements to strings
	table.printLive()						# prints all rows (and headers) that haven't been printed before

If another row is added to the table, another call to `printLive()` will only print only that new row.

