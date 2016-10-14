# genpy

The Python ROS message and service generator.

## Regenerate test messages

```console
./test/scripts/gen_test_messages.sh
```

## Run genpy tests

```console
./test/scripts/run_tests.sh
```

## Examples for generating messages with dependencies

```console
./scripts/genmsg_py.py -p std_msgs -Istd_msgs:`rospack find std_msgs`/msg -o gen `rospack find std_msgs`/msg/String.msg
./scripts/genmsg_py.py -p geometry_msgs -Istd_msgs:`rospack find std_msgs`/msg -Igeometry_msgs:`rospack find geometry_msgs`/msg -o gen `rospack find geometry_msgs`/msg/PoseStamped.msg
```
