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

import traceback
import threading
import time
import random
import logging
import os

from sipptam.sipp.SIPp import SIPp

logger = logging.getLogger(__name__)


def testWorker(sipp, batons, triggers, pd, tasPool):
    '''
    '''
    try:
        # These events will help in the sync with the testrunWorker
        eBatonOn, eBatonOff = batons
        eReady, eRun = triggers

        # I need a tas to start working with this scenario.
        tas = tasPool.pop()

        # Asking for a free port.
        port = tas._getPort()
        logger.debug('We just got a port:\"%s\"' % port)
        sipp.setBindPort(port)

        # We have a port, we are ready to start.
        logger.debug('I\'m ready to start. I set eReady:%s' % eReady)
        eReady.set()

        # Lets wait until they tell me with the eRun condition.
        logger.debug('I have to wait for the eRun:%s' % eRun)
        eRun.wait()

        # Now we have to wait until I take the baton.
        logger.debug('Waiting for the baton. eBatonOn:%s' % eBatonOn)
        if eBatonOn: eBatonOn.wait()

        # Time to execute the sipp portion.
        logger.debug('Executing sipp')
        ret = tas._runSIPp(sipp)
        if ret.ret:
            'Operation was ok!'
        pid = ret.pid

        # Handling off the baton so next worker can start its scenario.
        # We set a proper pause before handling off the baton, the reason
        # is even If we set the proper order scenarios' execution here,
        # the lag in different tas could be different and they could end
        # up executing in different order. This pause will fight against this.
        logger.debug('Handling off the baton. eBatonOff:%s' % eBatonOff)
        if eBatonOff:
            logger.debug('Pausing a little bit before handling off the baton')
            time.sleep(2)
            eBatonOff.set()

        # TODO. loop
        # Here we have to detect that the test is going success
        # or not, if not, raiseException and finish.
        # Checking when is going to finish
        logger.debug('Waiting until sipp finishes, checking the stats:')
        stats = tas._getStats(pid)
        logger.info('got this success:%s' % stats.success)
        logger.info('got this fail:%s' % stats.fail)
        logger.info('got this total:%s' % stats.total)
        logger.info('got this r:%s' % stats.r)
        logger.info('got this m:%s' % stats.m)

        # TODO
        #if not finish: logger.error('havent finished yet!')
        # TODO
        # turnOff = tas.turnOff(pid)
        # tas.returnPort !!!
        # This has ended. Returning the tas back to the pool.
    except Exception, err:
        trace = traceback.format_exc()
        logger.debug('Exception:%s traceback:%s' % (err, trace))
        logger.error(err)
        logger.debug('Error found so we fake eReady and eBatonOff and leave.')
        eReady.set()
        if eBatonOff: eBatonOff.set()
    finally:
        logger.debug('Returning tas to the pool. tas:\"%s\"', tas)
        tasPool.append(tas)


def testrunWorker(queue, pd, tasPool, scenarioCache):
    '''
    '''
    while True:
        addr, testrun, (eReadyG, eRunG, eDoneG) = queue.get()
        
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
                for scenario, batons, trigs in zip(testrun, batonsChain, trigsL):
                    # TODO. Modifications.
                    scenarioContent = scenarioCache.getFile(scenario)
                    injection, injectionContent = None, None
                    #if testrun.has('mod'):
                        #scenarioContent, injection  = \
                        #    testrun.get('mod').apply(scenario, scenarioContent)
                        #if injection:
                        #    injectionContent = scenarioCache.getFile(injection)
                    scenarioTmp = '%s__%s' % \
                        (testrun.getId(), os.path.basename(scenario))
                    duthost, dutport = addr
                    sipp = SIPp(r, m, scenarioTmp, scenarioContent, 
                                duthost, dutport, 
                                injection=injection, injectionContent=injectionContent)
                    # Creating threads.                    
                    n = '%s__%s' % (threading.currentThread().name, scenarioTmp)
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
                logger.debug('testworkers are ready. We set eReadyG:%s' % 
                             eReadyG)
                eReadyG.set()
                # Lets wait them to finish.
                for th in thL:
                    th.join()
        # Setting the finish flag
        eDoneG.set()
