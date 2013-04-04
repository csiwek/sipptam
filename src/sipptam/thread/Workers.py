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
            logger.warning('This fun:\"%s\" didn\'t return anything' % (funNa))
            logger.error(err)
            time.sleep(pause)
    return ret


def testWorker(testrun, batons, triggers, pd, tasPool):
    '''
    '''
    eBatonOn, eBatonOff = batons
    eReady, eRun = triggers

    # I need a tas to start working with this scenario.
    tas = tasPool.pop()
    logger.debug('I will handle this testrun:\"%s\" using this tas:\"%s\"' % 
                 (testrun, tas))

    # Asking for a free port
    port = perform(tas.getPort, {})

    # We are ready to start
    eReady.set()

    # Lets wait until they tell me.
    eRun.wait()

    # Now we have to wait until the batonOn is given to us.
    if eBatonOn: eBatonOn.wait()

    # Some example of params. TODO.
    args = {'r' : 10, 'm' : 100, 
            'sf' : 'scenario file' * 100, 'inf' : 'users file', 
            'duthost' : '192.168.200.222', 'dutport' : 5060,
            'port' : port}
    pid = perform(tas.runSipp, args)
    if not pid: logger.error('Error while running SIPp')

    # Handling off the baton so next worker can start its scenario.
    if eBatonOff: eBatonOff.set()
    
    # Checking when is going to finish
    finish = perform(tas.hasFinish, {'pid' : pid}, max=500, pause=1)
    if not finish: logger.error('havent finished yet!')

    # TODO
    #turnOff = perform(tas.turnOff, pid)
    #perform(tas.returnPort!)

    # This has ended. Returning the tas back to the pool.
    tasPool.append(tas)

def testrunWorker(queue, pd, tasPool):
    '''
    '''
    # Triggers will help to sync with others testruns.
    while True:
        testrun, (eReadyG, eRunG, eDoneG) = queue.get()

        # Triggers
        triggersL = [(threading.Event(), eRunG) for x in range(len(testrun))]
        # Creating the batons.
        # The batons concept makes the sync between different
        # threads of the same testrun possible. Remember that using SIPp, 
        # we need to have the scenarios be ran with some order.
        tmp = [threading.Event() for x in range(len(testrun) - 1)]
        batonsChain = zip([None] + tmp, tmp + [None])

        # Wrapping up the parameters.
        params = zip (testrun.get('scenarioNameShortL'), 
                      batonsChain,
                      triggersL)

        # Creating threads.
        thL = []
        for scenario, batons, triggers  in params:
            n = '%s_%s_%s' % (threading.currentThread().name, 
                              testrun.getId(), 
                              scenario)
            th = threading.Thread(name=n,
                                  target=testWorker,
                                  args=[scenario, batons, triggers,
                                        pd, tasPool])
            th.setDaemon(True)
            th.start()
            thL.append(th)

        # Wait for all testworker threads to be ready.
        while not all(map(lambda (x,y) : x.is_set(), triggersL)):
            time.sleep(1)

        # testworker threads are ready so we are ready.
        eReadyG.set()

        # Lets wait them to finish.
        for t in thL:
            t.join()
        # Setting the finish flag
        eDoneG.set()
