![ScreenShot](http://192.168.200.12/sipptam/blob/master/doc/sipptam_logo_small.png)

SIPp Test Automation Manager
============================

sipptam automates the use of SIPp.

## SIPp
SIPp is a great tool created by HP which allows to generate SIP traffic. A SIPp execution requires an scenario to run, the scenario defines the messages that are going to be sent and received as well as another logic.

## Testing your SIP code using SIPp
SIPp has a flexible way to define its scenarios and makes easy to simulate different SIP traffic flows. SIPp is sometimes used as a powerful SIP bulk load tester. The traditional SIPp execution forces the user to run the desired SIPp command manually. 

## The need of sipptam
The fact of manually run a high number of SIPp commands has obvious disadvantages such as human errors or waste of time. SIPp lacks of ways to automate it. This is where sipptam starts to make sense. If you just have a couple of SIPp scenarios to run against you device under test (SIP UA, SIP proxy, SIP b2bua) manual execution could be allowed, when you have N number of SIPp scenarios and N gets high, you have to look for SIPp automation, sipptam will help you on this.


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