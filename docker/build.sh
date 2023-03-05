#!/bin/bash -e
SCRIPT_DIR=$(dirname $(realpath $0))

$SCRIPT_DIR/fuzzer_base/build.sh
$SCRIPT_DIR/benchmark/build.sh

wait
