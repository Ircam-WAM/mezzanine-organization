#!/bin/bash

export PGPASSWORD="HmazS2frT"

db_exists=`psql -hpgdb -Ueve -lqt  | cut -d \| -f 1 | grep -w eve | wc -l`

if [ ! $db_exists == 0 ]; then
    psql -hpgdb -Ueve  -c 'drop database eve'
fi

psql -hpgdb -Ueve -c 'create role eve'
psql -hpgdb -Ueve -c 'create role django'
psql -hpgdb -Ueve -c 'create database eve'
gunzip -c /srv/backup/eve.sql.gz | psql -hpgdb -Ueve -q eve
