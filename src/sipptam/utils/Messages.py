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
import logging


def showInteractiveOut(name, version):
    '''
    '''
    msgs = ['You decided not to continue.'
            'Thanks for using this software.',
            '%s - %s' % (name, version)]
    logging.info('\n'.join(msgs))
    sys.exit(1)

def showVersion(name, version):
    '''
    Helper function to show the 
    '''
    msgs = ['%s - %s' % (name, version),
            'INdigital Telecom 2013.',
            'Luis Martin Gil.',
            '',
            'Not running!']
    logging.info('\n'.join(msgs))
    sys.exit(1)

def showHelp(name, version):
    '''
    Helper function to which prints how to run this script
    '''
    msgs = ['%s - %s. Help menu.' % (name, version),
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
    logging.info('\n'.join(msgs))
    sys.exit(1)
