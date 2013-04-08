#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.mod.Mod.py
    ~~~~~~~~~~~~~~~~~~

    Object which represents a mod element.

    @author:  Luis Martin Gil
    @contact: luis.martin.gil@indigital.net
    @organization: INdigital Telecom, Inc.
    @copyright: INdigital Telecom, Inc. 2013. luismartingil.
    @license: See LICENSE_FILE.
"""

import re


class Mod(object):
    '''
    '''
    regex = None
    kwargs = None
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.regex = kwargs['regex']

    def __str__(self):
        tmp = []
        for key, value in self.kwargs.iteritems():
            tmp.append('    * %s:\"%s\"' % (key, value))
        return "\n".join(tmp)

    def matches(self, scenario):
        return re.match(self.regex, scenario)


    # TODO. Make it mandatory to define when subclassing from Mod class!
    #def apply(self, scenario, scenarioContent):
    #    pass

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
