#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.tas.Testrun.py

Object which represents a testrun element.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''


class Testrun(object):
    '''
    '''
    def __init__(self, **kwargs):
        self.args = kwargs

    def __str__(self):
        return str(self.args)

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    t = Testrun(color="red", bold=False)
    print t
