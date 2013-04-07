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

class itemNotFoundExcept(Exception):
    pass

class Mod(object):
    '''
    '''
    kwargs = None
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    def getId(self):
        return self.kwargs['id']

    def apply(self, scenario, sfcontent):
        '''
        Returns: (sfcontent*, injection*)
        '''
        pass

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
