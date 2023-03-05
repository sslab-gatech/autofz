#!/bin/bash -e
SCRIPT_DIR=$(dirname $(realpath $0))
export IMAGE_PREFIX=fuzzer_base

fuzzer_list=(
    base
    aflplusplus
    afl
    aflfast
    angora
    mopt
    fairfuzz
    lafintel
    radamsa
    libfuzzer
    learnafl
    redqueen
)

USER=$(id -un)
GID=$(id -g)

if [ ! -z "$NO_CACHE" ]; then
    build_args+=('--no-cache')
fi

pushd .
cd $SCRIPT_DIR/..

if [ ! -z "$1" ]; then
    fuzzer=$1
    if [ -e fuzzer_base/$fuzzer/Dockerfile ]; then
        echo "$fuzzer Dockerfile exists; start build for $fuzzer"
        docker build \
               --build-arg PREFIX=$IMAGE_PREFIX \
               --build-arg USER=$USER \
               --build-arg UID=$UID \
               --build-arg GID=$GID \
               -t $IMAGE_PREFIX/$fuzzer \
               -f fuzzer_base/$fuzzer/Dockerfile \
               "${build_args[@]}" \
               .

    else
        echo "$fuzzer Dockerfile does not exist!"
    fi
else
    for fuzzer in "${fuzzer_list[@]}"
    do
        if [ -e fuzzer_base/$fuzzer/Dockerfile ]; then
            echo "$fuzzer Dockerfile exists; start build for $fuzzer"
            docker build \
                   --build-arg PREFIX=$IMAGE_PREFIX \
                   --build-arg USER=$USER \
                   --build-arg UID=$UID \
                   --build-arg GID=$GID \
                   -t $IMAGE_PREFIX/$fuzzer \
                   -f fuzzer_base/$fuzzer/Dockerfile \
                   "${build_args[@]}" \
                   .
        else
            echo "$fuzzer Dockerfile does not exist!"
        fi
    done
fi

popd

wait
