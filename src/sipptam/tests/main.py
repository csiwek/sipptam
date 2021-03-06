   #!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sipptam.tests.Tests.py

This runs all the tests.

@author:  Luis Martin Gil
@contact: martingil.luis@gmail.com
@organization: INdigital Telecom, Inc.
@copyright: INdigital Telecom, Inc. 2012
'''

import unittest


import sipptam.tests.test_Configuration
import sipptam.tests.test_Schema


if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    suites = [sipptam.tests.test_Configuration.suite(),
              sipptam.tests.test_Schema.suite()]
    alltests = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)
