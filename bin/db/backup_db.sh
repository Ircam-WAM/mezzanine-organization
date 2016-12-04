#!/bin/bash

export PGPASSWORD=$POSTGRES_PASSWORD

pg_dump -Fc -hdb -Upostgres -dpostgres > /srv/backup/ircam-www.dump

echo "Backup done!"
