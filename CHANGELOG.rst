^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package genpy
^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.6.14 (2020-08-10)
-------------------
* create Struct objects to save memory (`#129 <https://github.com/ros/genpy/issues/129>`_)

0.6.13 (2020-07-20)
-------------------
* don't raise exceptions on unicode decode error (`#127 <https://github.com/ros/genpy/issues/127>`_)

0.6.12 (2020-05-28)
-------------------
* fix check_type for uint8[] to accept bytes (`#123 <https://github.com/ros/genpy/issues/123>`_)

0.6.11 (2020-05-12)
-------------------
* support non-int integral time parameters (`#121 <https://github.com/ros/genpy/issues/121>`_)

0.6.10 (2020-01-24)
-------------------
* various code cleanup (`#117 <https://github.com/ros/genpy/issues/117>`_)
* update logic for newer PyYAML output for dump() (`#116 <https://github.com/ros/genpy/issues/116>`_)
* small optimization in dynamic.py (`#109 <https://github.com/ros/genpy/issues/109>`_)
* use setuptools instead of distutils (`#115 <https://github.com/ros/genpy/issues/115>`_)
* bump CMake version to avoid CMP0048 warning (`#114 <https://github.com/ros/genpy/issues/114>`_)
* serialization: always set _x var for correct exception msg (`#113 <https://github.com/ros/genpy/issues/113>`_)
* sort generated imports to make them reproducible (`#111 <https://github.com/ros/genpy/issues/111>`_)
* make the generated "struct" constructs reproducible (`#110 <https://github.com/ros/genpy/issues/110>`_)

0.6.9 (2019-10-03)
------------------
* fix Python 3 buffer handling (`#106 <https://github.com/ros/genpy/issues/106>`_)
* Python 3 compatibility (`#104 <https://github.com/ros/genpy/issues/104>`_)
* fix usage of undefined variables in exception (`#105 <https://github.com/ros/genpy/issues/105>`_)
* convert map iterator to list (`#103 <https://github.com/ros/genpy/issues/103>`_)
* fix negative limit check for signed ints (`#102 <https://github.com/ros/genpy/issues/102>`_)
* failing test case for UTF-8 encoded characters in comments (`#95 <https://github.com/ros/genpy/issues/95>`_)

0.6.8 (2019-03-04)
------------------
* check size of fixed sized arrays when serializing (`#92 <https://github.com/ros/genpy/issues/92>`_)
* allow returning derived types in overloaded operators (`#100 <https://github.com/ros/genpy/issues/100>`_)
* reload() was move into importlib in Python 3 (`#98 <https://github.com/ros/genpy/issues/98>`_)
* fix _convert_getattr for handling uint8[] message fields in Python 3 (`#96 <https://github.com/ros/genpy/issues/96>`_)

0.6.7 (2017-10-26)
------------------
* use errno to detect existing dir (`#89 <https://github.com/ros/genpy/issues/89>`_)
* fix typo (`#84 <https://github.com/ros/genpy/issues/84>`_)

0.6.6 (2017-07-27)
------------------
* add escaping for strings which is valid in YAML (`#79 <https://github.com/ros/genpy/issues/79>`_)
* fix inefficient canon method in rostime (`#77 <https://github.com/ros/genpy/issues/77>`_)

0.6.5 (2017-03-06)
------------------
* expose spec for dynamically generated messages (`#75 <https://github.com/ros/genpy/issues/75>`_)

0.6.4 (2017-02-27)
------------------
* fix default value for non-primitive fixed-size arrays, regression of 0.6.1 (`#74 <https://github.com/ros/genpy/issues/74>`)

0.6.3 (2016-10-24)
------------------
* fix Python 3 regressions (`#71 <https://github.com/ros/genpy/issues/71>`_)
* use Python safe subfields for nested types (`#69 <https://github.com/ros/genpy/issues/69>`_)

0.6.2 (2016-09-03)
------------------
* fix regression regarding lazy init introduced in 0.6.1 (`#67 <https://github.com/ros/genpy/issues/67>`_)

0.6.1 (2016-09-02)
------------------
* lazy init struct (`#65 <https://github.com/ros/genpy/issues/65>`_)
* fix default value of lists to not expand to N items in the generated code (`#64 <https://github.com/ros/genpy/issues/64>`_)
* simpler and more canonical hash (`#55 <https://github.com/ros/genpy/pull/55>`_)
* various improvements to the time and duration classes (`#63 <https://github.com/ros/genpy/issues/63>`_)

0.6.0 (2016-04-21)
------------------
* change semantic of integer division for duration (`#59 <https://github.com/ros/genpy/issues/59>`_)

0.5.9 (2016-04-19)
------------------
* warn about using floor division of durations (`#58 <https://github.com/ros/genpy/issues/58>`_)
* allow durations to be divided by other durations (`#48 <https://github.com/ros/genpy/issues/48>`_)
* avoid adding newline in msg_generator (`#47 <https://github.com/ros/genpy/issues/47>`_, `#51 <https://github.com/ros/genpy/issues/51>`_)

0.5.8 (2016-03-09)
------------------

* right align nsec fields of timestamps (`#45 <https://github.com/ros/genpy/issues/45>`_)
* fix order of imports in generated init files deterministic (`#44 <https://github.com/ros/genpy/issues/44>`_)
* fix exception handling code using undefined variable (`#42 <https://github.com/ros/genpy/issues/42>`_)
* add test for expected exception when serializing wrong type

0.5.7 (2015-11-09)
------------------
* add line about encoding to generated Python files (`#41 <https://github.com/ros/genpy/issues/41>`_)

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
