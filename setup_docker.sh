#!/bin/sh

TAG=xift.ai:gpt-2
VERSION=cpu

# Descargamos el modelo si no está descargado con anterioridad
if [ ! -d models ];
then
  sh download_model.sh 117M
fi

# Creamos el contenedor 
docker build --file Dockerfile.${VERSION} --tag ${TAG} .

