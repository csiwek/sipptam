#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.modification.Replace.py

Object which represents a replace element.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''


class Replace(object):
    '''
    '''
    kwargs = None
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        pass

    def __str__(self):
        return str(self.args)
    
    def apply(self):
        print self.kwargs['src']

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
