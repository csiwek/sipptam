#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.thread.Pool.py

This module implements the Pool class.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''
import traceback
import threading
import random
import time
import logging

log = logging.getLogger(__name__)


class Pool(object):
    '''
    Represents a pool.
    '''
    pause = None
    items = None
    lock = None
    def __init__(self, pause):
        '''
        '''
        self.pause = pause
        self.items = []
        self.lock = threading.Lock()
        
    def __len__(self):
        '''
        '''
        return len(self.items)

    def __str__(self):
        '''
        '''
        ret = []
        with self.lock:
            map(lambda x: ret.append(str(x)), self.items)
        return "\n".join(ret)
   
    def append(self, item):
        '''
        Adds an item to the first place of the pool.
        '''
        if hasattr(item, 'getId') and callable(getattr(item, 'getId')):
            with self.lock:
                self.items.insert(0, item)
        else:
            raise Exception('Trying to add an item with no getId method.')

    def pop(self):
        '''
        Pops the last item.
        '''
        with self.lock:
            item = self.items.pop()
        return item

    def remove(self, id):
        '''
        Removes the link with id 'id' from the pool.
        PRE. the pool must have a link with id 'id' or another thread has 
        that link and will return it to the pool in the future.
        PRE. Items have an 'getId' operation.
        '''
        removed = threading.local()
        removed = False
        while (not removed):
            with self.lock:
                try:
                    log.debug('trying to remove the link:%s' % (id))
                    l = filter(lambda x: x.getId() == id, self.items)[0]
                    self.items.remove(l)
                    removed = True
                except:
                    log.debug('link:%s is not in the pool. Re-trying' % (id))
            #trace = traceback.format_exc()
            #log.debug('Exception captured. traceback:%s' % (repr(trace)))
            log.debug('giving a break, sleeping little bit')
            time.sleep(self.pause)

    def shuffle(self):
        '''
        Shuffles the links.
        '''    
        with self.lock:
            random.shuffle(self.items)
