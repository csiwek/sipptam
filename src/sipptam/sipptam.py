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
        Small helper function which exists
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
        print 'Configuration file error. Error:%s' % str(err)
        usage()
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

    # Checking if regexs are well formed
    if str2bool(config.obj.advanced.regexValidate):
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
    print 'Info. Done!'

    # Unknown modification
    class UnknownMod(Exception):
        pass

if __name__ == '__main__':
    main()
