#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sipptam.utils.Messages.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    This module provides informational functions for the users.

    @author:  Luis Martin Gil
    @contact: luis.martin.gil@indigital.net
    @organization: INdigital Telecom, Inc.
    @copyright: INdigital Telecom, Inc. 2013
"""
import sys

def showVersion():
    '''
    Helper function to show the 
    '''
    msgs = ['Beta version.',
            'INdigital Telecom 2013.',
            'Luis Martin Gil.',
            '',
            'Not running!']
    print '\n'.join(msgs)
    sys.exit(1)

def showHelp():
    '''
    Helper function to which prints how to run this script
    '''
    msgs = ['%s. Help menu.' % name,
            '',
            'Parameters:',
            ' -c  <configfile>',
            ' -i  ::sets interactive mode',
            ' -b  ::sets background mode',
            ' -v  ::shows version',
            ' -h  ::shows help',
            '',
            'Usage:',
            '    %s -c <configfile>' % name,
            '    %s -c <configfile> -i' % name,
            '    %s -c <configfile> -b' % name,
            '    %s -c <configfile> -v' % name,
            '    %s -c <configfile> -h' % name,
            '',
            'Not running!']
    print '\n'.join(msgs)
    sys.exit(1)
