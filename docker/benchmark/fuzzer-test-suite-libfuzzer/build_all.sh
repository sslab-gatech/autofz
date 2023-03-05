#!/bin/bash -e

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
 #   llvm-libcxxabi-2017-01-27
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
mkdir -p /d/p/libfuzzer
BUILD_DIR=/autofz_bench/fuzzer-test-suite-build
mkdir -p $BUILD_DIR

cd $BUILD_DIR

FTS_DIR=/autofz_bench/fuzzer-test-suite

JOBS=" " # make -j
export JOBS


# NOTE: make it work ubuntu 16.04 host
export ASAN_OPTIONS=detect_leaks=0

for target in ${targets[@]};
do
    {
        CC=clang
        CXX=clang++
        LIBFUZZER_SRC=/fuzzer/libfuzzer/llvm-project/compiler-rt/lib/fuzzer/
        FUZZING_ENGINE=fsanitize_fuzzer
        export CC CXX FUZZING_ENGINE LIBFUZZER_SRC
        BUILD_SCRIPT=$FTS_DIR/$target/build.sh
        RUNDIR="$target"
        mkdir -p $RUNDIR
        pushd .
        cd $RUNDIR
        $BUILD_SCRIPT > /dev/null
        for EXECUTABLE in $target*-out*;
        do
            NEW_NAME=${EXECUTABLE%-out*}
            NEW_DIR=/d/p/libfuzzer/fuzzer-test-suite/$NEW_NAME
            NEW_PATH=$NEW_DIR/$NEW_NAME
            mkdir -p $NEW_DIR
            mv $EXECUTABLE $NEW_PATH
        done
        popd
    } &
done
wait



ls -alh /d/p/*
cp -r $BUILD_DIR/openssl-1.0.1f/runtime /d/p/libfuzzer/fuzzer-test-suite/openssl-1.0.1f/
