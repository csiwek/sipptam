#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.config.Config.py
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Object which represents a config element.

    @author:  Luis Martin Gil
    @contact: martingil.luis@gmail.com
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

    def __len__(self):
        return len(self.get('scenarioNameL'))

    def __iter__(self):
        for s in self.get('scenarioNameL'):
            yield s

    def getConf(self):
        return self.get('config')
    
    def getId(self):
        return self.get('id')

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

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    pass
