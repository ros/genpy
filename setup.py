#!/usr/bin/env python

from setuptools import setup

setup(
    name='ros_genpy',
    version='0.5.10',
    description='Python ROS message and service generators.',
    url='http://github.com/ros/genpy',
    author='Ken Conley, Troy Straszheim, Morten Kjaergaard',
    maintainer_email='dthomas@osrfoundation.org',
    license='BSD',
    packages=['genpy'],
    package_dir={'': 'src'},
    install_requires=['ros_genmsg', 'pyyaml'],
    dependency_links=['git+https://github.com/asmodehn/genmsg.git@setuptools#egg=ros_genmsg']
)

