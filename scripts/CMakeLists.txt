cmake_minimum_required(VERSION 2.8)

install(
  PROGRAMS genmsg_py.py gensrv_py.py
  DESTINATION bin)

#install(
#  FILES msg.h.template srv.h.template
#  DESTINATION share/genpy
#  )
