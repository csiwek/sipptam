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
import time

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
        self.kwargs = kwargs

    def __str__(self):
        tmp = []
        tmp.append('~' * 50)
        tmp.append('testrun:\"%s\"' % (self.getId()))
        tmp.append("%s" % (self.kwargs['config']))
        if self.kwargs.has_key('mod'):
            tmp.append("%s" % (self.kwargs['mod']))
        tmp.append("kwargs:%s" % self.kwargs)
        return "\n".join(tmp)

    def getId(self):
        return self.kwargs['id']

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

    def run(self):
        for ratio in range(1, 3):
            for max in range(6, 7):
                for tries in range(1, 2):
                    for s in self.get('scenarioNameL'):
                        print s

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    pass
