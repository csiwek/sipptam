![ScreenShot](http://192.168.200.12/sipptam/blob/master/doc/sipptam_logo_small.png)

SIPp Test Automation Manager
============================

`sipptam` automates the use of SIPp. It distributes the SIPp scenarios and parameters using.

# 

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