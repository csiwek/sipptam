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
from sipptam.mod.Injection import Injection
from sipptam.mod.Replace import Replace

logger = logging.getLogger(__name__)


class errorAnyScenario(Exception):
    pass

def statsWorker(pd):
    '''
    '''
    while True:
        logger.debug(pd)
        time.sleep(2.0)


def scenarioWorker(sipp, id, batons, triggers, ePowerOff, pd, tasPool):
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

        # Executing SIPp
        logger.debug('Executing sipp')
        ret = tas._runSIPp(sipp)
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

        # TODO. If no new calls success increased in the X seconds (param)
        # flag the call as not success.
        # Regularly check the stats and status of the scenario.
        end = False
        while not end and not ePowerOff.is_set():
            logger.debug('Checking the stats of \"%s\".' % id)
            stats = tas._getStats(pid)
            pd.update(id, stats)
            # If we have fail calls we have to powerOff the others scenarios.
            if (stats['cfail'] > 0):
                logger.info('Found some error calls in this SIPp instance, ' + \
                                'setting the ePowerOff.')
                ePowerOff.set()
            if ((stats['end'] == True) or
                (stats['csuccess'] == stats['ctotal'])):
                end = True

    except Exception, err:
        logger.debug('Error found so we fake eReady and eBatonOff and leave.')
        ePowerOff.set()
        eReady.set()
        if eBatonOff: eBatonOff.set()
        trace = traceback.format_exc()
        logger.debug('Exception:%s traceback:%s' % (err, trace))
        logger.error(err)

    finally:
        try:
            logger.debug('We have to sure this SIPp:\"%s\" is done.' % pid + \
                             ' Also, we need to return the port:\"%s\"' % port)
            powerOff = tas._powerOff(pid)
        except Exception, err:
            trace = traceback.format_exc()
            logger.debug('Exception:%s traceback:%s' % (err, trace))
            logger.error(err)
        logger.debug('Returning tas to the pool. tas:\"%s\"', tas)
        tasPool.append(tas)


def testrunWorker(queue, pd, tasPool, filesCache):
    '''
    '''
    while True:
        addr, testrun, (eReadyG, eRunG, eDoneG) = queue.get()
        
        pause = float(testrun.getConf().getPause())
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
                # Trigs structure will help to sync with others testruns.
                trigsL = [(threading.Event(), eRunG) for _ in testrun]
                # ePowerOff will sync the threads when things go bad.
                ePowerOff = threading.Event()
                thL = []
                for scenario, batons, trigs in zip(testrun, batonsChain, trigsL):
                    # Time to handle the modifications for each of the 
                    # scenarios in the testrun.
                    scenarioContent = filesCache.getFile(scenario)
                    injection, injectionContent, injectionTmp = None, None, None
                    if testrun.has('mod'):
                        for item in testrun.get('mod'):
                            if isinstance(item, Injection):
                                res = item.apply(scenario)
                                if res:
                                    injection = res
                                    injectionTmp = '%s__%s' % \
                                        (testrun.getId(), os.path.basename(injection))
                                    injectionContent = filesCache.getFile(injection)
                            elif isinstance(item, Replace):
                                res  = item.apply(scenario, 
                                                  scenarioContent)
                                if res:
                                    scenarioContent = res
                            else:
                                logger.warning('Mod unknown, discarding it.')
                    scenarioTmp = '%s__%s' % \
                        (testrun.getId(), os.path.basename(scenario))
                    duthost, dutport = addr
                    # We will create the SIPp object with the proper params.
                    sipp = SIPp(r, m, scenarioTmp, scenarioContent, 
                                duthost, dutport, injection=injectionTmp,
                                injectionContent=injectionContent)
                    # Creating threads..
                    n = '%s__%s' % (threading.currentThread().name, scenarioTmp)
                    id = '%s;%s;%s;%s;%s' % (testrun.getId(), t, r, m, scenario)
                    th = threading.Thread(name=n,
                                          target=scenarioWorker,
                                          args=[sipp, id, 
                                                batons, trigs, ePowerOff,
                                                pd, tasPool])
                    th.setDaemon(True)
                    thL.append(th)
                # Lets start the threads
                map(lambda x:x.start(), thL)
                # Wait for all scenarioWorker threads to be ready.
                logger.debug('Waiting for the scenarioWorkers to be ready')
                while not all(map(lambda (x,y) : x.is_set(), trigsL)):
                    time.sleep(0.5)
                # scenarioWorker threads are ready so we are ready. 
                # This will be useful for the first iteration over (tries x r,m)
                # to let the main thread that we are ready to start the testrun.
                logger.debug('scenarioWorkers ready. Setting eReadyG:%s' % eReadyG)
                eReadyG.set()
                # Lets wait them to finish.
                logger.debug('Joining the scenarioWorkers.')
                for th in thL:
                    th.join()
                # Little pause at the end. This will pause also even
                # if this is the last 'try' of the testrun.
                logger.info('Pausing \"%s\"secs between tries.' % pause)
                time.sleep(pause)
        # Setting the finish flag
        eDoneG.set()
