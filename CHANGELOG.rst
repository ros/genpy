^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package genpy
^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.5.6 (2015-10-12)
------------------
* fix handling of dynamic message classes with names containing other message classes as substrings (`#40 <https://github.com/ros/genpy/pull/40>`_)

0.5.5 (2015-09-19)
------------------
* fix handling of dynamic message classes with the same name (`#37 <https://github.com/ros/genpy/issues/37>`_)
* fix Duration.abs() when sec is zero (`#35 <https://github.com/ros/genpy/issues/35>`_)

0.5.4 (2014-12-22)
------------------
* add support for fixed-width floating-point and integer array values (`ros/ros_comm#400 <https://github.com/ros/ros_comm/issues/400>`_)
* add missing test dependency on yaml

0.5.3 (2014-06-02)
------------------
* make TVal more similar to generated messages for introspection (`ros/std_msgs#6 <https://github.com/ros/std_msgs/issues/6>`_)

0.5.2 (2014-05-08)
------------------
* fix usage of load_manifest() introduced in 0.5.1 (`#28 <https://github.com/ros/genpy/issues/28>`_)

0.5.1 (2014-05-07)
------------------
* resolve message classes from dry packages (`ros/ros_comm#293 <https://github.com/ros/ros_comm/issues/293>`_)
* add architecture_independent flag in package.xml (`#27 <https://github.com/ros/genpy/issues/27>`_)

0.5.0 (2014-02-25)
------------------
* use catkin_install_python() to install Python scripts (`#25 <https://github.com/ros/genpy/issues/25>`_)

0.4.15 (2014-01-07)
-------------------
* python 3 compatibility (`#22 <https://github.com/ros/genpy/issues/22>`_)
* use PYTHON_EXECUTABLE when invoking scripts for better Windows support (`#23 <https://github.com/ros/genpy/issues/23>`_)
* improve exception message when message type does not match (`#21 <https://github.com/ros/genpy/issues/21>`_)

0.4.14 (2013-08-21)
-------------------
* make genpy relocatable (`ros/catkin#490 <https://github.com/ros/catkin/issues/490>`_)
* enable int/long values for list of time/duration (`#13 <https://github.com/ros/genpy/issues/13>`_)
* fix issue with time/duration message fields (without std_msgs prefix) when used as array (`ros/ros_comm#252 <https://github.com/ros/ros_comm/issues/252>`_)
* fix Time() for seconds being of type long on 32-bit systems (fix `#15 <https://github.com/ros/genpy/issues/15>`_)
* fix passing keys to _fill_message_args (`#20 <https://github.com/ros/genpy/issues/20>`_)

0.4.13 (2013-07-03)
-------------------
* check for CATKIN_ENABLE_TESTING to enable configure without tests

0.4.12 (2013-06-18)
-------------------
* fix deserialize bytes in Python3 (`#10 <https://github.com/ros/genpy/issues/10>`_)

0.4.11 (2013-03-08)
-------------------
* fix handling spaces in folder names (`ros/catkin#375 <https://github.com/ros/catkin/issues/375>`_)

0.4.10 (2012-12-21)
-------------------
* first public release for Groovy
