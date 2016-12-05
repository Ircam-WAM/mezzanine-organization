#!/bin/sh

docker-compose run app bash -c "cd /srv && bower --allow-root install && gulp build"
docker-compose run app python /srv/app/manage.py collectstatic --no-input
