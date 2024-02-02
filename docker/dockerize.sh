#!/bin/sh

DIR="$(dirname "$(readlink -f "$0")")"
VERSION=$(cat ${DIR}/version)

build() {
  echo "Start build ${VERSION}"

  docker build \
    -t ${GITHUB_REPOSITORY}:${VERSION} \
    -t ${GITHUB_REPOSITORY}:latest \
    -f ${DIR}/Dockerfile ${DIR}/..
}

push() {
  echo "Pushing ${VERSION}"

  docker push ${GITHUB_REPOSITORY}:${VERSION}
  docker push ${GITHUB_REPOSITORY}:latest
}

clean() {
  echo "Cleaning ${VERSION}"

  docker rmi ${GITHUB_REPOSITORY}:${VERSION}
  docker rmi ${GITHUB_REPOSITORY}:latest
}

$1
