#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.thread.workers.py

This module implements different thread workers.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''

import threading
import time
import random
import logging
import os
import traceback

from sipptam.sipp.SIPp import SIPp

logger = logging.getLogger(__name__)


def perform(fun, args, max=5, pause=0.1):
    '''
    Just a DRY helper function which executes a function @max 
    times with a pause of @pause in between when they fail.
    '''
    ret, tries, funNa = None, 0, fun.__name__
    while not ret and tries < max:
        try:
            ret = fun(**args)
            logger.debug('This fun:\"%s\" returned:\"%s\"' % (funNa, ret))
        except Exception, err:
            trace = traceback.format_exc()
            logger.warning('This fun:\"%s\" didn\'t return anything' % (funNa))
            logger.error('Excepton catched. %s. traceback:%s' % (err, trace))
            time.sleep(pause)
    return ret


def testWorker(sipp, batons, triggers, pd, tasPool):
    '''
    '''
    # I need a tas to start working with this scenario.
    tas = tasPool.pop()
    eBatonOn, eBatonOff = batons
    eReady, eRun = triggers
    # Asking for a free port
    port = perform(tas.getPort, {})
    sipp.setBindPort(port)
    # We are ready to start
    logger.debug('We just got a port and I ready to start. I set eReady.')
    eReady.set()
    # Lets wait until they tell me.
    logger.debug('I have to wait for the eRun condition')
    eRun.wait()
    # Now we have to wait until I take the batonOn.
    logger.debug('Waiting for the batonOn')
    if eBatonOn: eBatonOn.wait()
    # Time to send the sipp to the tas and execute it.
    logger.debug('Executing sipp')
    pid = perform(tas.runSipp, {'sipp' : sipp})
    if not pid: logger.error('Error while running SIPp')
    # Handling off the baton so next worker can start its scenario.
    logger.debug('Passing the baton to the next one')
    if eBatonOff: eBatonOff.set()
    # Checking when is going to finish
    logger.debug('Waiting untill sipp finishes, max=500, pause=1')
    finish = perform(tas.hasFinish, {'pid' : pid}, max=500, pause=1)
    if not finish: logger.error('havent finished yet!')
    # TODO
    #turnOff = perform(tas.turnOff, pid)
    #perform(tas.returnPort!)
    # This has ended. Returning the tas back to the pool.
    tasPool.append(tas)


def testrunWorker(queue, pd, tasPool, scenarioCache):
    '''
    '''
    while True:
        testrun, (eReadyG, eRunG, eDoneG) = queue.get()
        
        pause = testrun.getConf().getPause()
        tries = testrun.getConf().getTries()

        # Going through the tries and all the {ratio, max} values.
        for t in range(tries):
            for r, m in testrun.getConf():
                logger.debug('Starting try:\"%s\" with r:\"%s\", m:\"%s\"' % \
                                 (t, r, m))
                # Creating the batons.
                # The batons concept makes the sync between different
                # threads of the same testrun possible. Remember,
                # when using SIPp, we need to make sure the scenarios are
                # ran in an specific order.
                tmp = [threading.Event() for _ in testrun][:-1]
                batonsChain = zip([None] + tmp, tmp + [None])
                # Trigs will help to sync with others testruns.
                trigsL = [(threading.Event(), eRunG) for _ in testrun]
                thL = []
                for sf, batons, trigs in zip(testrun, batonsChain, trigsL):
                    # TODO. Modifications.
                    sfcontent = scenarioCache.getFile(sf)
                    sfTmp = '%s__%s' % (testrun.getId(), os.path.basename(sf))
                    duthost, dutport = '192.168.2.1', 5060 # TODO
                    sipp = SIPp(r, m, sfTmp, sfcontent, duthost, dutport)
                    # Creating threads.                    
                    n = '%s__%s' % (threading.currentThread().name, sfTmp)
                    th = threading.Thread(name=n,
                                          target=testWorker,
                                          args=[sipp, batons, trigs,
                                                pd, tasPool])
                    th.setDaemon(True)
                    thL.append(th)
                # Lets start the threads
                map(lambda x:x.start(), thL)
                # Wait for all testworker threads to be ready.
                logger.debug('Waiting for the testworkers to be ready')
                while not all(map(lambda (x,y) : x.is_set(), trigsL)):
                    time.sleep(0.5)
                # testworker threads are ready so we are ready. 
                # This will be useful for the first iteration over (tries x r,m)
                # to let the main thread that we are ready to start the testrun.
                logger.debug('Looks like testworkers are ready. We set eReadyG')
                logger.debug(eRunG)
                logger.debug(eRunG.isSet())
                eReadyG.set()
                # Lets wait them to finish.
                for th in thL:
                    th.join()
        # Setting the finish flag
        eDoneG.set()
