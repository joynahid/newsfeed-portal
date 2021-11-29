#!/bin/bash

docker-compose up -d --build djangoapp
sleep 5s
docker exec djangoapp /scripts/make.sh
docker-compose down