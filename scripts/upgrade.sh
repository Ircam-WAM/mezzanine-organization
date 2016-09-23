#!/bin/sh

# Use this script to update a dev/prod server

git pull origin dev
git submodule update --init --recursive
git submodule foreach git pull origin master
docker-compose run app python /srv/app/manage.py migrate  --noinput
bower install
gulp build
docker-compose run app python /srv/app/manage.py collectstatic --noinput
