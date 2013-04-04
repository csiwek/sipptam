#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptas.sipp.SIPp.py

This module represents a SIPp instance.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''

import logging
import os

log = logging.getLogger(__name__)

class SIPp(object):
    r, m = None, None
    sfpath, sf, sfcontent = None, None, None
    duthost, dutport = None, None
    port = None
    inf = None
    trace_err = None
    
    def __init__(self, r, m, sf, sfcontent, duthost, dutport, 
                 port=None, inf=None, trace_err=False):
        self.r = r
        self.m = m
        self.sf = sf
        self.sfcontent = sfcontent
        self.sfpath = os.path.join('/tmp/', sf)
        self.duthost = duthost
        self.dutport = dutport
        if port: self.port = port
        if inf: self.inf = inf
        if trace_err: self.trace_err

    def __str__(self):
        cmd = []
        cmd.append('sipp')
        cmd.append('-sf %s' % self.sfpath)
        cmd.append('-inf %s' % self.inf)
        cmd.append('%s:%s' % (self.duthost, self.dutport))
        if self.port: cmd.append('-p %s' % self.port)
        cmd.append('-r %s' % self.r)
        cmd.append('-m %s' % self.m)
        if self.trace_err: cmd.append('-trace_err')
        return ' '.join(cmd)

    def createScenario(self):
        with open(self.sfpath, 'w') as f:
            f.write(self.sfcontent)

    def getBindedPort(self):
        return self.port

    def setBindPort(self, port):
        self.port = port
