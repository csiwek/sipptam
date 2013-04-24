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
### \<sipptam\>
* Mandatory. Cardinality : 1.
* _**sipptam.duthost**_, device under test host
* _**sipptam.port**_, device under test port

### \<tas\> 
* Mandatory. Cardinality : Unbounded.
* _**tas.host**_, host to communicate with the tas.
* _**tas.port**_, port to communicate with the tas.
* _**tas.jobs**_, max jobs to assign to this tas.

### \<testrun\>
* Mandatory. Cardinality : Unbounded.
* _**testrun.id**_, identifier for the testrun.
* _**testrun.scenarioPath**_, path where to find the scenarios of the testrun.
* _**testrun.configLink**_, link to the configuration of the testrun. Config must be defined.
* _**testrun.modLink**_, max jobs to assign to this testrun. Mod must be defined. Optional.

```    <testrun id="test-0001"
    	     scenarioPath="/usr/local/share/sipptam/scenarios/test-001*.xml"
    	     configlink="simple"
	     modlink="one"/>
```


***

# Installation
## Debian package
TODO.

## RPM package
TODO.

## Python Package Index
TODO.

***
