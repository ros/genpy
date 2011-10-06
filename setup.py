from distutils.core import setup

setup(name='genpy',
      version= '0.1.0',
      packages=['genpy'],
      package_dir = {'':'src'},
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
