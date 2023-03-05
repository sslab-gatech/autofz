#!/bin/bash -e
SCRIPT_DIR=$(dirname $(realpath $0))
IMAGE_PREFIX=autofz
BENCHMARK_PREFIX=autofz_bench

USER=autofz

# hard code UID and GID to bypass docker volumn permission issue
# you might need to change your own UID/GID to 2000
# this is used in the prebuilt docker image
_UID=2000 #_UID is used here because UID is read-only variable in shell
GID=2000

# Use this one to use your own GID; UID is set by SHELL
# _UID=$UID
# GID=$(id -g)

build_args=()

if [ ! -z "$NO_CACHE" ]; then
    build_args+=('--no-cache')
fi

if [ -e $SCRIPT_DIR/Dockerfile ]; then
    docker build \
            --build-arg BENCHMARK_PREFIX=$BENCHMARK_PREFIX \
            --build-arg USER=$USER \
            --build-arg UID=$_UID \
            --build-arg GID=$GID \
            -t autofz \
            -f $SCRIPT_DIR/Dockerfile \
            "${build_args[@]}" \
            .
else
    echo "Dockerfile does not exist!"
    exit 1
fi
