#!/bin/bash
# Copyright 2016 Google Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
. $(dirname $0)/../custom-build.sh $1 $2
. $(dirname $0)/../common.sh

build_lib() {
  rm -rf BUILD
  cp -rf SRC BUILD
  (cd BUILD && CC="$CC $CFLAGS" ./config && make clean && make -j $JOBS)
}

get_git_tag https://github.com/openssl/openssl.git OpenSSL_1_0_2d SRC
build_lib
build_fuzzer

if [[ $FUZZING_ENGINE == "hooks" ]]; then
  # Link ASan runtime so we can hook memcmp et al.
  LIB_FUZZING_ENGINE="$LIB_FUZZING_ENGINE -fsanitize=address"
fi
set -x
$CXX $CXXFLAGS $SCRIPT_DIR/target.cc -DCERT_PATH=\"$SCRIPT_DIR/\"  BUILD/libssl.a BUILD/libcrypto.a $LIB_FUZZING_ENGINE -lgcrypt -I BUILD/include -o $EXECUTABLE_NAME_BASE-$EXECUTABLE_NAME_EXT
