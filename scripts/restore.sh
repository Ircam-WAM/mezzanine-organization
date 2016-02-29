#!/bin/sh

sudo chown -R $USER ../data/media
sudo chown -R $USER ../data/backup
git pull
docker-compose run db /srv/scripts/restore_db.sh
