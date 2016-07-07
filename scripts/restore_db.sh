#!/bin/bash

export PGPASSWORD=$POSTGRES_PASSWORD

pg_restore --clean -Fc -hdb -Upostgres -d postgres /srv/backup/ircam-www.dump

echo "Restore done!"
