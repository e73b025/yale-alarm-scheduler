#!/bin/bash

DOCKER_IMAGE_NAME="yale_alarm_scheduler"

# Build
docker build -t $DOCKER_IMAGE_NAME .

# Run
docker run --rm $DOCKER_IMAGE_NAME