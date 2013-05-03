#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
sipptam.validate.Validate.py

Generic object to save the configuration parameters.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''

import logging
import traceback
import os
import types
from lxml import etree
from pprint import pformat

from sipptam.utils.Utils import xml2obj
from sipptam.validate.Schema import schema
from sipptam.validate.Semantic import checkSemantics


logger = logging.getLogger(__name__)


class Validate(object):
    '''
    '''
    root = None
    obj = None
    def __init__(self, file, parse = False):
        if not os.path.isfile(file):
            raise Exception('Configuration file not found')
        try:
            # Loading config file
            tree = etree.parse(file)
            if parse:
                # Running validation
                xmlschema_doc = etree.parse(schema)
                xmlschema = etree.XMLSchema(xmlschema_doc)
                # Lets check against the XSD schema.
                xmlschema.assertValid(tree)
            self.root = tree.getroot()
            with open(file, 'r') as f:
                self.obj = xml2obj(f.read())
        except Exception, err:
            self.obj = None
            trace = traceback.format_exc()
            logger.error('Exception:%s traceback:%s' % (err, trace))
            raise
    def __str__(self):
        return pformat(self.obj)
    def checkSemantics(self):
        checkSemantics(self.obj)

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    pass
