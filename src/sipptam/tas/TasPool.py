#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.tas.TasPool.py

This module implements the TasPool class.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''
import logging

from sipptam.thread.Pool import Pool

logger = logging.getLogger(__name__)


class TasPool(Pool):
    '''
    Represents a pool of tas.
    '''
    pass
#    def bridgeAll(self, fun, args):
#        with self.lock:
#            map(lambda x: x.bridge(fun, args), self.items)

#     def killAllSIPp(self):
#         with self.lock:
#             # Lets pick a tas for each of the hosts
#             d = {x.getTasHost(): x for x in self.items}
#             logger.debug('Killing SIPp instances from hosts:%s' % d.keys())
#             # We need to clear the existing SIPp instances.
#             for key, value in d.iteritems():
#                 ret = value.killAllSIPp()
#                 if ret: logger.debug('SIPp instances killed in host:%s' % key)
#                 else: logger.warning('Unable kill SIPp instances from host:%s' % key)
