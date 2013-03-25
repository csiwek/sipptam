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
        self.id = kwargs['id']
        self.mods = []

    def __str__(self):
        return '%s' % (str(self.kwargs))

    def getId(self):
        return self.id

    def get(self, attr):
        if attr in self.kwargs.keys():
            return self.kwargs[attr]
        else:
            raise itemNotFoundExcept('[error] attr:%s not found' % attr)

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    pass
