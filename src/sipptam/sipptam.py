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
    configFile = '/etc/sipptam/config/sipptam.xml'
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
        print 'Not running. Usage: %s [-c <<config_file>>]' % name
        sys.exit(1)

    # Lets parse input parameters
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:')
    except getopt.GetoptError:
        usage()
    # Looking for command line parameters
    for o, a in opts:
        if o == '-c':
            configFile = a
            continue

    # Show which config file are we using
    print '[info] Using configFile:\"%s\"' % configFile
    # Parsing the config file
    try:
        # Parsing configuration file. Lexical validation
        config = Validate(configFile, parse=True)
        config.checkSemantics()
    except Exception, err:
        print '[error] Configuration file error. %s' % str(err)
        usage()


    # Validation done. Creating objects from the parameters.
    tasL = fill(Tas, config.obj.tas)
    testrunL = fill(Testrun, config.obj.testrun)
    configD = fill(Config, config.obj.config, dic = True)
    modD = fill(Mod, config.obj.mod, dic = True)

    print '--'
    print tasL
    print '--'
    print testrunL
    print '--'
    print configD
    print '--'
    print modD
    print '--'

if __name__ == '__main__':
    main()
