Source: @(CATKIN_PACKAGE_PREFIX)genpy
Section: misc
Priority: extra
Maintainer: Troy Straszheim <straszheim@@willowgarage.com>
Build-Depends: debhelper (>= 7), cmake, make, catkin
Homepage: <insert the upstream URL, if relevant>

Package: @(CATKIN_PACKAGE_PREFIX)genpy
Architecture: all
Depends: ${misc:Depends} @(CATKIN_PACKAGE_PREFIX)genmsg
Description: It generates python, it does
 <insert long description, indented with spaces>
X-ROS-Pkg-Name: genpy
X-ROS-Pkg-Depends: catkin, genmsg
X-ROS-System-Depends:
X-ROS-Message-Generator: C++