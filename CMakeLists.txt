cmake_minimum_required(VERSION 2.8)
project(genpy)
find_package(catkin)

add_subdirectory(scripts)

catkin_project(genpy
  VERSION 0.0.1
  CFG_EXTRAS genpy-extras.cmake
  PYTHONPATH src
  )


file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/genpy "Python")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/genpy
  DESTINATION etc/langs
  )

enable_python(genpy)

