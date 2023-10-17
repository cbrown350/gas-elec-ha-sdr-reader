#!/bin/sh

python3 -m pip install .
VERSION=$(python3 -m pip show gas-elec-ha-sdr-reader -V | grep Version: | cut -d' ' -f2)
REPO=$(python3 -m pip show gas-elec-ha-sdr-reader -V | grep Home-page: | cut -d' ' -f2)
TAG="ghcr.io/$(echo $REPO | cut -d'/' -f4-)"

# https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
# login-> echo "<personal access token>" | docker login ghcr.io -u USERNAME --password-stdin
docker buildx build --platform linux/amd64,linux/arm64 --label org.opencontainers.image.source=$REPO -t $TAG:$VERSION -t $TAG:latest --push .