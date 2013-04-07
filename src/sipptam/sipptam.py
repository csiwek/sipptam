#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.sipptam
    ~~~~~~~~~~~~~~~

    Main sipptam module.

    :copyright: (c) 2013 INdigital Telecom. luismartingil.
    :license: See LICENSE_FILE.
"""

import traceback
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
from mod.Injection import Injection
from utils.Messages import showVersion, showHelp, showInteractiveOut
from tas.TasPool import TasPool
from thread.Workers import testrunWorker
from thread.PDict import PDict


def main ():
    '''
    Main function.
    '''
    # Defines a logging level and logging format based on a given string key.
    LEVELS = {'debug': (logging.DEBUG,
                        '%(levelname)-9s %(name)-30s %(threadName)-54s' + 
                        ' +%(lineno)-4d' +
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
        trace = traceback.format_exc()
        logger.debug('Exception:%s traceback:%s' % (err, trace))
        logger.error('ConfigFile file error. %s' % str(err))
        showHelp(_name, _version)

    # Reading the files and storing them for future reads.
    scenarioCache = FileManager()
    scenarioCache.addFile(configFile.obj.ssSet)
    scenarioCache.addFile(configFile.obj.iSet)

    # Validation done. Creating objects from the parameters.
    tasPool = TasPool(pauseTasPool)
    map(lambda x: tasPool.append(x), fill(Tas, configFile.obj.tas, 
                                          multiple='jobs'))
    # We need to clean the SIPp instances that are running.
    tasPool.shuffle()
    # We don't want previous SIPp running.
    # TODO.

    testrunL = fill(Testrun, configFile.obj.testrun)
    configDic = fill(Config, configFile.obj.config, dic = True)
    modDic = fill(Mod, configFile.obj.mod, dic = True)
    duthost, dutport = configFile.obj.duthost, int(configFile.obj.dutport)

    # Some debugging.
    logger.debug('tasPool:%s' % tasPool)
    logger.debug('testrunL:%s' % testrunL)
    logger.debug('configDic:%s' % configDic)
    logger.debug('modDic:%s' % modDic)
    logger.info('Running test against:\"%s:%s\"' % (duthost, dutport))

    # Lets create the proper modification objects
    for m in configFile.obj.mod:
        tmp = {'replaces' : fill(Replace, m.replace),
               'injections' : fill(Injection, m.injection)}
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
    if 'serial' == configFile.obj.advanced.execMode:
        eReadyL = [threading.Event() for _ in testrunL]
        eRunL = [threading.Event() for _ in testrunL]
        eDoneL = [threading.Event() for _ in testrunL]
        nTestrunWorker = 1
        modReadyL = [[x] for (x) in eReadyL]
        modRunL = [[x] for (x) in eRunL]
    else:
        eReadyL = [threading.Event() for _ in testrunL]
        tmp = threading.Event()
        eRunL = [tmp for _ in testrunL]
        eDoneL = [threading.Event() for _ in testrunL]
        nTestrunWorker = len(testrunL)
        modReadyL = [eReadyL]
        modRunL = [eRunL]

    # Events will passed as part of the jobs.
    events = zip(eReadyL, eRunL, eDoneL)

    # Creating and starting testrunWorker threads.
    wthL = [threading.Thread(target=testrunWorker, 
                             args=[q, pd, tasPool, scenarioCache, ]) 
            for x in range(nTestrunWorker)]
    for wth in wthL:
        wth.setDaemon(True)
        wth.start()

    # Feeding the threads with jobs using the queue. 
    # A job is a <(duthost, dutport), testrun, events>
    map(lambda (x, y): q.put(((duthost, dutport), x, y)), zip(testrunL, events))

    # Lets wait for the threads to be ready and trigger them.
    for modReady, modRun in zip(modReadyL, modRunL):
        while not all(map(lambda x : x.is_set(), modReady)):
            logger.info('Waiting for the testrunWorkers to be ready...')
            time.sleep(pauseCheckAlleReady)
        logger.debug('All testrunWorkers are ready.')
        # Checking if the user still wants to run these testruns.
        logger.debug('Checking interactive mode, interactive:\"%s\"' % 
                      interactive)
        if interactive:
            var = raw_input("Do you want to proceed? [N/y] ")
            if ('y' != var):
                # TODO. Save results
                showInteractiveOut(_name, _version)
        logger.debug('Running the testrunWorkers. modRun:\"%s\"' % modRun)
        map(lambda x : x.set(), modRun)

    # Waiting for all the eDone events.
    while not all(map(lambda (x,y,z) : z.is_set(), events)):
        logger.info('Waiting for the testrunWorkers to be done...')
        time.sleep(pauseCheckAlleDone)

    # Time to get the results.
    logger.debug('Getting results!')
    logger.info('The end!')

if __name__ == '__main__':
    main()
