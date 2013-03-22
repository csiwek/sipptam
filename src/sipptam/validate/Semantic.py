#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
sipptam.config.Semantic.py

This function will evaluate need semantic checks in the validation process.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''

import sets
import collections


# Some exceptions
class duplicatedTasExcept(Exception):
    pass
class duplicatedConfigExcept(Exception):
    pass
class duplicatedModExcept(Exception):
    pass
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

def duplicates(obj):
        # Validating the tas list so we dont have any duplicates.
    # @TODO. Dont repeat yourself!
    tmp = [(x.host, x.port) for x in obj.tas]
    if any([x for _,size in collections.Counter(tmp).items() if size > 1]):
        raise duplicatedTasExcept('tas duplicated. Same host and port.')
    print '[info] Success validating duplicated tas.'

    # Validating the config list so we dont have any duplicates.
    # @TODO. Dont repeat yourself!
    tmp = [(x.id) for x in obj.config]
    if any([x for _,size in collections.Counter(tmp).items() if size > 1]):
        raise duplicatedConfigExcept('config duplicated.')
    print '[info] Success validating duplicated config.'

    # Validating the mod list so we dont have any duplicates.
    # @TODO. Dont repeat yourself!
    tmp = [x.id for x in obj.mod]
    if any([x for _,size in collections.Counter(tmp).items() if size > 1]):
        raise duplicatedModsExcept('Mod id duplicated.')
    else:
        print '[info] Success validating duplicated mods.'

def checkSemantics(obj):
    '''
    '''
    duplicates(obj)
    
    # Validating the modifications defined and used.
    try:
        # Getting the Set of all the modifications
        ids = sets.Set([x.id for x in obj.modification])
        # Getting the Set of all modifications that the testruns are using
        testrunsM = sets.Set(map(lambda x : x.mod, \
                                  filter(lambda x : x.mod, obj.testrun)))
        if not ids.issuperset(testrunsM):
            raise UnknownMod('Not all modifications used:%s are defined:%s'
                             % (list(testrunsM), list(ids)))
        for m in ids.difference(testrunsM):
            print '[info] Modification: \"%s\" not used.' % (m)
    except Exception, err:
        print '[error] %s' % (err)
        usage()

    # Lets get a list of scenarios with scenarioPath. 
    scenarioPath = obj.scenarioPath
    scenarioMaxN = int(obj.advanced.scenarioMaxN)
    ss = glob.glob(obj.scenarioPath)
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
        print '[error] %s' % (err)
        usage()
    else:
        print '[info] Success validating scenarioPath:\"%s\"' % scenarioPath
        print '[info] Success validating scenarioMaxN:\"%s\".' % scenarioMaxN + \
            ' (Number of scenarios found:\"%s\")' % (len(ss))

    # Validating the max size for an scenario. scenarioMaxSize
    # Validating XML scenarios. scenarioValidate
    scenarioMaxSize = int(obj.advanced.scenarioMaxSize)
    scenarioValidate = str2bool(obj.advanced.scenarioValidate)
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
            print '[error] %s' % (err)
            usage()

    # Validating the regexs. regexValidate
    regexValidate = obj.advanced.regexValidate
    if regexValidate:
        tmp = sets.Set(map(lambda x : x.regex, obj.testrun))
        for mod in obj.modification:
            tmp.update(sets.Set([a.regex for a in \
                                     (list(mod.replace) + list(mod.fieldsf))]))
        for r in tmp:
            try:
                re.compile(r)
            except Exception, err:
                print '[error] Bad regex found regex:\"%s\". %s' % (r, err)
                usage()
        print '[info] Success validating regexs.'
    else:
        print '[info] No need to validate regexs. regexValidate=%s' % \
            obj.regexValidate
