#!/bin/bash

gunzip < /srv/backup/ircam-www.sql.gz | mysql -hdb -uroot -phyRob0otlaz4 ircam-www
echo "Restore done!"
