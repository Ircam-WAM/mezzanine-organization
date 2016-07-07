#!/bin/sh

docker-compose run app /srv/app/manage.py makemigrations
