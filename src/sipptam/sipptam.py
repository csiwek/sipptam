#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.sipptam
    ~~~~~~~~~~~~~~~

    Main sipptam module.

    :copyright: (c) 2013 by luismartingil.
    :license: See LICENSE_FILE.
"""
import getopt
import os
import sys
import glob
import lxml
import re

from conf.Schema import schema
from conf.Configuration import Configuration
from utils.Utils import str2bool


def main ():
    '''
    Main function.
    '''
    # Setting some default variables
    name = 'sipptam'
    configFile = '/etc/sipptam/sipptam.conf'
    logFormat = '%(levelname)-7s ' + \
        '%(name)6s ' + \
        '%(asctime)s ' + \
        '%(threadName)-24s ' + \
        '%(filename)-24s ' + \
        '+%(lineno)-4d ' + \
        '%(funcName)-22s ' + \
        '%(message)s '

    def usage():
        print 'usage: %s [-c <<config_file>>]' % name
        sys.exit(1)

    # Lets parse input parameters
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:')
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    global_config = {}

    # Looking for command line parameters
    for o, a in opts:
        if o == '-c':
            configFile = a
            continue

    # Parsing the config file
    if not configFile:
        usage()
    if not os.path.exists(configFile):
        print 'Error: configuration file not found: \"%s\"' % configFile
        usage()
    try:
        # Parsing configuration file. Lexical validation
        config = Configuration(configFile, validate=schema)
    except Exception, err:
        print 'Configuration file error. Error:%s' % str(err)
        usage()

    # Lets check the scenarios that the user wants to work with. 
    # Complexity: O(n). n is the number of scenarios
    try:
        scenariosPath = config.getAttr('testrunList', 'scenariosPath')
        ss = glob.glob(scenariosPath)
        if not ss:
            raise Exception ('None scenarios found in scenariosPath:\"%s\"' % \
                                 scenariosPath)
        # Lets validate the XML
        if str2bool(config.getAttr('testrunList', 'validateScenarioXML')):
            for s in ss:
                lxml.etree.parse(s)
                print 'Parsed XML from scenario:\"%s\"' % s
    except Exception, msg:
        print 'Error while getting the scenarios. %s' % msg
        usage()

    # Lets get deeper into the testList
    print 'Reading tests'
    for t in config.getList('testrunList'):
        validator = re.compile(t['applyRegex'])
        regex = t['applyRegex']
        # List of scenarios that match the given regex.
        match = filter(lambda x : validator.match(os.path.basename(x)), ss)
        if not match: print 'Warning. None scenarios associated to t:\"%s\"' % t
        if t.has_key('modificationList'):
            import pprint
            #import sipptam.utils.
            #listField
            for replaceList in t['modificationList']['__list__']:
                for replace in replaceList['__list__']:
                    print replace
                print '*' * 10
                
        print '-' * 60
    print
    print '.End.'
    print
    print config

if __name__ == '__main__':
    main()
