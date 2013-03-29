#!/usr/bin/python

import glob
import os
import sys
from setuptools import setup, find_packages

nname = 'sipptam'

setup(name         = nname,
      version      = "0.0.9",
      author       = "INdigital Telecom",
      author_email = "luis.martin.gil@indigital.net",
      url          = "http://www.indigital.net",
      description  = "%s - Sipp Test Automation Manager" % nname,
      classifiers  = [
        "Classifier: Development Status :: 4 - Beta",
        "Classifier: Operating System :: POSIX :: Linux",
        "Classifier: Operating System :: MacOS :: MacOS X",
        "Classifier: Programming Language :: Python :: 2.6",
        "Classifier: Programming Language :: Python :: 2.7",
        "Classifier: Environment :: Console",
                     ],
      package_dir  = {"":"src"},
      packages     = find_packages('src'),
      entry_points = {
        'console_scripts': [
            'sipptam = sipptam.sipptam:main',
            ],
        },
      install_requires = ['lxml'],
      data_files = [(os.path.join(sys.prefix, 'usr', 'local', 'share', nname, 'scenarios'),
                     glob.glob(os.path.join('resources', 'scenarios', '*.xml'))),
                    (os.path.join(sys.prefix, 'usr', 'local', 'share', nname, 'config'),
                     glob.glob(os.path.join('resources', 'sipptam.sample.xml')))]
      )
