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


class noReturnExcept(Exception):
    pass

def perform(fun, args, max=5, pause=0.1, funNa=None, alarm=True):
    '''
    Just a DRY helper function which executes a function @max 
    times with a pause of @pause in between when they fail.
    @funNa if we want to set a friendly function's name for debugging.
    '''
    logger.debug('Performing fun:\"%s\" args:\"%s\"' % (funNa, args))
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
    if alarm and not ret:
        msg = 'This fun:%s didn\'t return anything (tries:%s)' % (funNa, tries)
        raise noReturnExcept(msg)
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
    

#     def runSipp(self, sipp):
#         r = sipp.r
#         m = sipp.m
#         sf = sipp.sf
#         sfcontent = sipp.sfcontent
#         inf = sipp.inf
#         duthost = sipp.duthost
#         dutport = sipp.dutport
#         port = sipp.port
#         response = self.client.runSipp(r=r,
#                                        m=m,
#                                        sf=sf,
#                                        sfcontent=sfcontent,
#                                        inf=inf,
#                                        duthost=duthost,
#                                        dutport=dutport,
#                                        port=port)
#         #perform(response.pid)


    def _getPort(self):
        response = perform(self.client.getPort, {'nu' : 0}, funNa='getPort')
        return response.port

    def _runSIPp(self, sipp):
        #response = perform(self.client.runSIPp, **sipp, funNa='runSIPp')
        #return response.pid
        pass
    
    def _getStats(self, pid):
        response = perform(self.client.getStats, {'pid' : pid}, funNa='getStats')
        return response.ret
     

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
