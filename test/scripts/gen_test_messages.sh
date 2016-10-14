#!/bin/bash
GENPY_BASE_PATH=$(readlink -f $(dirname $0)/../..)

find $GENPY_BASE_PATH/test/msg/*.msg | xargs $GENPY_BASE_PATH/scripts/genmsg_py.py -p genpy -Igenpy:$GENPY_BASE_PATH/test/msg -o $GENPY_BASE_PATH/src/genpy/msg
$GENPY_BASE_PATH/scripts/genmsg_py.py --initpy -o $GENPY_BASE_PATH/src/genpy/msg
