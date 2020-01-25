from catkin_pkg.python_setup import generate_distutils_setup

from setuptools import setup

d = generate_distutils_setup(
    packages=['genpy'],
    package_dir={'': 'src'},
    requires=['genmsg']
)

setup(**d)
