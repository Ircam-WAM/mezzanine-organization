#!/bin/bash

gunzip < /srv/backup/manifeste.sql.gz | mysql -hdb -uroot -phyRob0otlaz4 manifeste
echo "Restore done!"
