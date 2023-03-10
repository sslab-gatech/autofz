#!/bin/bash
# Copyright 2016 Google Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
. $(dirname $0)/../custom-build.sh $1 $2
. $(dirname $0)/../common.sh

get_git_revision https://github.com/behdad/harfbuzz.git  f73a87d9a8c76a181794b74b527ea268048f78e3 SRC

build_lib() {
  rm -rf BUILD
  cp -rf SRC BUILD
  (cd BUILD && ./autogen.sh && CCLD="$CXX $CXXFLAGS" ./configure --enable-static --disable-shared &&
    make -j $JOBS -C src fuzzing)
}

build_lib
build_fuzzer

if [[ ! -d seeds ]]; then
  mkdir seeds
  cp BUILD/test/shaping/fonts/sha1sum/* seeds/
fi

if [[ $FUZZING_ENGINE == "hooks" ]]; then
  # Link ASan runtime so we can hook memcmp et al.
  LIB_FUZZING_ENGINE="$LIB_FUZZING_ENGINE -fsanitize=address"
fi
set -x
$CXX $CXXFLAGS -std=c++11 -I BUILD/src/ BUILD/test/fuzzing/hb-fuzzer.cc BUILD/src/.libs/libharfbuzz-fuzzing.a $LIB_FUZZING_ENGINE -lglib-2.0 -o $EXECUTABLE_NAME_BASE-$EXECUTABLE_NAME_EXT
