#!/bin/bash

IMAGE="dev"
VERSION="latest"

podman build \
    --build-arg UNAME=$(whoami) \
    -f Containerfile -t $IMAGE:$VERSION .
