#!/usr/bin/python

import re
import glob
import os
import sys
from setuptools import setup, find_packages

main_path = 'src/sipptam/sipptam.py'

def get_name(f):
    return re.search(r"""__name__\s+=\s+(?P<quote>['"])(?P<name>.+?)(?P=quote)""", open(f).read()).group('name')
def get_version(f):
    return re.search(r"""__version__\s+=\s+(?P<quote>['"])(?P<version>.+?)(?P=quote)""", open(f).read()).group('version')

nname = get_name(main_path)

setup(name         = nname,
      version      = get_version(main_path),
      author       = "Luis Martin Gil",
      author_email = "martingil.luis@gmail.com",
      url          = "http://www.luismartingil.com",
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
      install_requires = ['lxml', 'pysimplesoap', 'texttable'],
      data_files = [(os.path.join(sys.prefix, 'local', 'share', nname, 'injections'),
                     glob.glob(os.path.join('resources', 'injections', '*.csv'))),
                    (os.path.join(sys.prefix, 'local', 'share', nname, 'scenarios'),
                     glob.glob(os.path.join('resources', 'scenarios', '*.xml'))),
                    (os.path.join(sys.prefix, 'local', 'share', nname),
                     glob.glob(os.path.join('resources', '*.xml')))]
      )
