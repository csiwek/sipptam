![ScreenShot](http://192.168.200.12/sipptam/blob/master/doc/sipptam_logo_small.png)

SIPp Test Automation Manager
============================

`sipptam` automates the use of SIPp.

# The need of `sipptam`

## SIPp
SIPp is a great tool created by HP which allows to generate SIP traffic. A SIPp execution requires an scenario to run, the scenario defines the messages that are going to be sent and received as well as another logic. The traditional SIPp execution forces the user to run the desired SIPp command manually.

## Testing your SIP code using SIPp
SIPp has an smart way to define its scenarios and make it easy for the user to simulate different SIP traffic flows. Its engine to make bulk calls is very impressive. 

##

When you have two or more scenarios for the same test it is a little inconvenient.
Developing SIP applications requires an environment 
It distributes the SIPp scenarios and parameters using different slaves. 

## Reusing a binded port in the tas.
- The device under tests keeps sending SIP messages to a port that we were using
in another test. The new test if it is binded in the same port will be likely to fail.

# Configuration
Configuration is made through an XML file passed at runtime.

## config.xml

	from Lang import timeIt	

`timeIt` is a function decorator, so with the function you want to time, do:

	@timeIt
	def myFunction(...):
		asdf