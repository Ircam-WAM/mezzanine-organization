#!/bin/sh

docker-compose run app python /srv/app/manage.py makemigrations $1
