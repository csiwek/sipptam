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


def testWorker(testrun, events, pd, tasPool):
    '''
    '''
    # Random number in the range [0.0, 1.0)
    pauseGetPort = random.random()
    pauseUpdate = 2 + random.random()

    logger.debug('This worker will handle this testrun:\"%s\"' % testrun)
    tas = tasPool.pop()
    logger.debug('Using this tas:%s' % tas)

    # This will run the scenario, we need some thread order here.
    eBatonOn, eBatonOff = events
    if eBatonOn:
        eBatonOn.wait()
        logger.debug('Baton received, baton:\"%s\"' % eBatonOn)
    else:
        logger.debug('Beginning of the chain.')

    # Asking for a free port
    port = None
    while not port:
        try:
            port = tas.getPort()
            logger.debug('Returned port from tas:%s' % tmp)
        except:
            logger.error('Error while working with tas:%s' % tas)
            time.sleep(pauseGetPort)

    # Running SIPP
    try:
        r = 10
        m = 100
        sf = 'This is a scenario'
        inf = 'this is users file'
        duthost = '192.168.200.200'
        dutport = 5060
        tmp = tas.runSipp(r, m, sf, inf, duthost, dutport, port)
        logger.debug('Returned runSipp:%s from tas:%s' % (tmp, tas))
        logger.debug('type(runSipp):%s' % (type(tmp)))
    except:
        logger.error('Error while working with tas:%s' % tas)

    # Handling off the baton
    if eBatonOff:
        logger.debug('Baton handed off, baton:\"%s\"' % eBatonOff)
        eBatonOff.set()
    else:
        logger.debug('End of the chain.')

    pid = 8798273
    finish = 0
    while not finish:
        try:
            tmp = tas.checkSuccess(pid)
            logger.debug('Returned checkSuccess:%s from tas:%s' % (tmp, tas))

            tmp = tas.checkFail(pid)
            logger.debug('Returned checkFail:%s from tas:%s' % (tmp, tas))

            finish = tas.hasFinish(pid)
            logger.debug('Returned hasFinish:%s from tas:%s' % (finish, tas))
        except:
            logger.error('Error while working with tas:%s' % tas)
        time.sleep(pauseUpdate)
    # This has ended. Returning the tas back to the pool.
    tasPool.append(tas)

def testrunWorker(queue, pd, tasPool):
    '''
    '''
    while True:
        testrun, (eReady, eRun, eDone) = queue.get()
        sleepTime = random.randint(1, 5)
        logger.debug('I\'m sleeping: %s secs' % sleepTime)
        time.sleep(sleepTime)
        logger.debug('I\'m ready!')
        eReady.set()
        eRun.wait()
        thL = []
        eL = [threading.Event() for x in 
              range(len(testrun.get('scenarioNameL')) - 1)]
        eChain = zip([None] + eL, eL + [None])
        logger.debug('eventL:%s' % eL)
        logger.debug('eChain:%s' % eChain)
        for s, es in zip (testrun.get('scenarioNameShortL'), eChain):
            th = threading.Thread(name='%s_%s_%s' % \
                                      (threading.currentThread().name,
                                       testrun.getId(), s), 
                                  target=testWorker,
                                  args=[s, es, pd, tasPool])
            th.setDaemon(True)
            thL.append(th)
        # Lets get them started.
        for t in thL: 
            t.start()
        # Lets wait them to finish.
        for t in thL:
            t.join()
        # Setting the finish flag
        eDone.set()
