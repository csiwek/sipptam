#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
sipptam.config.Semantic.py

This function will evaluate need semantic checks in the validation process.
Adds some attributes to make things easier later.
Removes not used configuration.

@author:  Luis Martin Gil
@contact: martingil.luis@gmail.com
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''

import sets
import collections
import glob
import lxml
import re
import logging
import os

from sipptam.utils.Utils import str2bool, flat

logger = logging.getLogger(__name__)

# Some exceptions
class duplicatedTasExcept(Exception):
    pass
class duplicatedTestrunExcept(Exception):
    pass
class duplicatedConfigExcept(Exception):
    pass
class duplicatedModExcept(Exception):
    pass
class modNotDefined(Exception):
    pass
class configNotDefined(Exception):
    pass
class testrunsEmptyExcept(Exception):
    pass
class scenarioPathExcept(Exception):
    pass
class notEnoughTasExcept(Exception):
    pass
class scenarioValidateExcept(Exception):
    pass
class injectionFileNotExists(Exception):
    pass
class regexValidateExcept(Exception):
    pass


def checkDuplicates(l, exception):
    '''
    Checks if we have any duplicates in the list @l,
    if not @exception is raised.
    '''
    if len(l) != len(set(l)):
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
    logger.debug('Success validating duplicated \"tas\" items.')
    checkDuplicates([x.id for x in obj.testrun],
                    duplicatedTestrunExcept('testrun id duplicated.'))
    logger.debug('Success validating duplicated \"testrun\" items.')
    checkDuplicates([x.id for x in obj.config],
                    duplicatedConfigExcept('config id duplicated.'))
    logger.debug('Success validating duplicated \"config\" items.')
    checkDuplicates([x.id for x in obj.mod],
                    duplicatedModExcept('mod id duplicated.'))
    logger.debug('Success validating duplicated \"mod\" items.')

    # Lets get a ordered list of scenarios for each testrun.
    for t in obj.testrun:
        t._attrs['scenarioNameL'] = sorted(glob.glob(t.scenarioPath))
    # Removing testruns not used.
    # Getting them to be able to output for the user.
    notused = [x.id for x in filter(lambda x: not len(x.scenarioNameL), 
                                    obj.testrun)]
    obj.testrun = filter(lambda x: len(x.scenarioNameL), obj.testrun)
    for item in notused:
        logger.debug('testrun:\"%s\" not applies to any file. ' % item + \
                         'Removed. ' + \
                         '(Not parsing the rest its attributes either)')

    # Getting a set of all the used scenarios
    ssList = []
    for t in obj.testrun:
        for item in t.scenarioNameL:
            logger.debug('testrun:\"%s\" applies to scenario:\"%s\"' % \
                             (t.id, item))
        # End of for.
        ssList.append(t.scenarioNameL)
    # Adding the set of the scenarios to the configuration.
    obj._attrs['ssList'] = ssList
    obj._attrs['ssSet'] = sets.Set(flat(ssList))

    # If none scenario applies, just exit.
    if not len(ssList):
        msg = 'Testruns are empty, none scenarios found'
        raise testrunsEmptyExcept(msg)
    
    # Let's validate the length of the tas list, the scenarios 
    # we want to run at once and the execMode.
    obj._attrs['tasN'] = reduce(lambda x,y: x + int(y.jobs), obj.tas, 0)
    conds = {'serial' : max(len(x) for x in ssList),
             'parallel' : sum(len(x) for x in ssList)}
    if obj.tasN < conds[obj.advanced.execMode]:
        msg = 'Wanted to run at least \"%s\" ' % conds[obj.advanced.execMode]
        msg += 'scenarios at the same time, but we have just \"%s\" ' % obj.tasN
        msg += 'tas available. execMode used is \"%s\".' % obj.advanced.execMode
        raise notEnoughTasExcept(msg)
    logger.debug('Success validating testruns and size of the tas pool. ' + \
                  'available tas:\"%s\", needed tas:\"%s\".' % \
                  (obj.tasN, conds[obj.advanced.execMode]))

    # Validating well formed XML scenarios. scenarioValidate
    if str2bool(obj.advanced.scenarioValidate):
        for s in obj.ssSet:
            try:
                lxml.etree.parse(s)
            except Exception, err:
                raise scenarioValidateExcept \
                    ('Bad XML validation of scenario:\"%s\". %s' % (s, err))
            else:
                logger.debug('Success while XML parsing scenario:\"%s\"' % s)

    # Checking config defined and used.
    notused = checkDefinedUsed([x.id for x in obj.config],
                               [x.configlink for x in obj.testrun],
                               configNotDefined('Found configs not defined'))
    logger.debug('Success validating \"config\"s used & defined.')
    # Removing the configs not used.
    obj.config = filter(lambda x: x.id not in notused, obj.config)
    for item in notused:
        logger.debug('config:\"%s\" not used. Removed.' % item)

    # Checking mod defined and used. Making sure modlink exists.
    notused = checkDefinedUsed([x.id for x in obj.mod],
                               [x.modlink for x in obj.testrun if x.modlink],
                               modNotDefined('Found mods not defined'))
    logger.debug('Success validating \"mod\"s used & defined.')
    # Removing the configs not used.
    obj.mod = filter(lambda x: x.id not in notused, obj.mod)
    for item in notused:
        logger.debug('mod:\"%s\" not used. Removed.' % item)

    # iSet will be a set of all injection files
    iSet = sets.Set([])
    for t in obj.mod:
        if t.injection:
            for i in t.injection:
                iSet.add(i.path)
    # Adding the set of injection files to the configuration.
    obj._attrs['iSet'] = iSet
    
    # Checking that all the injection files given exists.
    for i in iSet:
        if not os.path.isfile(i):
            raise injectionFileNotExists('Mod uses an injection file which ' + 
                                         'doesn\'t exist. path:\"%s\", ' % i)
        else: logger.debug('Success checking injection file:\"%s\"' % i)

    # Validating well formed regexs. regexValidate
    if str2bool(obj.advanced.regexValidate):
        # Getting the set with regexs of the mods.
        tmp = sets.Set([])
        for m in obj.mod:
            if m.injection is not None:
                tmp.update([a.regex for a in m.injection])
            if m.replace is not None:
                tmp.update([a.regex for a in m.replace])
        # Trying to compile every regex defined.
        for r in tmp:
            try:
                re.compile(r)
            except Exception, err:
                raise regexValidateExcept('Bad regex:regex:\"%s\". %s' % \
                                              (r, err))
            else:
                logger.debug('Success parsing regex:\"%s\"' % r)
    else:
        logger.debug('No need to validate the regexValidate param.')
