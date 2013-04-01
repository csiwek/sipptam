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

log = logging.getLogger(__name__)


def testWorker(testrun, events):
    '''
    '''
    eBatonOn, eBatonOff = events
    if eBatonOn:
        eBatonOn.wait()
        log.debug('Baton received, baton:\"%s\"' % eBatonOn)
    else:
        log.debug('Beginning of the chain.')
    log.debug('Doing my job.')
    #time.sleep(random.randint(2, 5))
    log.debug('Job done.')
    if eBatonOff:
        log.debug('Baton handed off, baton:\"%s\"' % eBatonOff)
        eBatonOff.set()
    else:
        log.debug('End of the chain.')
    log.debug('Now I should check the status of the scenario.')

def testrunWorker(queue):
    '''
    '''
    while True:
        testrun, (eReady, eRun, eDone) = queue.get()
        sleepTime = random.randint(1, 5)
        log.debug('I\'m sleeping: %s secs' % sleepTime)
        time.sleep(sleepTime)
        log.debug('I\'m ready!')
        eReady.set()
        eRun.wait()
        thL = []
        eL = [threading.Event() for x in 
              range(len(testrun.get('scenarioNameL')) - 1)]
        eChain = zip([None] + eL, eL + [None])
        log.debug('eventL:%s' % eL)
        log.debug('eChain:%s' % eChain)
        for s, es in zip (testrun.get('scenarioNameShortL'), eChain):
            th = threading.Thread(name='%s_%s_%s' % \
                                      (threading.currentThread().name,
                                       testrun.getId(), s), 
                                  target=testWorker,
                                  args=[s, es,])
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
