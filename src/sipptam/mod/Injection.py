#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.mod.Injection.py

Object which represents a fieldsf element.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''
import logging

from sipptam.mod.Mod import Mod

logger = logging.getLogger(__name__)


class Injection(Mod):
    '''
    '''
    def apply(self, scenario):
        '''
        If the mod matches we return the injection file attached to the mod.
        '''
        # TODO. cache the scenarios that have been already processed
        injection = None
        if self.matches(scenario):
            injection = self.kwargs['path']
            logger.debug('Applying injection:\"%s\" to scenario:\"%s\"' %
                         (injection, scenario))
        else:
            logger.debug('Injection:\"%s\" not match scenario:\"%s\"' %
                         (injection, scenario))
        return injection


if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
