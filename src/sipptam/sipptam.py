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
import sets

from conf.Schema import schema
from conf.Parser import Parser
from utils.Utils import str2bool


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
        print 'usage: %s [-c <<config_file>>]' % name
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
    print 'Info. Using configFile: \"%s\"' % configFile
    # Parsing the config file
    if not configFile:
        usage()
    if not os.path.exists(configFile):
        print 'Error: configuration file not found: \"%s\"' % configFile
        usage()

    # Parsing the config file
    try:
        # Parsing configuration file. Lexical validation
        config = Parser(configFile, validate=schema)
    except Exception, err:
        print 'Error: Configuration file error. %s' % str(err)
        usage()

    # Validating the modifications defined and used.
    try:
        # Getting the Set of all the modifications
        ids = sets.Set([x.id for x in config.obj.modification])
        # Getting the Set of all modifications that the tests are using
        testsM = sets.Set(map(lambda x : x.mod, \
                                  filter(lambda x : x.mod, config.obj.test)))
        if not ids.issuperset(testsM):
            raise UnknownMod('Not all modifications used:%s are defined:%s'
                             % (list(testsM), list(ids)))
    except Exception, err:
        print 'Error: %s' % (err)
        usage()

    # Lets get a list of scenarios with scenarioPath. 
    scenarioPath = config.obj.scenarioPath
    scenarioMaxN = int(config.obj.advanced.scenarioMaxN)
    ss = glob.glob(config.obj.scenarioPath)
    # Validating the number of scenarios. scenarioMaxN
    try:
        if not ss:
            raise scenarioPathExcept ('None scenarios found. ' + \
                                          ' scenarioPath:\"%s\"' \
                                          % scenarioPath)
        elif int(scenarioMaxN) < len(ss):
            raise scenarioMaxN ('Found more scenarios than allowed. ' + \
             'Scenarios found:\"%s\" scenarioMaxN:\"%s\"' \
             % (len(ss), scenarioMaxN))
    except Exception, err:
        print 'Error: %s' % (err)
        usage()
    else:
        print 'Info. Success validating scenarioPath:\"%s\"' % scenarioPath
        print 'Info. Success validating scenarioMaxN:\"%s\".' % scenarioMaxN + \
            ' (Number of scenarios found:\"%s\")' % (len(ss))

    # Validating the max size for an scenario. scenarioMaxSize
    # Validating XML scenarios. scenarioValidate
    scenarioMaxSize = int(config.obj.advanced.scenarioMaxSize)
    scenarioValidate = str2bool(config.obj.advanced.scenarioValidate)
    for s in ss:
        try:
            if scenarioMaxSize < os.path.getsize(s):
                raise scenarioMaxSizeExcept \
                    ('Found scenario bigger than allowed' +
                     'Scenario:\"%s\" (\"%s\"B), scenarioMaxSize:\"%s\"B.' % \
                         (s, os.path.getsize(s), scenarioMaxSize))
            if scenarioValidate:
                try:
                    lxml.etree.parse(s)
                except Exception, err:
                    raise scenarioValidate \
                        ('Bad XML validation of scenario:\"%s\"' % s)
        except Exception, err:
            print 'Error: %s' % (err)
            usage()

    # Validating the regexs. regexValidate
    regexValidate = config.obj.advanced.regexValidate
    if regexValidate:
        tmp = sets.Set(map(lambda x : x.regex, config.obj.test))
        for mod in config.obj.modification:
            tmp.update(sets.Set([a.regex for a in \
                                     (list(mod.replace) + list(mod.fieldsf))]))
        for r in tmp:
            try:
                re.compile(r)
            except Exception, err:
                print 'Error: Bad regex found regex:\"%s\". %s' % (r, err)
                usage()
        print 'Info. Success validating regexs.'
    else:
        print 'Info. No need to validate regexs. regexValidate=%s' % \
            config.obj.regexValidate

    # Some exception
    class UnknownMod(Exception):
        pass
    class scenarioPathExcept(Exception):
        pass
    class scenarioMaxNExcept(Exception):
        pass
    class scenarioMaxSizeExcept(Exception):
        pass
    class scenarioValidate(Exception):
        pass

if __name__ == '__main__':
    main()
