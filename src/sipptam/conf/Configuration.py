#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.config.Configuration.py

Generic object to save the configuration parameters.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''

import os
import types
from lxml import etree
from pprint import pformat

from sipptam.utils.Utils import formatXML, listField, contentField, recursive_print
from sipptam.conf.Schema import schema

class Configuration(object):
    '''
    '''
    pdict = None

    def __init__(self, file, validate = None):
        if not os.path.exists(file):
            raise Exception('Configuration file not found')
        try:
            # Loading config file
            tree = etree.parse(file)
            if validate:
                # Running validation
                xmlschema_doc = etree.parse(validate)
                xmlschema = etree.XMLSchema(xmlschema_doc)
                # Lets validate against the XSD schema.
                xmlschema.assertValid(tree)
            root = tree.getroot()
            self.xmldict = formatXML(root, 'List')
        except:
            self.xmldict = None
            raise

    def __str__(self):
        return pformat(self.xmldict)

    def printLogging(self):
        recursive_print(self.xmldict)

    def searchAttr(self, dict, node, attr):
        '''
        Recursive private function to search an attr for a given node.
        '''
        ret = None
        if dict.has_key(node):
            if type(dict[node]) is types.DictType and dict[node].has_key(attr):
                ret = dict[node][attr]
        else:
            for k in filter(lambda x: (type(dict[x]) is types.DictType), dict.keys()):
                ret = self.searchAttr(dict[k], node, attr)
                if ret: break
        return ret
        
    def getAttr(self, node, attr):
        '''
        Returns the value of the attr in the node.
        If it doesn't exist, returns None.
        '''
        return self.searchAttr(self.xmldict.copy(), node, attr)
        
    def getList(self, node):
        '''
        Returns the list of the node.
        If it doesn't exist, returns None.
        '''
        return self.searchAttr(self.xmldict.copy(), node, listField)

    def getContent(self, node):
        '''
        Returns the content of the node.
        If it doesn't exist, returns None.
        '''
        return self.searchAttr(self.xmldict.copy(), node, contentField)

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    import sys

    # We need the configuration file as input parameter.
    if len(sys.argv) < 2:
        sys.exit('Usage: %s <config_file>' % sys.argv[0])

    if not os.path.exists(sys.argv[1]):
        sys.exit('Error. File %s was not found!' % sys.argv[1])

    # Lexical validation
    try:
        p = Configuration(sys.argv[1], validate = schema)
        #p = Configuration(sys.argv[1])
    except Exception, msg:
        print 'Error. Parsing configuration file error: %s' % msg
    else:
        print p
        print 'Lexical validation succeed!'



    # Playing with it... Lets print all the probes
    defaultN = p.getAttr('probeList', 'defaultN')
    defaultPort = p.getAttr('probeList', 'defaultPort')
    for probe in p.getList('probeList'):
        try: tmp_n = probe['n']
        except: tmp_n = defaultN
        try: tmp_port = probe['port']
        except: tmp_port = defaultPort
        for n in range(0, int(tmp_n)):
            print '%s:%s:%s' % (probe['host'],tmp_port, n)