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

import sys
import traceback
import threading
import time
import random
import logging
import os
import curses
import texttable

from sipptam.sipp.SIPp import SIPp
from sipptam.mod.Injection import Injection
from sipptam.mod.Replace import Replace

logger = logging.getLogger(__name__)


class callFailExcept(Exception):
    pass

def statsWorker(pd, eLeave):
    '''
    '''
    extra = 2
    dheader = None
    while not dheader:
        tmp = pd.get()
        for key,value in iter(sorted(tmp.iteritems())):
            if value[0]:
                dheader = value[0].keys()
    sheader = ['test-id', 'try', 'r', 'm', 'scenario']
    header =  sheader + dheader
    width = [len(x) + extra for x in header]
    while not eLeave.is_set():
        tab = texttable.Texttable()
        tab.header(header)
        tab.set_cols_width(width)
        tmp = pd.get()
        for key,value in iter(sorted(tmp.iteritems())):
            test, t, r, m, scenario = key.split(';')
            srow = [test, t, r, m, os.path.basename(scenario)]
            drow = []
            if value[0]:
                for keyDynamic in dheader:
                    if value[0].has_key(keyDynamic):
                        drow.append(value[0][keyDynamic])
                    else:
                        drow.append(None)
            else:
                drow = [None for _ in dheader]
            tab.add_row(srow + drow)
        s = tab.draw()
        print s
        time.sleep(0.3)


def scenarioWorker(sipp, id, batons, triggers, ePowerOff, pd, tas):
    '''
    '''
    try:
        # These events will help in the sync with the testrunWorker
        eBatonOn, eBatonOff = batons
        eReady, eRun = triggers

        # Init the pd
        pd.update(id, None)

        # Asking for a free port.
        port = tas.getSIPpBindPort()
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
        # Regularly checking the status and stats of the scenario.
        while not ePowerOff.is_set():
            logger.debug('Checking the stats of \"%s\".' % id)
            try:
                statsTmp = tas._getStats(pid)
                if statsTmp:
                    stats = statsTmp
                try:
                    stats.update({'SIPp\nbinded' : '%s:%s' % (tas.getSIPpBindHost(), 
                                                                tas.getSIPpBindPort())})
                except Exception, err:
                    logger.error('Error adding sipptas to stats. Err:\"%s\"' % err)
                pd.update(id, stats)
                if ((stats['errors'] > 0) or \
                        (stats['cfail'] > 0)):
                    raise callFailExcept('Detected fail calls within scenario.')
                # Scenario will be likely to be successful or it stopped
                # running without any apparent reason.
                if (stats['csuccess'] >= sipp.m):
                    logger.debug('Scenario was success, scenario:\"%s\".' % \
                                     sipp.scenario)
                    break
                if (not stats['running']):
                    logger.debug('Scenario not running anymore, scenario:\"%s\".' % \
                                     sipp.scenario)
                    break
            except callFailExcept:
                logger.debug('Found fail calls, scenario:\"%s\".' % id)
                raise
            except Exception, err:
                logger.debug('Unable to get stats, scenario:\"%s\". Err:\"%s\"' % (id, err))
            finally:
                time.sleep(1)

    except Exception, err:
        # Letting the other scenarioWorkers that is time to leave.
        logger.debug('Error. Setting eReady and ePowerOff.')
        eReady.set()
        ePowerOff.set()
        if eBatonOff: eBatonOff.set()
        trace = traceback.format_exc()
        logger.debug('Exception:%s traceback:%s' % (err, trace))
        logger.error(err)
    finally:
        try:
            logger.debug('We have to make sure SIPp:\"%s\" is done.' % pid + \
                             ' Also, we need to return the port:\"%s\"' % port)
            powerOff = tas._powerOff(pid)
        except Exception, err:
            trace = traceback.format_exc()
            logger.debug('Exception:%s traceback:%s' % (err, trace))
            logger.error(err)
        logger.debug('Returning tas to the pool. tas:\"%s\"', tas)


def testrunWorker(queue, pd, tasPool, filesCache):
    '''
    '''
    while True:
        addr, testrun, (eReadyG, eRunG, eDoneG) = queue.get()
        
        pause = float(testrun.getConf().getPause())
        tries = testrun.getConf().getTries()
        # Lets create the list of tas.
        tasL = [tasPool.pop() for _ in testrun]
        # Asking for a sippBindPort for each of the tas.
        map(lambda x : x._getPort(), tasL)
        # Check if we have any field to replace such as !sipptas(*)!
        # The same testrun object will have the logic to do so.
        # Assumed a drastic and pesimistic solution which is adding the possible
        # combinations of fields as Replaces objects which are going to
        # be applied to all the modifications.
        inputReplacesL = None
        inputReplacesL = []
        for t, n in zip(tasL, range(1, len(tasL) + 1)):
            inputReplacesL.append(Replace(**{'regex' : '(.*)', 
                                             'src' : '!sipptas(host(%s))!' % n, 
                                             'dst' : str(t.getSIPpBindHost())}))
            inputReplacesL.append(Replace(**{'regex' : '(.*)',
                                             'src' : '!sipptas(port(%s))!' % n,
                                             'dst' : str(t.getSIPpBindPort())}))
        if testrun.has('mod'): inputReplacesL.extend(testrun.get('mod'))
        testrun.set('inputmod', inputReplacesL, type(inputReplacesL))
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
                # Thread list
                thL = []
                for scenario, tas, batons, trigs in zip(testrun, tasL, batonsChain, trigsL):
                    # Time to handle the modifications for each of the 
                    # scenarios in the testrun.
                    scenarioContent = filesCache.getFile(scenario)
                    injection, injectionContent, injectionTmp = None, None, None
                    if testrun.has('inputmod'):
                        for item in testrun.get('inputmod'):
                            if isinstance(item, Injection):
                                res = item.apply(scenario)
                                if res:
                                    injection = res
                                    injectionTmp = '%s__%s' % \
                                        (testrun.getId(), os.path.basename(injection))
                                    injectionContent = filesCache.getFile(injection)
                            elif isinstance(item, Replace):
                                scenarioContent  = item.apply(scenario,
                                                              scenarioContent)
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
                                                pd, tas])
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
        # Returning the tas to the pool.
        map(lambda x:tasPool.append(x), tasL)
        # Setting the finish flag
        eDoneG.set()
