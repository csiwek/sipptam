# -*- coding: utf-8 -*-
"""
This.

:copyright: (c) 2013 by Luis Martin.
:license: ISC, see LICENSE for more details.
"""


class Scenario(object):
    """
    raw: is a valid parsed scenario
    """
    self.raw = None
    self.replace = None

    def __init__(self, raw, replace):
        self.raw = raw
        self.replace = replace
        
    def __str__(self):
        """Get the string raw scenario"""
        return self.raw
