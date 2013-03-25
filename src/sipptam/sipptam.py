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

    # Validation done. Creating objects from the parameters.
    tasL = fill(Tas, configFile.obj.tas)
    testrunL = fill(Testrun, configFile.obj.testrun)
    configDic = fill(Config, configFile.obj.config, dic = True)
    modDic = fill(Mod, configFile.obj.mod, dic = True)

    # Attaching {config, mod} objects to the testruns.
    for t in testrunL:
        config = configDic[t.get('configlink')]
        t.set('config', config, type(config))
        if t.has('modlink'):
            mod = modDic[t.get('modlink')]
            t.set('mod', mod, type(mod))

    # @TOREMOVE @TMP
    for t in tasL:
        print t
    print '-' * 80
    for t in testrunL:
        print t
        t.tmpRun()
        print '~' * 60
        
if __name__ == '__main__':
    main()
