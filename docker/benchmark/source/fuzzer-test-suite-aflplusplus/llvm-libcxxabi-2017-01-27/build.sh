#!/bin/bash
# Copyright 2016 Google Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
. $(dirname $0)/../custom-build.sh $1 $2
. $(dirname $0)/../common.sh

get_svn_revision http://llvm.org/svn/llvm-project/libcxxabi/trunk 293329 SRC
build_fuzzer

if [[ $FUZZING_ENGINE == "hooks" ]]; then
  # Link ASan runtime so we can hook memcmp et al.
  LIB_FUZZING_ENGINE="$LIB_FUZZING_ENGINE -fsanitize=address"
fi
$CXX $CXXFLAGS -std=c++11 SRC/fuzz/cxa_demangle_fuzzer.cpp SRC/src/cxa_demangle.cpp -I SRC/include \
   $LIB_FUZZING_ENGINE -o $EXECUTABLE_NAME_BASE-$EXECUTABLE_NAME_EXT
