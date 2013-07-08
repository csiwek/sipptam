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
from utils.Messages import showVersion, showHelp
from tas.TasPool import TasPool
from thread.Workers import testrunWorker, statsWorker
from thread.PDict import PDict


__name__ = 'sipptam'
__version__ = '0.0.9.dev000'


def main ():
    """ Main function """
    # Setting some default variables
    _name = __name__
    _version = __version__
    _id = '%s-%s' % (_name, _version)
    configFilePath = '/usr/local/share/sipptam/sipptam.sample.xml'
    background = False
    version = False
    help = False
    # Some pauses
    pauseTasPool = 0.1
    pauseCheckAlleReady = 1.0
    pauseCheckAlleDone = 1.0

    # Defines a logging level and logging format based on a given string key.
    LEVELS = {'debug': (logging.DEBUG,
                        _id + '%(levelname)-9s %(name)-30s %(threadName)-54s' + 
                        ' +%(lineno)-4d' +
                        ' %(message)s'),
              'info': (logging.INFO,
                       _id + '%(levelname)-9s %(name)-30s %(message)s'),
              'warning': (logging.WARNING,
                          _id + '%(levelname)-9s %(name)-30s %(message)s'),
              'error': (logging.ERROR,
                        _id + '%(levelname)-9s %(name)-30s %(message)s'),
              'critical': (logging.CRITICAL,
                           _id + '%(levelname)-9s %(name)-30s %(message)s')} 
    
    logstr = 'info'
    logFacilityLevel = 0
    loglevel, logformat = LEVELS[logstr]

    # Lets parse input parameters.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:l:s:bvh')
        optsLetters = [x for x,y in opts]
        if '-s' in optsLetters:
            if not int([y for (x,y) in opts if (x == '-s')][0]) in range(0, 9):
                raise Exception('Invalid syslog facility level. Expecting 0-9')
        # We must check the valid loglevel first.
        if '-l' in optsLetters:
            if not [y for (x,y) in opts if (x == '-l')][0] in LEVELS.keys():
                raise Exception('Invalid loglevel. Valid loglevels are:\"%s\"' %
                                LEVELS.keys())
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
            logStr = a
            loglevel, logformat = LOG_ATTR[logStr]
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
    #handlers = [logging.StreamHandler(stream=sys.stdout),
    handlers = [SysLogHandler(address=addr, facility=logFacility)]
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
    fileCache = FileManager()
    fileCache.addFile(configFile.obj.ssSet)
    fileCache.addFile(configFile.obj.iSet)

    # Validation done. Creating objects from the parameters.
    tasPool = TasPool(pauseTasPool)
    map(lambda x: tasPool.append(x), fill(Tas, configFile.obj.tas, 
                                          multiple='jobs'))
    # We need to clean the SIPp instances that are running.
    tasPool.shuffle()
    # We don't want previous SIPp running. TODO.
    testrunL = fill(Testrun, configFile.obj.testrun)
    configDic = fill(Config, configFile.obj.config, dic = True)
    duthost, dutport = configFile.obj.duthost, int(configFile.obj.dutport)
    
    # Lets create the proper modification objects
    modDic = {}
    for m in configFile.obj.mod:
        tmpReplace, tmpInjection = [], []
        if m.replace:
            tmpReplace = fill(Replace, m.replace)
        if m.injection:
            tmpInjection = fill(Injection, m.injection)
        modDic.update({m.id : tmpReplace + tmpInjection})

    # Some debugging.
    logger.debug('tasPool:%s' % tasPool)
    logger.debug('testrunL:%s' % testrunL)
    logger.debug('configDic:%s' % configDic)
    logger.debug('modDic:%s' % modDic)
    logger.debug('fileCache:%s' % fileCache)
    logger.info('Running test against:\"%s:%s\"' % (duthost, dutport))

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
                             args=[q, pd, tasPool, fileCache, ]) 
            for x in range(nTestrunWorker)]
    for wth in wthL:
        wth.setDaemon(True)
        wth.start()

    # This thread will print stats.
    eLeave = threading.Event()
    sth = threading.Thread(target=statsWorker,
                           name='statsThread',
                           args=[pd, eLeave])
    sth.setDaemon(True)
    sth.start()

    # Feeding the threads with jobs using the queue. 
    # A job is a <(duthost, dutport), testrun, events>
    map(lambda (x, y): q.put(((duthost, dutport), x, y)), zip(testrunL, events))

    # Lets wait for the threads to be ready and trigger them.
    for modReady, modRun in zip(modReadyL, modRunL):
        while not all(map(lambda x : x.is_set(), modReady)):
            logger.info('Waiting for the testrunWorkers to be ready...')
            time.sleep(pauseCheckAlleReady)
        logger.debug('All testrunWorkers are ready.')
        logger.debug('Running the testrunWorkers. modRun:\"%s\"' % modRun)
        map(lambda x : x.set(), modRun)

    # Waiting for all the eDone events.
    while not all(map(lambda (x,y,z) : z.is_set(), events)):
        logger.info('Waiting for the testrunWorkers to be done...')
        time.sleep(pauseCheckAlleDone)

    # Time to get the results.
    #logger.debug('Getting results!')
    #logger.info('-' * 60)
    #logger.debug('Results: \n %s' % pd)
    #logger.info('-' * 60)
    eLeave.set()
    sth.join()
    

if __name__ == '__main__':
    main()
