#!/bin/sh

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'

# uwsgi params
port=8000
processes=2
threads=2
autoreload=3
uid='www-data'
gid='www-data'
patterns='*.js,*.css,*.jpg,*.jpeg,*.gif,*.png,*.svg,*.ttf,*.eot,*.woff,*.woff2'

# Staging
# pip install psycopg2

chown -R $uid:$gid $media

# waiting for other services
sh $app/deploy/wait.sh

# waiting for available database
# python $app/wait.py
# python $manage wait-for-db-connection

# django init
# python $manage syncdb --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput
python $manage create-admin-user

# app start
if [ $1 = "--runserver" ]
then
    python $manage runserver 0.0.0.0:9000
else
    # static files auto update
    watchmedo shell-command --patterns="$patterns" --recursive \
        --command='python '$manage' collectstatic --noinput' $app &

    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
    --processes $processes --threads $threads \
    --uid $uid --gid $gid \
    --py-autoreload $autoreload
fi
