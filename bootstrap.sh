#!/bin/sh
pkgin in build-essential unzip py27-pip patchelf
pip install --egg esky bbfreeze

OLD=$(pwd)
cd /tmp
curl -kO 'https://pypi.python.org/packages/source/b/bbfreeze-loader/bbfreeze-loader-1.1.0.zip'
unzip bbfreeze-loader-1.1.0.zip

COMPILE="gcc -fno-strict-aliasing -O2 -pipe -O2 -DHAVE_DB_185_H -I/usr/include -I/opt/local/include -I/opt/local/include/db4 -I/opt/local/include/gettext -I/opt/local/include/ncurses -DNDEBUG -O2 -pipe -O2 -DHAVE_DB_185_H -I/usr/include -I/opt/local/include -I/opt/local/include/db4 -I/opt/local/include/gettext -I/opt/local/include/ncurses -fPIC -I/opt/local/include/python2.7 -static-libgcc"
$COMPILE -c bbfreeze-loader-1.1.0/_bbfreeze_loader/console.c -o /tmp/console.o
$COMPILE -c bbfreeze-loader-1.1.0/_bbfreeze_loader/getpath.c -o /tmp/getpath.o
gcc /tmp/console.o /tmp/getpath.o /opt/local/lib/python2.7/config/libpython2.7.a -L/opt/local/lib -L/opt/local/lib/python2.7/config -L/opt/local/lib -lsocket -lnsl -ldl -lrt -lm -static-libgcc -o /tmp/console.exe
patchelf --set-rpath '$ORIGIN:$ORIGIN/../lib' /tmp/console.exe

find /opt/local -name console.exe -exec mv /tmp/console.exe {} \;
cd ${OLD}
