#!/bin/bash

docker-compose run db /srv/scripts/backup_db.sh
git add data/media
git commit -a -m "update DB and media"
git push
