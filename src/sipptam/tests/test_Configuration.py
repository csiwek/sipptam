#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.tests.Configuration_test.py

Tests for tam.conf.Configuration.py

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''


import unittest
import sipptam.conf.Configuration


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        """
        """
        self.widget = 8

    def tearDown(self):
        """
        """
        self.widget = None

    def test_default_size(self):
        """
        """
        self.assertEqual(self.widget, 8,
                         'incorrect default size')

    def test_resize(self):
        """
        """
        self.widget = 10
        self.assertEqual(self.widget, 10,
                         'wrong size after resize')


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(WidgetTestCase)


if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    print 'todo'
