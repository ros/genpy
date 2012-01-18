#!/usr/bin/env python

from setuptools import setup

import sys
sys.path.insert(0, 'src')

import re
search = re.search(r'Version\:\s*(\d+\.\d+\.\d+)',open('stack.yaml').read())
if not search:
    print >>sys.stderr, 'You must have a Version field in your stack.yaml'
    sys.exit(-1)
__version__ = search.groups()[0]

#from genpy import __version__

setup(name='genpy',
      version= __version__,
      packages=['genpy'],
      package_dir = {'':'src'},
      install_requires=['genmsg'],
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
