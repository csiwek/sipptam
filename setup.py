#!/usr/bin/python

import glob
import os

from setuptools import setup, find_packages

nname = 'sipptam'

setup(name         = nname,
      version      = "0.0.2",
      author       = "INdigital Telecom",
      author_email = "luis.martin.gil@indigital.net",
      url          = "http://www.indigital.net",
      description  = "%s - Sipp Testing Automation Manager" % nname,
      classifiers  = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Service Providers",
            "License :: GNU General Public License 3",
            "Operating System :: OS Independent",
            "Programming Language :: Python"
                     ],
      package_dir  = {"":"src"},
      packages     = find_packages('src'),
      scripts      = [nname],
      data_files   = [('share/' + nname + '/scenarios', glob.glob(os.path.join('resources', 'scenarios', '*.xml')))]
      )
