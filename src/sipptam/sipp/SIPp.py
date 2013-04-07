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
    scenarioPath, scenario, scenarioContent = None, None, None
    duthost, dutport = None, None
    port = None
    injectionPath, injection, injectionContent = None, None, None
    trace_err = None
    
    def __init__(self, r, m, scenario, scenarioContent, duthost, dutport, 
                 port=5060, injection=None, injectionContent=None,
                 sipp='sipp', trace_err=False):
        self.r = r
        self.m = m
        self.scenario = scenario
        self.scenarioContent = scenarioContent
        self.scenarioPath = os.path.join('/tmp/', scenario)
        self.duthost = duthost
        self.dutport = dutport
        self.port = port
        self.sipp  = sipp
        if injection: self.injectionPath = os.path.join('/tmp/', injection)
        self.injection = injection
        self.injectionContent = injectionContent
        if trace_err: self.trace_err

    def __str__(self):
        cmd = []
        cmd.append(self.sipp)
        cmd.append('-sf %s' % self.scenarioPath)
        if self.injection: cmd.append('-inf %s' % self.injection)
        cmd.append('%s:%s' % (self.duthost, self.dutport))
        if self.port: cmd.append('-p %s' % self.port)
        cmd.append('-r %s' % self.r)
        cmd.append('-m %s' % self.m)
        if self.trace_err: cmd.append('-trace_err')
        return ' '.join(cmd)

    def createScenario(self):
        with open(self.scenarioPath, 'w') as f:
            f.write(self.scenarioContent)

    def createInjection(self):
        if self.injection is not None:
            with open(self.injectionPath, 'w') as f:
                f.write(self.injectionContent)

    def getBindedPort(self):
        return self.port

    def setBindPort(self, port):
        self.port = port
