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

log = logging.getLogger(__name__)


class Tas(object):
    host, port, jobs = None, None, None
    id = None

    def __init__(self, **kwargs):
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        self.id   = '%s_%s_%s' % (kwargs['host'],
                                  kwargs['port'],
                                  kwargs['jobs'])

    def __str__(self):
        return self.id

    def getId(self):
        return self.id

    def connect(self):
        pass

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
