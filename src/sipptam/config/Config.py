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

class itemNotFoundExcept(Exception):
    pass

class Config(object):
    '''
    '''
    def __init__(self, **kwargs):
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        self.kwargs = kwargs

    def __str__(self):
        tmp = []
        tmp.append('=> config:\"%s\"' % self.get('id'))
        for key, value in self.kwargs.iteritems():
            tmp.append('    * %s:\"%s\"' % (key, value))
        return "\n".join(tmp)

    def getId(self):
        return self.kwargs['id']

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
