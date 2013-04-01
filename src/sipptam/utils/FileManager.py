#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.utils.Filemanager.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Object which represents a filemanager element.

    @author:  Luis Martin Gil
    @contact: luis.martin.gil@indigital.net
    @organization: INdigital Telecom, Inc.
    @copyright: INdigital Telecom, Inc. 2013
"""
import logging

log = logging.getLogger(__name__)


class FileManager(object):
    '''
    '''
    files = None
    def __init__(self):
        self.files = {}

    def __str__(self):
        return str(self.files)

    def addFile(self, fnames):
        for fn in [x for x in fnames if x not in self.files.keys()]:
            log.debug('Adding file \"%s\" to the FileManager cache.' % fn)
            with open(fn, 'r') as f:
                self.files[fn] = f.read()

    def getFile(self, name):
        return self.files[name]

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    pass
