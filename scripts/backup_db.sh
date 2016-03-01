#!/bin/bash

mysqldump -hdb -uroot -phyRob0otlaz4 manifeste | gzip > /srv/backup/manifeste.sql.gz
echo "Backup done!"
