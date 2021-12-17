#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/gogochiou/NTHUproject_ws/src/navigation/base_local_planner"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/gogochiou/NTHUproject_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/gogochiou/NTHUproject_ws/install/lib/python2.7/dist-packages:/home/gogochiou/NTHUproject_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/gogochiou/NTHUproject_ws/build" \
    "/usr/bin/python2" \
    "/home/gogochiou/NTHUproject_ws/src/navigation/base_local_planner/setup.py" \
     \
    build --build-base "/home/gogochiou/NTHUproject_ws/build/navigation/base_local_planner" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/gogochiou/NTHUproject_ws/install" --install-scripts="/home/gogochiou/NTHUproject_ws/install/bin"
