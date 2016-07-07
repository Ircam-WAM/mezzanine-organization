#!/bin/sh

docker-compose run app /srv/app/manage.py migrate
