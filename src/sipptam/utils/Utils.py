#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.utils.Configuration.py

Generic object to save the configuration parameters.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''

import logging
import re
from lxml import etree

def str2bool(v):
    '''
    Returns a Boolean type from the v string value.

    @v: String to match as a Boolean.
    @type v:  str
    '''
    return v.lower() in ("yes", "true", "t", "1")


def fill(tmpClass, args, dic = False):
    '''
    Help function in conjunction to xml2obj
    '''
    tmp = []
    map(lambda x: tmp.append(tmpClass(**dict(x._attrs))), args)
    if dic:
        return dict([(x.getId(), x) for x in tmp]) #return tmp
    else:
        return tmp

## {{{ http://code.activestate.com/recipes/534109/ (r8)
import re
import xml.sax.handler

def xml2obj(src):
    """
    A simple function to converts XML data into native Python object.
    """

    non_id_char = re.compile('[^_0-9a-zA-Z]')
    def _name_mangle(name):
        return non_id_char.sub('_', name)

    class DataNode(object):
        def __init__(self):
            self._attrs = {}    # XML attributes and child elements
            self.data = None    # child text data
        def __len__(self):
            # treat single element as a list of 1
            return 1
        def __getitem__(self, key):
            if isinstance(key, basestring):
                return self._attrs.get(key,None)
            else:
                return [self][key]
        def __contains__(self, name):
            return self._attrs.has_key(name)
        def __nonzero__(self):
            return bool(self._attrs or self.data)
        def __getattr__(self, name):
            if name.startswith('__'):
                # need to do this for Python special methods???
                raise AttributeError(name)
            return self._attrs.get(name,None)
        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                # multiple attribute of the same name are represented by a list
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value
        def __str__(self):
            return self.data or ''
        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return u'{%s}' % ', '.join([u'%s:%s' % (k,repr(v)) for k,v in items])

    class TreeBuilder(xml.sax.handler.ContentHandler):
        def __init__(self):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []
        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            # xml attributes --> python attributes
            for k, v in attrs.items():
                self.current._add_xml_attr(_name_mangle(k), v)
        def endElement(self, name):
            text = ''.join(self.text_parts).strip()
            if text:
                self.current.data = text
            if self.current._attrs:
                obj = self.current
            else:
                # a text only node is simply represented by the string
                obj = text or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(_name_mangle(name), obj)
        def characters(self, content):
            self.text_parts.append(content)

    builder = TreeBuilder()
    if isinstance(src,basestring):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    return builder.root._attrs.values()[0]
## end of http://code.activestate.com/recipes/534109/ }}}

'''
translates the context of a string based on a given dictionary
'''
def translate(text, d):
    logging.debug('translating text:\"%s\" using d:\"%s\"' % (text, d))
    ret = reduce(lambda x, y: x.replace(y, d[y]), d, text)
    logging.debug('translated result:\"%s\"' % (ret))
    return ret

'''
returns a dict given a string value like: key1=val1;key2=val2;keyn=valn
'''
def text2dic(text, assign = '=', sep = ';'):
    '''                                                                               
    The escape character will be '\'                                                  
    Might raise ValueError Exception if text is not properly formed.                  
    '''
    logging.debug('converting text to dic assign:\"%s\", sep:\"%s\", text:\"%s\"' % (assign, sep, text))
    l = map (lambda x : x.replace('\\', ''), re.split(r'(?<!\\);', text))
    ret = dict((n,v) for n,v in (a.split(assign, 1) for a in l))
    logging.debug('converted dic:\"%s\"' % (ret))
    return ret
