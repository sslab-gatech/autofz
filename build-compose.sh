#!/bin/bash -ev

export USER=$(id -un)
export UID
export GID=$(id -g)

docker-compose config
docker-compose build
