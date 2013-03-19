#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.modification.Modification.py

Object which represents a modification element.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''


class Modification(object):
    '''
    '''
    def __init__(self, **kwargs):
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        pass

    def __str__(self):
        return str(self.args)

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    t = Modification(color="red", bold=False)
    print t
