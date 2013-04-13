#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.mod.InputReplace.py

Object which represents an input replace element.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2013
'''
import logging

from sipptam.mod.Replace import Replace

logger = logging.getLogger(__name__)


# class InputReplace(object):
#     '''
#     '''
#     regex = None
#     def __init__(self):
#         self.regex = r"!sipptas\((?P<name>port|host)\((?P<number>\d+)\)\)!"

#     def getReplaces(self, scenarioContent, tasL):
#         '''
#         Pre. tas already has a port assigned.
#         '''
#         ret = []
#         for name, number in re.findall(regex, tmp):
#             tas = tasL[int(number)]
#             host, port = tas.getTasHost(), tas.getTasPort()
#             if 'port' == name: dst = port
#             elif 'host' == name: dst = host
#             ori = ('!sipptas(%s(%s))!' % (name, number))
#             # Tweaking the Replace so it always matches.
#             ret.append(Replace({'regex' : '(.*)', 'src' : ori, 'dst' : dst}))
#         return ret


if __name__ == '__main__':
    '''
    Main execution thread.
    '''

