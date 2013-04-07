#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.modification.Injection.py

Object which represents a fieldsf element.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''


class Injection(object):
    '''
    '''
    kwargs = None
    def __init__(self, **kwargs):
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        self.kwargs = kwargs

    def __str__(self):
        tmp = []
        for key, value in self.kwargs.iteritems():
            tmp.append('    * %s:\"%s\"' % (key, value))
        return "\n".join(tmp)

    def apply(self):
        pass

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
