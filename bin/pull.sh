#!/bin/sh

sudo chown -R $USER var/media
sudo chown -R $USER var/backup
git pull
git submodule foreach git pull
docker-compose run db /srv/bin/db/restore.sh
gulp build
