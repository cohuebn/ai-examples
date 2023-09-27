#!/usr/bin/env bash

scriptDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Spin up infrastructure
docker compose -f "$scriptDir/local.docker-compose.yml" up --build \
  --remove-orphans \
  --always-recreate-deps \
  --force-recreate \
  --detach
