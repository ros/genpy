#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup
import sys
from xml.etree.ElementTree import ElementTree

try:
    root = ElementTree(None, 'stack.xml')
    version = root.findtext('version')
except Exception as e:
    print('Could not extract version from your stack.xml:\n%s' % e, file=sys.stderr)
    sys.exit(-1)

sys.path.insert(0, 'src')

setup(name = 'genpy',
      version = version,
      packages = ['genpy'],
      package_dir = {'': 'src'},
      install_requires = ['genmsg'],
      scripts = ['scripts/genmsg_py.py', 'scripts/gensrv_py.py'],
      author = "Ken Conley",
      author_email = "kwc@willowgarage.com",
      url = "http://www.ros.org/wiki/genpy",
      download_url = "http://pr.willowgarage.com/downloads/genpy/",
      keywords = ["ROS"],
      classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License" ],
      description = "ROS msg/srv Python generation",
      long_description = """\
Library and scripts for generating ROS message data structures in Python.
""",
      license = "BSD"
      )
