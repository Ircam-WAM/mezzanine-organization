#!/bin/sh

docker-compose run app bash -c "cd /srv && bower --allow-root install && gulp build"
