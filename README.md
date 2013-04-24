![ScreenShot](http://192.168.200.12/sipptam/blob/master/doc/sipptam_logo_small.png)

SIPp Test Automation Manager
============================

***

# Introduction

## SIPp
[SIPp](http://sipp.sourceforge.net/) is a great tool created by HP which allows to generate SIP traffic. A SIPp execution requires an scenario to run, the scenario defines the messages that are going to be sent and received as well as another logic. Multiple parameters can be defined. Also, it has a flexible way to define its highly customizable scenarios.
## Testing your SIP code using SIPp. The need of sipptam
SIPp makes easy to simulate different SIP traffic flows. SIPp is sometimes used as a powerful SIP bulk load tester. The traditional SIPp execution forces the user to run the desired SIPp command manually. The fact of manually run a high number of SIPp commands has obvious disadvantages such as human errors or waste of time. SIPp lacks of ways to automate it. This is where sipptam starts to make sense. If you just have a couple of SIPp scenarios to run against you device under test (SIP UA, SIP proxy, SIP b2bua) manual execution could be allowed, when you have N number of SIPp scenarios and N gets high, you have to look for SIPp automation, sipptam is what you are looking for. **`sipptam` automates the use of SIPp**.

***

# How it works
## Manager and slave(s). `sipptam` and `sipptas` [Yin yang](http://en.wikipedia.org/wiki/Yin_and_yang)
Two basic type of entities in the {sipptam, sipptas} world.
- `sipptam`, manager which reads the scenarios and parameters, it distributes the SIPp jobs among the slaves (`sipptas`), checks the process of them and outputs the result back to the user.
- `sipptas`, slave which performs SIPp jobs. It provides an API for executing SIPp jobs in the box where it is running.

TODO image

## Scenario execution order
**The order which scenarios are selected defines the scenarios order execution.**

#### Example
Having this folder:
- `/tmp/test-0000.xml`
- `/tmp/test-0001_a.xml`
- `/tmp/test-0001_b.xml`
- `/tmp/test-0002_a.xml`
- `/tmp/test-0002_b.xml`
- `/tmp/test-0002_c.xml`

A testrun defined with this `scenarioPath="/tmp/test-0002_*.xml"` would select this scenarios:
- `/tmp/test-0002_a.xml`
- `/tmp/test-0002_b.xml`
- `/tmp/test-0002_c.xml`

Again, the order which scenarios are selected defines the scenarios order execution. In this example, `/tmp/test-0002_a.xml` will run first, `/tmp/test-0002_b.xml` will run second and `/tmp/test-0002_c.xml` will run third. The last scenario selected (`/tmp/test-0002_c.xml` in this example) will be the one that will send the first INVITE in the scenario, this way the user makes sure the first two scenarios are already waiting for this INVITE and the testrun is well syncronized.


## Execution mode
parallel, serial

TODO image

r, m, tries
TODO plot

***

# Configuration
Configuration is made through an XML file passed at runtime.

## Example
You can find one [here](http://192.168.200.12/sipptam/tree/master/resources/sipptam.sample.xml)

## Schema
You can find the **schema** of the XML configuration file [here](http://192.168.200.12/sipptam/tree/master/src/sipptam/validate/Schema.py)
### \<sipptam\>
* Mandatory. Cardinality : **1**.
* _**sipptam.duthost**_, device under test host
* _**sipptam.port**_, device under test port

```<sipptam duthost="10.22.22.112" dutport="5060">
```

### \<tas\> 
* Mandatory. Cardinality : **Unbounded**.
* _**tas.host**_, host to communicate with the tas.
* _**tas.port**_, port to communicate with the tas.
* _**tas.jobs**_, max jobs to assign to this tas.

```<tas host="10.22.22.200" port="8008" jobs="25"/>
```

### \<testrun\>
* Mandatory. Cardinality : **Unbounded**.
* _**testrun.id**_, identifier for the testrun.
* _**testrun.scenarioPath**_, path where to find the scenarios of the testrun.
* _**testrun.configLink**_, link to the configuration of the testrun. Config must be defined.
* _**testrun.modLink**_, max jobs to assign to this testrun. Mod must be defined. Optional.

```    <testrun id="test-0001"
    	     scenarioPath="/usr/local/share/sipptam/scenarios/test-001*.xml"
    	     configlink="simple"
	     modlink="one"/>
```

### \<config\> 
* Mandatory. Cardinality : **Unbounded**.
* _**config.id**_, identifier for the configlink.
* _**config.ratio**_, semicolon separated list of ratio (SIPp parameter, calls per seconds).
* _**config.max**_, semicolon separated list of calls (SIPp parameter, maximum calls to make).
* _**config.pause**_, seconds to pause between every {ratio, max} combination.
* _**config.tries**_, number of times to execute every {ratio, max} combination.

```   <config id="advanced"
              ratio="5;10"
	      max="20;60"
	      pause="5.0"
	      tries="2"/>
```


### \<mod\> 
* Optional. Cardinality : **Unbounded**.
* _**mod.id**_, identifier for the configlink.

```     <mod id="one">
	    	 <replace regex="(.*_a.xml)" src="__notusednow1__" dst="tmp1a"/>
		 <replace regex="(.*_a.xml)" src="__notusednow2__" dst="tmp1a"/>
		 <injection regex="(.*)" path="/usr/local/share/sipptam/injections/injection1.sample.csv"/>
	</mod>
```

###### \<replace\>
* Optional. Cardinality : **Unbounded**.
* _**mod.replace.regex**_, scenarios from the testrun which match this regex will use this ``replace`` modification.
* _**mod.replace.src**_, string to be replaced in the scenario.
* _**mod.replace.dst**_, string to replace in the scenario.

```     <replace regex="(.*_a.xml)" src="__notusednow2__" dst="tmp1a"/>
```

###### \<injection\>
Injection modification are used to inject values from external files. Files injectected will be passed with the scenarios that apply. Please check the -inf param of SIPp [here](http://sipp.sourceforge.net/doc/reference.html#Injecting+values+from+an+external+CSV+during+calls).
* Optional. Cardinality : **Unbounded**.
* _**mod.injection.regex**_, scenarios from the testrun which match this regex will use this ``injection`` modification.
* _**mod.injection.path**_, injection file to attach to the .

```     <injection regex="(.*)" path="/usr/local/share/sipptam/injections/injection1.sample.csv"/>
```


### \<advanced\>
* Mandatory. Cardinality : **1**.
* _**advanced.execMode**_, execution mode. parallel will run all the testruns at the same time. serial will run one testrun after another in the way they are defined.
* _**advanced.scenarioValidate**_, checks that all the scenarios loaded in the testruns pass basic XML validation.
* _**advanced.regexValidate**_, checks that the regex defined by the user are correct.

```   <advanced execMode="parallel"
      		scenarioValidate="False"
		regexValidate="True"/>
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
