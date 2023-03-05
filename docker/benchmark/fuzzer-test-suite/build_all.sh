#!/bin/bash

FTS_DIR=/autofz_bench/fuzzer-test-suite

targets=(
    boringssl-2016-02-12
    c-ares-CVE-2016-5180
    freetype2-2017
    guetzli-2017-3-30
    harfbuzz-1.3.2
    json-2017-02-12
    lcms-2017-03-21
    libarchive-2017-01-04
    libjpeg-turbo-07-2017
    libpng-1.2.56
    libssh-2017-1272
    libxml2-v2.9.2
    # llvm-libcxxabi-2017-01-27
    openssl-1.0.1f
    openssl-1.0.2d
    openssl-1.1.0c
    openthread-2018-02-27
    pcre2-10.00
    proj4-2017-08-14
    re2-2014-12-09
    sqlite-2016-11-14
    vorbis-2017-12-11
    woff2-2016-05-06
    wpantund-2018-02-27
)
mkdir -p /d/p/justafl /d/p/aflasan /d/p/normal /d/p/cov
BUILD_DIR=/autofz_bench/fuzzer-test-suite-build
mkdir -p $BUILD_DIR /autofz_bench/fuzzer-test-suite-seeds

cd $BUILD_DIR

FTS_DIR=/autofz_bench/fuzzer-test-suite

JOBS="-l$(nproc)" # make -j
export JOBS

for target in ${targets[@]};
do
    {
        # build with asan off
        CC=clang
        CXX=clang++
        CFLAGS='-O2 -fno-omit-frame-pointer -fsanitize-coverage=trace-pc-guard,trace-cmp,trace-gep,trace-div'
        CXXFLAGS="$CFLAGS -stdlib=libc++"
        FUZZING_ENGINE=afl
        AFL_SRC=/fuzzer/afl
        LIBFUZZER_SRC=/llvm/compiler-rt-12.0.0.src/lib/fuzzer/
        export CC CXX CFLAGS CXXFLAGS FUZZING_ENGINE AFL_SRC LIBFUZZER_SRC
        BUILD_SCRIPT=$FTS_DIR/$target/build.sh
        RUNDIR="$target"
        mkdir -p $RUNDIR
        pushd .
        cd $RUNDIR
        $BUILD_SCRIPT > /dev/null
        for EXECUTABLE in $target*-out*;
        do
            NEW_NAME=${EXECUTABLE%-out*}
            NEW_DIR=/d/p/justafl/fuzzer-test-suite/$NEW_NAME
            NEW_PATH=$NEW_DIR/$NEW_NAME
            mkdir -p $NEW_DIR
            mv $EXECUTABLE $NEW_PATH
        done
        popd

        # build with asan on
        CC=clang
        CXX=clang++
        CFLAGS='-O2 -fno-omit-frame-pointer -fsanitize=address -fsanitize-address-use-after-scope -fsanitize-coverage=trace-pc-guard,trace-cmp,trace-gep,trace-div'
        CXXFLAGS="$CFLAGS -stdlib=libc++"
        FUZZING_ENGINE=afl
        AFL_SRC=/fuzzer/afl
        LIBFUZZER_SRC=/llvm/compiler-rt-12.0.0.src/lib/fuzzer/
        export CC CXX CFLAGS CXXFLAGS FUZZING_ENGINE AFL_SRC LIBFUZZER_SRC
        BUILD_SCRIPT=$FTS_DIR/$target/build.sh
        RUNDIR="$target"
        mkdir -p $RUNDIR
        pushd .
        cd $RUNDIR
        $BUILD_SCRIPT > /dev/null
        for EXECUTABLE in $target*-out*;
        do
            NEW_NAME=${EXECUTABLE%-out*}
            NEW_DIR=/d/p/aflasan/fuzzer-test-suite/$NEW_NAME
            NEW_PATH=$NEW_DIR/$NEW_NAME
            mkdir -p $NEW_DIR
            mv $EXECUTABLE $NEW_PATH
        done
        popd
        # build normal binary
        CC=clang
        CXX=clang++
        CFLAGS='-O2 -fno-omit-frame-pointer'
        CXXFLAGS="$CFLAGS -stdlib=libc++"
        FUZZING_ENGINE=coverage
        AFL_SRC=/fuzzer/afl
        LIBFUZZER_SRC=/llvm/compiler-rt-12.0.0.src/lib/fuzzer/
        export CC CXX CFLAGS CXXFLAGS FUZZING_ENGINE AFL_SRC LIBFUZZER_SRC
        BUILD_SCRIPT=$FTS_DIR/$target/build.sh
        RUNDIR="$target"
        mkdir -p $RUNDIR
        pushd .
        cd $RUNDIR
        $BUILD_SCRIPT > /dev/null
        for EXECUTABLE in $target*-out*;
        do
            NEW_NAME=${EXECUTABLE%-out*}
            NEW_DIR=/d/p/normal/fuzzer-test-suite/$NEW_NAME
            NEW_PATH=$NEW_DIR/$NEW_NAME
            mkdir -p $NEW_DIR
            mv $EXECUTABLE $NEW_PATH
        done
        popd
    } &
done
wait

for target in ${targets[@]};
do
    {
        echo "build $target"
        RUNDIR="$target"
        mkdir -p $RUNDIR
        # build normal binary
        CC=clang
        CXX=clang++
        CFLAGS='-fprofile-arcs -ftest-coverage'
        CXXFLAGS="$CFLAGS -stdlib=libc++"
        FUZZING_ENGINE=coverage
        AFL_SRC=/fuzzer/afl
        LIBFUZZER_SRC=/llvm/compiler-rt-12.0.0.src/lib/fuzzer/
        export CC CXX CFLAGS CXXFLAGS FUZZING_ENGINE AFL_SRC LIBFUZZER_SRC
        BUILD_SCRIPT=$FTS_DIR/$target/build.sh
        RUNDIR="$target"
        mkdir -p $RUNDIR
        pushd .
        cd $RUNDIR
        $BUILD_SCRIPT > /dev/null
        for EXECUTABLE in $target*-out*;
        do
            NEW_NAME=${EXECUTABLE%-out*}
            NEW_DIR=/d/p/cov/fuzzer-test-suite/$NEW_NAME
            NEW_PATH=$NEW_DIR/$NEW_NAME
            mkdir -p $NEW_DIR
            mv $EXECUTABLE $NEW_PATH
        done
        popd
    } &
done
wait

cp -r $BUILD_DIR/openssl-1.0.1f/runtime /d/p/justafl/fuzzer-test-suite/openssl-1.0.1f/
cp -r $BUILD_DIR/openssl-1.0.1f/runtime /d/p/aflasan/fuzzer-test-suite/openssl-1.0.1f/
cp -r $BUILD_DIR/openssl-1.0.1f/runtime /d/p/normal/fuzzer-test-suite/openssl-1.0.1f/
cp -r $BUILD_DIR/openssl-1.0.1f/runtime /d/p/cov/fuzzer-test-suite/openssl-1.0.1f/


ls -alh /d/p/*
