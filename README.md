# Archived - ROS 1 End-of-life

This repository contains ROS 1 packages.
The last supported ROS 1 release, ROS Noetic, [officially reached end of life on May 31st, 2025](https://bit.ly/NoeticEOL).

# genpy

The Python ROS message and service generator.

## Examples for generating messages with dependencies

```console
./scripts/genmsg_py.py -p std_msgs -Istd_msgs:`rospack find std_msgs`/msg -o gen `rospack find std_msgs`/msg/String.msg
./scripts/genmsg_py.py -p geometry_msgs -Istd_msgs:`rospack find std_msgs`/msg -Igeometry_msgs:`rospack find geometry_msgs`/msg -o gen `rospack find geometry_msgs`/msg/PoseStamped.msg
```
