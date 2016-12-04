#!/bin/bash

export PGPASSWORD=$POSTGRES_PASSWORD

pg_restore -c -Fc -hdb -Upostgres -dpostgres /srv/backup/ircam-www.dump

echo "Restore done!"
