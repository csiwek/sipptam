#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.config.Config.py
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Object which represents a config element.

    @author:  Luis Martin Gil
    @contact: luis.martin.gil@indigital.net
    @organization: INdigital Telecom, Inc.
    @copyright: INdigital Telecom, Inc. 2013
"""

from sipptam.mod.Mod import Mod
from sipptam.config.Config import Config

class itemNotFoundExcept(Exception):
    pass

class unknownModExcept(Exception):
    pass

class unknownConfigExcept(Exception):
    pass

class Testrun(object):
    '''
    '''
    config = None
    mod = None
    def __init__(self, **kwargs):
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        self.kwargs = kwargs

    def __str__(self):
        return '%s config:%s mod:%s' % (str(self.kwargs),
                                        self.config, 
                                        self.mod)

    def get(self, attr):
        if attr in self.kwargs.keys():
            return self.kwargs[attr]
        else:
            raise itemNotFoundExcept('[error] attr:%s not found' % attr)

    def setConfig(self, c):
        if isinstance(c, Config):
            self.config = c
        else:
            raise unknownConfigExcept('Config type unknown ' + \
                                          'config:\"%s\", ' + \
                                          'type:\"%s\"' % \
                                          (c, type(c)))
    def setMod(self, m):
        if isinstance(m, Mod):
            self.mod = m
        else:
            raise unknownModExcept('Mod type unknown ' + \
                                       'mod:\"%s\", ' + \
                                       'type:\"%s\"' % \
                                       (m, type(m)))

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    pass
