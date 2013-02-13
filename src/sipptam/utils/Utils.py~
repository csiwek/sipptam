#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
tam.utils.Configuration.py

Generic object to save the configuration parameters.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''

import logging
import re
from lxml import etree

def recursive_print(src, dpth = 0, key = ''):
    """ Recursively prints nested elements."""
    tabs = lambda n: ' ' * n * 4 # or 2 or 8 or...
    brace = lambda s, n: '%s%s%s' % ('['*n, s, ']'*n)

    if isinstance(src, dict):
        for key, value in src.iteritems():
            logging.info(tabs(dpth) + brace(key, dpth))
            recursive_print(value, dpth + 1, key)
    elif isinstance(src, list):
        for litem in src:
            recursive_print(litem, dpth + 2)
    else:
        if key:
            logging.info(tabs(dpth) + '%s = %s' % (key, repr(src)))
        else:
            logging.info(tabs(dpth) + '- %s' % src)

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


listField = '__list__'
contentField = '__content__'
def formatXML(xmltree, listToken):
    '''
    Returns a XML tree formated as dicts and lists. Decision whether to add the tag
    as a list or dictionary is based on finding the 'listToken' word in the actual tag.
    Recursive operation.

    # Example 1:
    tree = lxml.etree.parse('path_to_file')
    root = tree.getroot()
    xmldict = formatXML(root)

    # Example 2:
    tree = lxml.etree.fromstring(reply)
    xmldict = formatXML(tree)

    @xmltree: XML tree to be processed.
    @type xmltree:  lxml.etree structure.
    '''

    def format(tree):
        '''
        @tree: XML tree to be processed.
        @type tree:  lxml.etree structure.
        '''
        ret = {}
        if tree.items(): ret.update(dict(tree.items()))
        if tree.text: ret[contentField] = tree.text
        if (listToken in tree.tag):
            ret[listField] = []
            for element in tree:
                if element.tag is not etree.Comment:
                    ret[listField].append(format(element))
        else:
            for element in tree:
                if element.tag is not etree.Comment:
                    ret[element.tag] = format(element)
        return ret
    return {xmltree.tag : format(xmltree)}
