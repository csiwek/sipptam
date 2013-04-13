#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.mod.Replace.py

Object which represents a replace element.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''
import logging

from sipptam.mod.Mod import Mod

logger = logging.getLogger(__name__)


class Replace(Mod):
    '''
    '''
    def apply(self, scenario, scenarioContent):
        '''
        If the mod matches we return the modified scenarioContent.
        '''
        newScenarioContent = scenarioContent
        if self.matches(scenario):
            newScenarioContent = \
                scenarioContent.replace(self.kwargs['src'],
                                        self.kwargs['dst'])
            logger.debug('Replacing:\"%s\" -> \"%s\" in scenario:\"%s\"' %
                         (self.kwargs['src'], self.kwargs['dst'], scenario))
        else:
            logger.debug('Replace \"%s\" -> \"%s\" not match scenario:\"%s\"' %
                         (self.kwargs['src'], self.kwargs['dst'], scenario))
        return newScenarioContent

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
