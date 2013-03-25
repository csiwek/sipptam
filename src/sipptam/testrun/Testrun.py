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
from sipptam.utils.Utils import filesMatch


# Some exceptions
class itemNotFoundExcept(Exception):
    pass
class invalidTypeExcept(Exception):
    pass


class Testrun(object):
    '''
    '''
    kwargs = None
    def __init__(self, **kwargs):
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        self.kwargs = kwargs

    def __str__(self):
        tmp = []
        tmp.append('kwargs:%s' % self.kwargs)
        return "\n".join(tmp)

    def has(self, attr):
        return attr in self.kwargs.keys()

    def get(self, attr):
        if attr in self.kwargs.keys():
            return self.kwargs[attr]
        else:
            raise itemNotFoundExcept('[error] attr:\"%s\" not found' % attr)

    def set(self, key, value, t):
        if isinstance(value, t):
            self.kwargs[key] = value
        else:
            raise invalidTypeExcept('Type mismatch ' +
                                    'key:\"%s\" t:\"%s\" type(key):\"%s\"' %
                                    (key, t, type(key)))

    def tmpRun(self):
        print '+' * 80
        print self.get('regex')
        print self.get('scenarioPath')
        print filesMatch(self.get('scenarioPath'), self.get('regex'))

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    pass
