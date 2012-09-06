cmake_minimum_required(VERSION 2.8)
project(genpy)
find_package(catkin REQUIRED COMPONENTS genmsg)

catkin_stack()
catkin_project(${PROJECT_NAME}
  CFG_EXTRAS genpy-extras.cmake)

add_subdirectory(scripts)

file(WRITE ${CATKIN_BUILD_PREFIX}/${GENMSG_LANGS_DESTINATION}/genpy "Python")
install(FILES ${CATKIN_BUILD_PREFIX}/${GENMSG_LANGS_DESTINATION}/genpy
  DESTINATION ${GENMSG_LANGS_DESTINATION})

catkin_python_setup()

catkin_add_nosetests(${PROJECT_SOURCE_DIR})
