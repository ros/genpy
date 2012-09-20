#!/usr/bin/env python

from distutils.core import setup
from catkin.package import parse_package_for_distutils

d = parse_package_for_distutils()
d['packages'] = ['genpy']
d['package_dir'] = {'': 'src'}
d['install_requires'] = ['genmsg']
d['scripts'] = ['scripts/genmsg_py.py', 'scripts/gensrv_py.py']

setup(**d)
