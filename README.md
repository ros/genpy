# genpy

The Python ROS message and service generator.

## Regenerate test messages

```console
./scripts/genmsg_py.py -p genpy -Igenpy:`pwd`/test/msg -o src/genpy/msg `pwd`/test/msg/TestFillEmbedTime.msg
./scripts/genmsg_py.py -p genpy -Igenpy:`pwd`/test/msg -o src/genpy/msg `pwd`/test/msg/TestFillSimple.msg
./scripts/genmsg_py.py -p genpy -Igenpy:`pwd`/test/msg -o src/genpy/msg `pwd`/test/msg/TestManyFields.msg
./scripts/genmsg_py.py -p genpy -Igenpy:`pwd`/test/msg -o src/genpy/msg `pwd`/test/msg/TestMsgArray.msg
./scripts/genmsg_py.py -p genpy -Igenpy:`pwd`/test/msg -o src/genpy/msg `pwd`/test/msg/TestPrimitiveArray.msg
./scripts/genmsg_py.py -p genpy -Igenpy:`pwd`/test/msg -o src/genpy/msg `pwd`/test/msg/TestString.msg
```

## Examples for generating messages with dependencies

```console
./scripts/genmsg_py.py -p std_msgs -Istd_msgs:`rospack find std_msgs`/msg -o gen `rospack find std_msgs`/msg/String.msg
./scripts/genmsg_py.py -p geometry_msgs -Istd_msgs:`rospack find std_msgs`/msg -Igeometry_msgs:`rospack find geometry_msgs`/msg -o gen `rospack find geometry_msgs`/msg/PoseStamped.msg
```
