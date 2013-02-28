#!/usr/local/bin/python
import getopt
import os
import sys

from conf.Schema import schema
from conf.Configuration import Configuration

def main ():
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

    # Playing a little bit with this
    print config
    # Playing with it... Lets print all the tass
    defaultN = config.getAttr('tasList', 'defaultJobs')
    defaultPort = config.getAttr('tasList', 'defaultPort')
    for tas in config.getList('tasList'):
        try:
            tmp_n = tas['jobs']
        except:
            tmp_n = defaultN
        try:
            tmp_port = tas['port']
        except:
            tmp_port = defaultPort
        for n in range(0, int(tmp_n)):
            print '%s:%s:%s' % (tas['host'], tmp_port, n)


if __name__ == '__main__':
    main()