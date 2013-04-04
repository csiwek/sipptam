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
import logging
from pysimplesoap.client import SoapClient

log = logging.getLogger(__name__)
instance = 0

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

    def __str__(self):
        return self.id

    def getId(self):
        return self.id

    def getPort(self):
        response = self.client.getPort(notused=1)
        return response.port

    def runSipp(self, r, m, sf, inf, duthost, dutport, port):
        response = self.client.runSipp(r=r,
                                       m=m,
                                       sf=sf,
                                       inf=inf,
                                       duthost=duthost,
                                       dutport=dutport,
                                       port=port)
        return response.pid

    def hasFinish(self, pid):
        response = self.client.hasFinish(pid=pid)
        return response.ret

    def checkSuccess(self, pid):
        response = self.client.checkSuccess(pid=pid)
        return response.ret

    def checkFail(self, pid):
        response = self.client.checkFail(pid=pid)
        return response.ret

    def cancel(self, pid):
        response = self.client.cancel(pid=pid)
        return response.ret

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
