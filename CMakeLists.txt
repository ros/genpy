cmake_minimum_required(VERSION 2.8)
project(genpy)
find_package(catkin)

# add_subdirectory(scripts)

install_cmake_infrastructure(genpy
  VERSION 0.0.1
  CFG_EXTRAS genpy-extras.cmake
  PYTHONPATH src
  )


file(WRITE genpy "Python")
install(FILES genpy
  DESTINATION etc/langs
  )

catkin_package(genpy)

enable_python(genpy)