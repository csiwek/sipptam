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
from conf.Parser import Parser
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
        config = Parser(configFile, validate=schema)
    except Exception, err:
        print 'Configuration file error. Error:%s' % str(err)
        usage()

    print '=' * 60
    print config
    print '=' * 60

if __name__ == '__main__':
    main()
