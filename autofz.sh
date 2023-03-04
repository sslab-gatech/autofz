#!/bin/bash -e

# /work/autofz can be anything
# autofz.sh run --rm -v data:/work/autofz -w /work/autofz autofz

SCRIPT_DIR=$(dirname $(realpath $0))

COMPOSE_FILE=$SCRIPT_DIR/docker-compose.yml

JOBS=${JOBS:=1}

echo "JOBS is ${JOBS}"

docker-compose -f $COMPOSE_FILE "$@"
