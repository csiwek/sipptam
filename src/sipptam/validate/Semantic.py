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
import glob
import lxml
import re

from sipptam.utils.Utils import str2bool


# Some exceptions
class duplicatedTasExcept(Exception):
    pass
class duplicatedConfigExcept(Exception):
    pass
class duplicatedModExcept(Exception):
    pass
class modNotDefined(Exception):
    pass
class configNotDefined(Exception):
    pass
class scenarioPathExcept(Exception):
    pass
class scenarioMaxNExcept(Exception):
    pass
class scenarioValidateExcept(Exception):
    pass
class regexValidateExcept(Exception):
    pass


def checkDuplicates(l, exception):
    '''
    Checks if we have any duplicates in the list @l,
    if not @exception is raised.
    '''
    if any([True for _,size in collections.Counter(l).items() if size > 1]):
        raise exception

def checkDefinedUsed(definedL, usedL, exception):
    '''
    This function checks if the members of the list @usedL 
    are defined in the @definedL, if not @exception is raised.
    '''
    definedSet = sets.Set(definedL)
    usedSet = sets.Set(usedL)
    if not definedSet.issuperset(usedSet):
        raise exception
    return list(definedSet.difference(usedSet))

def checkSemantics(obj):
    '''
    '''
    # Check duplicated items
    checkDuplicates([(x.host, x.port) for x in obj.tas],
                  duplicatedTasExcept('tas duplicated. Same host and port.'))
    print '[info] Success validating duplicated \"tas\" items.'
    checkDuplicates([(x.id) for x in obj.config],
                  duplicatedConfigExcept('config id duplicated.'))
    print '[info] Success validating duplicated \"config\" items.'
    checkDuplicates([x.id for x in obj.mod],
                  duplicatedModExcept('Mod id duplicated.'))
    print '[info] Success validating duplicated \"mod\" items.'

    # Checking mod defined and used. Making sure modlink exists.
    notused = checkDefinedUsed([x.id for x in obj.mod],
                               [x.modlink for x in obj.testrun if x.modlink],
                               modNotDefined('Found mods not defined'))
    print '[info] Success validating \"mod\"s used & defined.'
    for m in notused:
        print '[info] mod:\"%s\" not used.' % (m)

    # Checking config defined and used.
    notused = checkDefinedUsed([x.id for x in obj.config],
                               [x.configlink for x in obj.testrun],
                               configNotDefined('Found configs not defined'))
    print '[info] Success validating \"config\"s used & defined.'
    for m in notused:
        print '[info] config:\"%s\" not used.' % (m)

    # Lets get a list of scenarios with scenarioPath. 
    ss = sets.Set([])
    for sp in sets.Set([x.scenarioPath for x in obj.testrun]):
        ss.update(glob.glob(sp))
        print '[info] Success validating scenarioPath:\"%s\"' % sp

    # Lets validate scenarioMaxN in case it is desired.
    scenarioMaxN = obj.advanced.scenarioMaxN
    if scenarioMaxN: 
        # Validating the number of scenarios. scenarioMaxN
        if not ss:
            raise scenarioPathExcept ('None scenarios found. ' + \
                                          ' scenarioPath:\"%s\".' \
                                          % scenarioPath)
        elif int(scenarioMaxN) < len(ss):
            raise scenarioMaxNExcept ('Found more scenarios than allowed. ' + \
                                          'scenarioMaxN:\"%s\". (Found:%s)' \
                                          % (scenarioMaxN, len(ss)))
        print '[info] Success validating scenarioMaxN:\"%s\". (Found:%s)' % \
            (scenarioMaxN, len(ss))
    else:
        print '[info] No need to validate the scenarioMaxN param.'

    # Validating well formed XML scenarios. scenarioValidate
    if str2bool(obj.advanced.scenarioValidate):
        for s in ss:
            try:
                lxml.etree.parse(s)
            except Exception, err:
                raise scenarioValidateExcept \
                    ('Bad XML validation of scenario:\"%s\"' % s)
            else:
                print '[info] Success while XML parsing scenario:\"%s\"' % s

    # Validating well formed regexs. regexValidate
    if str2bool(obj.advanced.regexValidate):
        # Getting a set og the regexs of the testruns.
        tmp = sets.Set([x.regex for x in obj.testrun])
        # Updating the set with regexs of the mods.
        for m in obj.mod:
            tmp.update(sets.Set([a.regex for a in \
                                     (list(m.replace) + list(m.fieldsf))]))
        # Trying to compile every regex defined.
        for r in tmp:
            try:
                re.compile(r)
            except Exception, err:
                raise regexValidateExcept('Bad regex:regex:\"%s\". %s' % \
                                              (r, err))
            else:
                print '[info] Success parsing regex:\"%s\"' % r
    else:
        print '[info] No need to validate the regexValidate param.'
