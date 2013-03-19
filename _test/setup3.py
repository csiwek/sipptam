#!/usr/bin/python

import os
import sys
import glob
from setuptools import setup, find_packages

PACKAGES = ['sipptam']

classes = """
    Development Status :: 3 - Alpha
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Topic :: System :: Distributed Computing
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.6
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

def get_init_val(val, packages=PACKAGES):
    pkg_init = "%s/__init__.py" % PACKAGES[0]
    value = '__%s__' % val
    fn = open(pkg_init)
    for line in fn.readlines():
        if line.startswith(value):
            return line.split('=')[1].strip().strip("'")

setup(
    name=get_init_val('title'),
    version=get_init_val('version'),
    description=get_init_val('description'),
    long_description=open('README.rst').read(),
    author=get_init_val('author'),
    author_email=get_init_val('email'),
    url=get_init_val('url'),
    classifiers  = classifiers,
    package_dir  = {"":"src"},
    package_data={'': ['LICENSE', 'NOTICE']},
    packages     = PACKAGES,
    entry_points = {
        'console_scripts': [
            'sipptam = sipptam.sipptam:main',
            ],
        },
    install_requires = ['lxml'],
    license=get_init_val('license'),
    data_files = [(os.path.join(sys.prefix, 'usr', 'local', 'share', nname, 'scenarios'),
                   glob.glob(os.path.join('resources', 'scenarios', '*.xml'))),
                  (os.path.join(sys.prefix, 'usr', 'local', 'share', nname, 'config'),
                   glob.glob(os.path.join('resources', 'sipptam.xml.sample')))]
)
