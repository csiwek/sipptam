   #!/usr/bin/python
# -*- coding: utf-8 -*-

'''
tam.tests.Tests.py

This runs all the tests.

@author:  Luis Martin Gil
@contact: luis.martin.gil@indigital.net
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''

import unittest


import tam.tests.test_Configuration
import tam.tests.test_Schema


if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    suites = [tam.tests.test_Configuration.suite(),
              tam.tests.test_Schema.suite()]
    alltests = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)
