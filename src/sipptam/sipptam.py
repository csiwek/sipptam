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
from logging.handlers import SysLogHandler
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
from thread.PDict import PDict


def main ():
    '''
    Main function.
    '''
    # Defines a logging level and logging format based on a given string key.
    LEVELS = {'debug': (logging.DEBUG,
                        '%(levelname)-9s %(name)-30s %(threadName)-40s' + 
#                        ' +%(lineno)-4d' +
                        ' %(message)s'),
              'info': (logging.INFO,
                       '%(levelname)-9s %(name)-30s %(message)s'),
              'warning': (logging.WARNING,
                          '%(levelname)-9s %(name)-30s %(message)s'),
              'error': (logging.ERROR,
                        '%(levelname)-9s %(name)-30s %(message)s'),
              'critical': (logging.CRITICAL,
                           '%(levelname)-9s %(name)-30s %(message)s')} 
    
    # Setting some default variables
    _name = 'sipptam'
    _version = '0.1'
    configFilePath = '/usr/local/share/sipptam/sipptam.sample.xml'
    loglevel, logformat = LEVELS['info']
    logFacilityLevel = 0
    interactive = False
    background = False
    version = False
    help = False
    pauseTasPool = 0.1
    pauseCheckAlleReady = 1.0
    pauseCheckAlleDone = 1.0

    # Lets parse input parameters.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:l:s:ibvh')
        optsLetters = [x for x,y in opts]
        if '-s' in optsLetters:
            if not int([y for (x,y) in opts if (x == '-s')][0]) in range(0, 9):
                raise Exception('Invalid syslog facility level. Expecting 0-9')
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
        elif o == '-s':
            logFacilityLevel = a
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

    # Configuring the log file. We will log both stdout and syslog.
    # Depending on the platform we use diferent syslog.
    if sys.platform == "darwin": addr = '/var/run/syslog'
    else: addr = '/dev/log'
    logger = logging.getLogger()
    logger.setLevel(loglevel)
    logger.handlers = [] # Clearing previous logs
    formatter = logging.Formatter(logformat)
    logFacility = 'local%s' % logFacilityLevel
    handlers = [logging.StreamHandler(stream=sys.stdout),
                SysLogHandler(address=addr, facility=logFacility)]
    for h in handlers:
        h.setFormatter(formatter)
        logger.addHandler(h)
    # Getting a basic log
    logger = logging.getLogger(__name__)

    # Output the version if the user wants it.
    if version:
        showVersion(_name, _version)

    # Output the help if the user wants it.
    if help: 
        showHelp(_name, _version)

    # Show which configFile are we using
    logger.info('Using configFilePath:\"%s\"' % configFilePath)
    # Parsing the configFile file
    try:
        # Parsing configFile. Lexical validation
        configFile = Validate(configFilePath, parse=True)
        configFile.checkSemantics()
    except Exception, err:
        logger.error('ConfigFile file error. %s' % str(err))
        showHelp(_name, _version)

    # Reading the files and storing them for future reads.
    scenarioCache = FileManager()
    scenarioCache.addFile(configFile.obj.ssSet)

    # Validation done. Creating objects from the parameters.
    tasPool = Pool(pauseTasPool)
    map(lambda x: tasPool.append(x), fill(Tas, configFile.obj.tas, 
                                          multiple='jobs'))
    tasPool.shuffle()
    testrunL = fill(Testrun, configFile.obj.testrun)
    configDic = fill(Config, configFile.obj.config, dic = True)
    modDic = fill(Mod, configFile.obj.mod, dic = True)

    # Some debugging.
    logger.debug('tasPool:%s' % tasPool)
    logger.debug('testrunL:%s' % testrunL)
    logger.debug('configDic:%s' % configDic)
    logger.debug('modDic:%s' % modDic)

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

    # This queue will transmit the testrun jobs to the testrun workers.
    q = Queue.Queue()
    # The protected dict will hold the results.
    pd = PDict()
    # Adding some events for a fluent comunication with the testrunWorkers.
    # events = [(eReady, eRun, eDone)]
    eRun = threading.Event()
    events = [(threading.Event(), eRun, threading.Event()) 
              for x in range(len(testrunL))]
    if 'serial' == configFile.obj.advanced.execMode:
        nTestrunWorker, eventWaitL = 1, [[x] for (x, y, z) in events]
    else: # parallel
        nTestrunWorker, eventWaitL = len(testrunL), [[x for (x, y, z) in events]]
    logger.debug('nTestrunWorker:\"%s\", events:\"%s\", eventWaitL:\"%s\"' % 
                 (nTestrunWorker, events, eventWaitL))

    # Creating and starting testrunWorker threads.
    wthL = [threading.Thread(target=testrunWorker, 
                             args=[q, pd, tasPool, scenarioCache, ]) 
            for x in range(nTestrunWorker)]
    for wth in wthL:
        wth.setDaemon(True)
        wth.start()

    # Feeding the threads with jobs. A job is a testrun and its events.
    map(lambda (x, y): q.put((x, y)), zip(testrunL, events))

    # Lets wait for the threads to be ready and trigger them.
    for evs in eventWaitL:
        while not all(map(lambda x : x.is_set(), evs)):
            logger.debug('Waiting for the testrunWorkers to be ready...')
            time.sleep(pauseCheckAlleReady)
        logger.debug('All testrunWorkers are ready.')
        # Checking if the user still wants to run these testruns.
        logger.debug('Checking interactive mode, interactive:\"%s\"' % 
                      interactive)
        if interactive:
            var = raw_input("Do you want to proceed? [N/y] ")
            if ('y' != var):
                showInteractiveOut(_name, _version)
            else:
                # Stop annoying.
                interactive = False
        logger.debug('Running the testrunWorkers...')
        eRun.set()

    # Waiting for all the eDone events.
    while not all(map(lambda (x,y,z) : z.is_set(), events)):
        logger.debug('Waiting for the testrunWorkers to be done...')
        time.sleep(pauseCheckAlleDone)

    # Time to get the results.
    logger.debug('Getting results!')
    logger.info('The end!')

if __name__ == '__main__':
    main()
