#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.testrun.Scenario.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This module represents an scenario.

    @author:  Luis Martin Gil
    @contact: luis.martin.gil@indigital.net
    @organization: INdigital Telecom, Inc.
    @copyright: INdigital Telecom, Inc. 2013
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
