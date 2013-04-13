#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.thread.PDict.py

This module implements a shared resource to store the result.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''
import threading
import datetime
import logging
import copy

logger = logging.getLogger(__name__)


class PDict(object):
    '''
    PDict stands for protected dictionary.
    '''
    def __init__(self):
        '''
        '''
        self.dict = {}
        self.lock = threading.Lock()
        
    def __len__(self):
        '''
        '''
        return len(self.dict)

    def __str__(self):
        '''
        '''
        with self.lock:
            tmp = ['\n']
            for key, value in sorted(self.dict.iteritems()):
                tmp.append('%s  -->  %s' % (key, value))
            return "\n".join(tmp)
        
    def has(self, item):
        '''
        '''
        with self.lock:
            return key in self.dict

    def add(self, key, item):
        '''
        Adds an elem to the dict.
        Last result to enter will be the default result.
        '''
        with self.lock:
            self.dict[key] = item

    def get(self, key):
        '''
        Gets the value of an element of the dict.
        '''
        with self.lock:
            return copy.copy(self.dict[key])

    def update(self, key, value):
        with self.lock:
            self.dict[key] = [value]
