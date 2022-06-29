#!/usr/bin/env bash

docker-compose -f /drone/src/docker-compose.yml -f /drone/src/docker-compose.prod.yml config >/drone/src/docker-compose.processed.yml || exit 1
docker stack deploy -c /drone/src/docker-compose.processed.yml maplelegends_vote_reminder || exit 1
