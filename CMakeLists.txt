cmake_minimum_required(VERSION 2.8)
project(genpy)
find_package(catkin)

add_subdirectory(scripts)

catkin_stack()
catkin_project(genpy
  CFG_EXTRAS genpy-extras.cmake
  )


file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/genpy "Python")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/genpy
  DESTINATION etc/langs
  )

install(FILES stack.xml DESTINATION share/${PROJECT_NAME})

catkin_python_setup()

add_nosetests(${PROJECT_SOURCE_DIR})
