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

    print config
    print '=' * 60    

    class FieldsFile(object):
        '''
        '''
        ffile = None
        def __init__(self, ffile, *args, **kwargs):
            super(FieldsFile, self).__init__(*args, **kwargs)
            self.ffile = ffile
        def __str__(self):
            return 'FieldsFile ffile:%s' % \
                (self.ffile)

    class Replace(object):
        '''
        '''
        src = None
        dst = None
        def __init__(self, src, dst, *args, **kwargs):
            super(Replace, self).__init__(*args, **kwargs)
            self.src = src
            self.dst = dst
        def __str__(self):
            return 'Replace src:%s, dst:%s' % \
                (self.src, self.dst)

    class Configuration(object):
        '''
        '''
        id = None
        replaces = None
        fields = None
        def __init__(self, id):
            self.id = id
            self.replaces = []
            self.fields = []
        def __str__(self):
            return 'configuration:%s \n%s' % \
                (str(self.id),
                 '\n'.join(str(n) for n in self.replaces),
                 '\n'.join(str(n) for n in self.fields))
        def __eq__(self, name):
            return (self.id == name)
        def add(self, item):
            if isinstance(item, Replace):
                self.replaces.append(item)
            elif isinstance(item, FieldsFile):
                self.fields.append(item)
            else:
                raise Exception('Item type unknown')


    class Scenario(object):
        '''
        '''
        path = None
        mods = None
        def __init__(self, path):
            self.path = path
            self.mods = []
        def __eq__(self, name):
            return (self.path == name)
        def __str__(self):
            return '%s \n%s' % (str(self.path),
                                '\n'.join(str(n) for n in self.mods))
        def add(self, mod):
            self.mods.append(mod)
        def hasMods(self):
            return self.mod
        def apply(self, cache):
            try:
                content = cache[self.path]
                #map(lambda x : x., self.mods)
            except:
                raise

    class ScenarioAlreadyAdded(Exception):
        pass

    class Testrun(object):
        '''
        '''
        scenarios = None
        cache = None
        def __init__(self):
            self.scenarios = []
        def __str__(self):
            return '\n%s\n%s' % \
                ('\n\n'.join(str(n) for n in self.scenarios),
                 self.cache)
        def addScenario(self, scenario):
            if scenario in self.scenarios:
                raise ScenarioAlreadyAdded
            self.scenarios.append(scenario)
#        def updateScenario(self, scenario, mod):
#            if scenario in self.scenarios:
#                index = self.scenarios.index(scenario)
#                self.scenarios[index].add(mod)
#            else:
#                raise Exception('Can\'t update scenario:%s. Doesn\'t exist') % \
#                    scenario
        def setCache(self, cache):
            self.cache = cache
        def run(self):
            for s in self.scenarios:
                print s.apply(self.cache)

    from sets import Set
    scenarioCacheSet = Set([]) # All the scenarios that applied
    trs = []
    
    def applies(regex, l):
        '''
        Based on a given regex and a list of paths,
        returns the list of paths that match the regex.
        '''
        validator = re.compile(regex)
        return filter(lambda x : validator.match(os.path.basename(x)), l)

    # Lets get deeper in the testrunList
    for testrun in config.getList('testrunList'):
        # List of scenarios that match the given regex.
        regex = testrun['applyRegex']
        apply = applies(regex, ss)
        scenarioCacheSet.update(apply)
        if not apply:
            print 'WARNING. Invalidating testrun.' + \
                'None scenario matches to regex:\"%s\"' % (regex)
        else:
            tr = Testrun()
            map(lambda x : tr.addScenario(Scenario(x)), apply)
            # Lets see if we have modifications here
            # 
            # Adding the testrun tr the testrun list
            trs.append(tr)

    def fun(name):
        with open(name, 'r') as f:
            ret = f.read()
        return ret
    cache = dict(zip(scenarioCacheSet, map(fun, scenarioCacheSet)))
    map(lambda x : x.setCache(cache), trs)

    print '=' * 60
    for tmp in trs:
        print '-' * 30
        tmp.run()
    print '=' * 60

if __name__ == '__main__':
    main()
