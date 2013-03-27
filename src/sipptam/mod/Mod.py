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
#from sipptam.mod.Replace import Replace
#from sipptam.mod.Fieldsf import Fieldsf
#from sipptam.utils.Utils import fill


class Mod(object):
    '''
    '''
    kwargs = None
    def __init__(self, **kwargs):
        #for key, value in kwargs.iteritems():
        #    print "%s = %s" % (key, value)
        self.kwargs = kwargs
        #self.id = kwargs['id']
        #self.replaces = fill(Replace, kwargs['replace'])
        #self.fieldsfs = fill(Fieldsf, kwargs['fieldsf'])
        
    def __str__(self):
        tmp = []
        tmp.append('=> mod:\"%s\"' % self.getId())
        for key, value in self.kwargs.iteritems():
            tmp.append('    * %s:\"%s\"' % (key, value))
        return "\n".join(tmp)

    def getId(self):
        return self.kwargs['id']

    def apply(self):
        map(lambda x : x.apply(), \
                self.replaces + self.fieldsfs)

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
