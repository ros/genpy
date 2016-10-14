#!/bin/bash
GENPY_BASE_PATH=$(readlink -f $(dirname $0)/../..)

catkin_make_isolated --directory $GENPY_BASE_PATH/../.. --pkg genpy --cmake-args -DCATKIN_ENABLE_TESTING=1
catkin_make --directory $GENPY_BASE_PATH/../.. run_tests_genpy
