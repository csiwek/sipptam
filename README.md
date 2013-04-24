![ScreenShot](http://192.168.200.12/sipptam/blob/master/doc/sipptam_logo_small.png)

SIPp Test Automation Manager
============================

***

# Introduction

## SIPp
SIPp is a great tool created by HP which allows to generate SIP traffic. A SIPp execution requires an scenario to run, the scenario defines the messages that are going to be sent and received as well as another logic.
## Testing your SIP code using SIPp
SIPp has a flexible way to define its scenarios and makes easy to simulate different SIP traffic flows. SIPp is sometimes used as a powerful SIP bulk load tester. The traditional SIPp execution forces the user to run the desired SIPp command manually. 
## The need of sipptam
The fact of manually run a high number of SIPp commands has obvious disadvantages such as human errors or waste of time. SIPp lacks of ways to automate it. This is where sipptam starts to make sense. If you just have a couple of SIPp scenarios to run against you device under test (SIP UA, SIP proxy, SIP b2bua) manual execution could be allowed, when you have N number of SIPp scenarios and N gets high, you have to look for SIPp automation, sipptam is what you are looking for. `sipptam` automates the use of SIPp.

***

# How it works
## sipptam and sipptas as twins : manager and slave(s)
Two basic type of entities in the {sipptam, sipptas} world.
- `sipptam`, manager which reads the scenarios and parameters, it distributes the SIPp jobs among the slaves (`sipptas`), checks the process of them and outputs the result back to the user.
- `sipptas`, slave which performs SIPp jobs. It provides an API for executing SIPp jobs in the box where it is running.

## Scenario execution order
TODO

***

# Configuration
Configuration is made through an XML file passed at runtime.

## config.xml
1. You can find the **schema** of the XML configuration file [here](http://192.168.200.12/sipptam/tree/master/src/sipptam/validate/Schema.py)
2. You have a configuration file **example** [here](http://192.168.200.12/sipptam/tree/master/resources/sipptam.sample.xml)

## Parameters
- `sipptam`, basic sipptam root **node**. Mandatory. Cardinality : 1.
- `sipptam.duthost`, device under test host
- `sipptam.port`, device under test port
- `tas`, test automation slave **node**. Mandatory. Cardinality : Unbounded.
- `tas.host`, host to communicate with the tas.
- `tas.port`, port to communicate with the tas.
- `tas.jobs`, max jobs to assign to this tas.

- `testrun`, testrun **node**. Mandatory. Cardinality : Unbounded.
- `testrun.id`, identifier for the testrun.
- `testrun.scenarioPath`, path where to find the scenarios of the testrun.
- `testrun.configLink`, link to the configuration of the testrun. Config must be defined.
- `testrun.modLink`, max jobs to assign to this testrun. Mod must be defined. Optional.
~~~

    <testrun id="test-0001"
    	     scenarioPath="/usr/local/share/sipptam/scenarios/test-001*.xml"
    	     configlink="simple"
	     modlink="one"/>

~~~


    <config id="simple"
    	    ratio="1"
	    max="1"
	    pause="1.0"
	    tries="1"/>
~~~
    <mod id="one">
    	 <replace regex="(.*_a.xml)" src="__notusednow1__" dst="tmp1a"/>
	 <replace regex="(.*_a.xml)" src="__notusednow2__" dst="tmp1a"/>
	 <injection regex="(.*)" path="/usr/local/share/sipptam/injections/injection1.sample.csv"/>
    </mod>
~~~
   <advanced execMode="parallel"
             scenarioValidate="False"
	     regexValidate="True"/>
~~~

***

# Installation
## Debian package
TODO.

## RPM package
TODO.

## Python Package Index
TODO.

***
