#!/bin/bash

SRC=`basename $1`
LIB_NAME=lib${SRC%%.*}.so
LATEST_LIB=`find . -name "$LIB_NAME*" | sort -V -r | head -1`

if [ -n "$LATEST_LIB" ]
then
   if [ `stat -c %Y $SRC` -le `stat -c %Y $LATEST_LIB` ]
   then
      echo "nothing to build"
      exit
   fi
   EXT=${LATEST_LIB##*.}
   if [ $EXT == "so" ]
   then
      let EXT=1
   else
      let EXT=EXT+1
   fi
   LIB_NAME=$LIB_NAME.$EXT
fi

gcc -O3 -shared -fPIC -I/usr/include/libxml2 -I$XROAD_ROOT_DIR/sdk/include $1 -o $LIB_NAME
