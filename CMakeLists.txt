cmake_minimum_required(VERSION 2.8)
project(genpy)
find_package(catkin REQUIRED)

add_subdirectory(scripts)

catkin_stack()
catkin_project(genpy
  CFG_EXTRAS genpy-extras.cmake
  )

file(WRITE ${catkin_BUILD_PREFIX}/etc/langs/genpy "Python")
install(FILES ${catkin_BUILD_PREFIX}/etc/langs/genpy
  DESTINATION etc/langs
  )

install(FILES stack.xml DESTINATION share/${PROJECT_NAME})

catkin_python_setup()

add_nosetests(${PROJECT_SOURCE_DIR})
