#!/bin/sh

docker-compose run app bash -c "cd /srv && bower install && gulp build"
