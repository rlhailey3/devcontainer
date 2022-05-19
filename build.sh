#!/bin/bash

IMAGE="dev"
VERSION="latest"


podman build \
    --build-arg UNAME=$(whoami) \
    -f Containerfile -t $IMAGE:$VERSION .


#podman build \
#    --build-arg UNAME=$(whoami) \
#    --build-arg UID=$(id -u) \
#    --build-arg GID=$(id -g) \
#    -f Containerfile -t $IMAGE:$VERSION .
