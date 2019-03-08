#!/bin/sh

TAG=xift.ai:gpt-2

# Ejecutamos el docker
docker run -ti ${TAG} python3 src/generate_conditional_samples.py "$1"

