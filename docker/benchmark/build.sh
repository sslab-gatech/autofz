#!/bin/bash -e
SCRIPT_DIR=$(dirname $(realpath $0))
IMAGE_PREFIX=autofz_bench
FUZZER_PREFIX=fuzzer_base

# NOTE: order is important becasue of dependencies between Dockerfile
fuzzer_list=(
    fuzzer-test-suite
    fuzzer-test-suite-angora
    fuzzer-test-suite-libfuzzer
    fuzzer-test-suite-aflplusplus
    fuzzer-test-suite-lafintel
    aflplusplus
    afl
    gcc
    coverage
    # aflfast
    # mopt
    # qsym
    angora
    # fairfuzz
    libfuzzer
    radamsa
    redqueen
    # learnafl
    lafintel
)

pushd .
cd $SCRIPT_DIR

build_args=()

if [ ! -z "$NO_CACHE" ]; then
    build_args+=('--no-cache')
fi

if [ ! -z "$1" ]; then
    fuzzer=$1
    if [ -e $fuzzer/Dockerfile ]; then
        echo "$fuzzer Dockerfile exists; start build for $fuzzer"
        docker build \
               --build-arg FUZZER_PREFIX=$FUZZER_PREFIX \
               --build-arg BENCHMARK_PREFIX=$IMAGE_PREFIX \
               -t $IMAGE_PREFIX/$fuzzer \
               -f $fuzzer/Dockerfile \
               "${build_args[@]}" \
               .
    else
        echo "$fuzzer Dockerfile does not exist!"
        exit 1
    fi
else
    for fuzzer in "${fuzzer_list[@]}"
    do
        if [ -e $fuzzer/Dockerfile ]; then
            echo "$fuzzer Dockerfile exists; start build for $fuzzer"
            docker build \
                   --build-arg FUZZER_PREFIX=$FUZZER_PREFIX \
                   --build-arg BENCHMARK_PREFIX=$IMAGE_PREFIX \
                   -t $IMAGE_PREFIX/$fuzzer \
                   -f $fuzzer/Dockerfile \
                   "${build_args[@]}" \
                   .
        else
            echo "$fuzzer Dockerfile does not exist!"
            exit 1
        fi
    done
fi

popd

wait
