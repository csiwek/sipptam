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

from sipptam.mod.Replace import Replace
from sipptam.mod.Fieldsf import Fieldsf
from sipptam.utils.Utils import fill


class Mod(object):
    '''
    '''
    id = None
    replaces = None
    fieldsfs = None
    def __init__(self, **kwargs):
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        self.id = kwargs['id']
        self.replaces = fill(Replace, kwargs['replace'])
        self.fieldsfs = fill(Fieldsf, kwargs['fieldsf'])
        
    def __str__(self):
        return 'id:%s replaces:%s fieldsfs:%s' % (self.id,
                                                  self.replaces,
                                                  self.fieldsfs)
    def getId(self):
        return self.id

    def apply(self):
        map(lambda x : x.apply(), \
                self.replaces + self.fieldsfs)

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
