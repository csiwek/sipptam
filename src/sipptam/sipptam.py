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
import threading 
import logging
import Queue
import time

from validate.Validate import Validate
from utils.Utils import fill
from tas.Tas import Tas
from testrun.Testrun import Testrun
from config.Config import Config
from mod.Mod import Mod
from utils.FileManager import FileManager
from mod.Replace import Replace
from mod.Fieldsf import Fieldsf
from utils.Messages import showVersion, showHelp, showInteractiveOut
from thread.Pool import Pool
from thread.Workers import testrunWorker


def main ():
    '''
    Main function.
    '''
    # Defines a logging level and logging format based on a given string key.
    LEVELS = {'debug': (logging.DEBUG,
                        '%(levelname)-7s %(name)-30s %(threadName)-40s' + 
                        ' +%(lineno)-4d' +
                        ' %(message)s'),
              'info': (logging.INFO,
                       '%(levelname)-7s %(message)s'),
              'warning': (logging.WARNING,
                          '%(levelname)-7s %(message)s'),
              'error': (logging.ERROR,
                        '%(levelname)-7s %(message)s'),
              'critical': (logging.CRITICAL,
                           '%(levelname)-7s %(message)s')} 
    
    # Setting some default variables
    _name = 'sipptam'
    _version = '0.1'
    configFilePath = '/etc/sipptam/sipptam.xml'
    loglevel, logformat = LEVELS['info']
    interactive = False
    background = False
    version = False
    help = False
    pauseTasPool = 0.1
    pauseCheckeReady = 1.0
    pauseCheckeDone = 1.0

    # Lets parse input parameters.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:l:ibvh')
        optsLetters = [x for x,y in opts]
        # We must check the valid loglevel first.
        if '-l' in optsLetters:
            if not [y for (x,y) in opts if (x == '-l')][0] in LEVELS.keys():
                raise Exception('Invalid loglevel. Valid loglevels are:\"%s\"' %
                                LEVELS.keys()) 
        # Check modes incompability.
        if '-i' in optsLetters and '-b' in optsLetters:
            raise Exception('Interactive & background mode aren\'t compatible')
    except Exception, msg:
        logging.error(msg)
        showHelp(_name, _version)

    # Looking for command line parameters
    for o, a in opts:
        if o == '-c':
            configFilePath = a
            continue
        elif o == '-l':
            loglevel, logformat = LEVELS[a]
            continue
        elif o == '-i':
            interactive = True
            continue
        elif o == '-b':
            background = True
            continue
        elif o == '-v':
            version = True
            continue
        elif o == '-h':
            help = True
            continue

    # Configuring the log file.
    logging.basicConfig(level=loglevel, format=logformat)
    # Getting the log.
    log = logging.getLogger(__name__)

    # Output the version if the user wants it.
    if version:
        showVersion(_name, _version)

    # Output the help if the user wants it.
    if help: 
        showHelp(_name, _version)

    # Show which configFile are we using
    log.info('Using configFilePath:\"%s\"' % configFilePath)
    # Parsing the configFile file
    try:
        # Parsing configFile. Lexical validation
        configFile = Validate(configFilePath, parse=True)
        configFile.checkSemantics()
    except Exception, err:
        log.error('ConfigFile file error. %s' % str(err))
        showHelp(_name, _version)

    # Reading the files and storing them for future reads.
    scenarioCache = FileManager()
    scenarioCache.addFile(configFile.obj.ssSet)

    # Validation done. Creating objects from the parameters.
    tasPool = Pool(pauseTasPool)
    map(lambda x: tasPool.append(x), fill(Tas, configFile.obj.tas))
    testrunL = fill(Testrun, configFile.obj.testrun)
    configDic = fill(Config, configFile.obj.config, dic = True)
    modDic = fill(Mod, configFile.obj.mod, dic = True)

    # Lets create the proper modification objects
    for m in configFile.obj.mod:
        tmp = {'replaces' : fill(Replace, m.replace),
               'fieldsfs' : fill(Fieldsf, m.fieldsf)}
        m._attrs.update(tmp)

    # Attaching {config, mod} objects in the testruns.
    for t in testrunL:
        # Setting the proper config to the testrun.
        config = configDic[t.get('configlink')]
        t.set('config', config, type(config))
        # Setting the proper mod in the testrun.
        if t.has('modlink'):
            mod = modDic[t.get('modlink')]
            t.set('mod', mod, type(mod))
        # Setting the proper scenarioCache.
        t.set('scenarioCache', scenarioCache, type(scenarioCache))

    # This queue will transmit the testrun jobs to the testrun workers.
    q = Queue.Queue()
    # Adding some events for a fluent comunication with the testrunWorkers.
    # events = [(eReady, eRun, eDone)]
    eRun = threading.Event()
    events = [(threading.Event(), eRun, threading.Event()) 
              for x in range(len(testrunL))]
    if 'serial' == configFile.obj.advanced.execMode:
        n, eventWaitL = 1, [[x] for (x, y, z) in events]
    else: # parallel
        n, eventWaitL = len(testrunL), [[x for (x, y, z) in events]]
    log.debug('events:%s' % events)
    log.debug('eventWaitL:%s' % eventWaitL)
    log.debug('n:%s' % n)

    # Creating and starting threads.
    wthL = [threading.Thread(target=testrunWorker, args=[q,]) for x in range(n)]
    for wth in wthL:
        wth.setDaemon(True)
        wth.start()

    # Feeding the threads with jobs. A job is a testrun and its events.
    map(lambda (x, y): q.put((x, y)), zip(testrunL, events))

    # Lets wait for the threads to be ready and trigger them.
    for evs in eventWaitL:
        while not all(map(lambda x : x.is_set(), evs)):
            log.debug('Waiting for the testrunWorkers to be ready...')
            time.sleep(pauseCheckeReady)
        log.debug('All testrunWorkers are ready.')
        # Checking if the user still wants to run these testruns.
        log.debug('Checking interactive mode, interactive:\"%s\"' % 
                      interactive)
        if interactive:
            var = raw_input("Do you want to proceed? [N/y] ")
            if ('y' != var):
                showInteractiveOut(_name, _version)
            else:
                # Stop annoying.
                interactive = False
        log.debug('Running the testrunWorkers...')
        eRun.set()
        eRun.clear()

    # Waiting for all the eDone events.
    while not all(map(lambda (x,y,z) : z.is_set(), events)):
        log.debug('Waiting for the testrunWorkers to be done...')
        time.sleep(pauseCheckeDone)

    # Time to get the results.
    log.debug('Getting results!')
    log.info('The end!')

if __name__ == '__main__':
    main()
