#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.tas.Tas.py

Object which represents a the Test Automation Slave.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''
import time
import logging
from pysimplesoap.client import SoapClient

logger = logging.getLogger(__name__)
instance = 0


class operationFailed(Exception):
    pass

class noReturnExcept(Exception):
    pass


def call(fun, args, max=5, pause=0.1, funNa=None, alarm=True):
    '''
    Just a DRY helper function which executes a function @max 
    times with a pause of @pause in between when they fail.
    @funNa if we want to set a friendly function's name for debugging.
    '''
    #logger.debug('Calling fun:\"%s\" args:\"%s\"' % (funNa, args))
    if not funNa: funNa = fun.__name__
    ret, tries = None, 0
    while not ret and tries < max:
        try:
            ret = fun(**args)
            logger.debug('This fun:\"%s\" returned:\"%s\"' % (funNa, ret))
        except Exception, err:
            tries += 1
            logger.warning('This fun:\"%s\" didn\'t return anything' % (funNa))
            time.sleep(pause)
    if alarm:
        if not ret:
            msg = 'This fun:%s didn\'t return anything (tries:%s)' % (funNa, tries)
            raise noReturnExcept(msg)
        if not ret.ret:
            raise operationFailed('Operation returned an error code:%s' % funNa)
    return ret


class Tas(object):
    host, port, jobs = None, None, None
    id = None

    def __init__(self, **kwargs):
        global instance
        instance += 1
        self.id   = '%s_%s_%s' % (instance, 
                                  kwargs['host'],
                                  kwargs['port'])
        s = 'http://%s:%s/' % (kwargs['host'], kwargs['port'])
        self.client = SoapClient(location = s,
                                 action = s, 
                                 namespace = s, 
                                 soap_ns='soap',
                                 trace = False,
                                 ns = False,
                                 exceptions = False)
        self.tasHost = kwargs['host']
        self.tasPort = kwargs['port']

    def __str__(self):
        return self.id

    def getId(self):
        return self.id

    def getTasHost(self):
        return self.tasHost

    def getTasPort(self):
        return self.tasPort

    def _getPort(self):
        response = call(self.client.getPort, {'nu' : 0}, funNa='getPort')
        return response.port

    def _runSIPp(self, sipp):
        args = {'r' : sipp.r,
                'm' : sipp.m,
                'scenario' : sipp.scenario,
                'scenarioContent' : sipp.scenarioContent,
                'injection' : sipp.injection,
                'injectionContent' : sipp.injectionContent,
                'duthost' : sipp.duthost,
                'dutport' : sipp.dutport,
                'port' : sipp.port}
        response = call(self.client.runSIPp, args, funNa="runSIPp")
        return response.ret
    
    def _getStats(self, pid, scenario):
        response = call(self.client.getStats, 
                        {'pid' : pid, 'scenario' : scenario}, 
                        funNa='getStats')
        ret = {'start' : int(response.ret.start),
               'elapsed' : int(response.ret.elapsed),
               'csuccess' : int(response.ret.csuccess),
               'cfail' : int(response.ret.cfail),
               'ctotal' : int(response.ret.ctotal),
               'r' : int(response.ret.r),
               'm' : int(response.ret.m),
               'end' : bool(response.ret.end)}
        return ret

    def _powerOff(self, pid, port):
        response = call(self.client.powerOff, 
                        {'pid' : pid, 'port' : port},
                        funNa='powerOff')
        return response.ret

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
