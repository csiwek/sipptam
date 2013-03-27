#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.sipptam
    ~~~~~~~~~~~~~~~

    Main sipptam module.

    :copyright: (c) 2013 INdigital Telecom. luismartingil.
    :license: See LICENSE_FILE.
"""
import getopt
import sys

from validate.Validate import Validate
from utils.Utils import fill
from tas.Tas import Tas
from testrun.Testrun import Testrun
from config.Config import Config
from mod.Mod import Mod
from utils.FileManager import FileManager
from testrun.Scenario import Scenario
from mod.Replace import Replace
from mod.Fieldsf import Fieldsf


def main ():
    '''
    Main function.
    '''
    # Setting some default variables
    name = 'sipptam'
    configFilePath = '/etc/sipptam/sipptam.xml'
    logFormat = '%(levelname)-7s ' + \
        '%(name)6s ' + \
        '%(asctime)s ' + \
        '%(threadName)-24s ' + \
        '%(filename)-24s ' + \
        '+%(lineno)-4d ' + \
        '%(funcName)-22s ' + \
        '%(message)s '

    def usage():
        '''
        Helper function to which prints how to run this script
        '''
        print 'Not running. Usage: %s [-c <<configFilePath>>]' % name
        sys.exit(1)

    # Lets parse input parameters
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:')
    except getopt.GetoptError:
        usage()
    # Looking for command line parameters
    for o, a in opts:
        if o == '-c':
            configFilePath = a
            continue

    # Show which configFile are we using
    print '[info] Using configFilePath:\"%s\"' % configFilePath
    # Parsing the configFile file
    try:
        # Parsing configFile. Lexical validation
        configFile = Validate(configFilePath, parse=True)
        configFile.checkSemantics()
    except Exception, err:
        print '[error] ConfigFile file error. %s' % str(err)
        usage()

    # Reading the files and storing them for future reads.
    scenarioCache = FileManager()
    scenarioCache.addFile(configFile.obj.ssSet)

    # Validation done. Creating objects from the parameters.
    tasL = fill(Tas, configFile.obj.tas)
    testrunL = fill(Testrun, configFile.obj.testrun)
    configDic = fill(Config, configFile.obj.config, dic = True)
    modDic = fill(Mod, configFile.obj.mod, dic = True)

    # Lets create the proper modification objects
    for m in configFile.obj.mod:
        tmp = {'replaces' : fill(Replace, m.replace),
               'fieldsfs' : fill(Fieldsf, m.fieldsf)}
        m._attrs.update(tmp)

    # Attaching {config, mod} objects in the testruns.
    for t in testrunL:
        # Setting the proper config to the testrun.
        config = configDic[t.get('configlink')]
        t.set('config', config, type(config))

        # Setting the proper mod in the testrun.
        if t.has('modlink'):
            mod = modDic[t.get('modlink')]
            t.set('mod', mod, type(mod))

        # Setting the proper scenarioCache.
        t.set('scenarioCache', scenarioCache, type(scenarioCache))
        t.run()

if __name__ == '__main__':
    main()
