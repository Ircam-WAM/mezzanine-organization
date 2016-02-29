#!/bin/bash

export PGPASSWORD="mysecretpassword"
db_exists=`psql -hpgdb -Upostgres -lqt  | cut -d \| -f 1 | grep -w eve | wc -l`

if [ $db_exists == 0 ]; then
    psql -hpgdb -Upostgres -c 'create role eve'
else
    psql -hpgdb -Upostgres  -c 'drop database eve'
fi

psql -hpgdb -Upostgres -c 'create database eve'
gunzip -c /srv/backup/eve.sql.gz | psql -hpgdb -Upostgres -q eve
