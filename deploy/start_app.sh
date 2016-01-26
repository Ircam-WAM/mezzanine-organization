#!/bin/sh

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'

# uwsgi params
port=8000
processes=2
threads=2
autoreload=3
uid='www-data'
gid='www-data'

# Staging
#pip install mezzanine_instagram

chown -R $uid:$gid $media

# waiting for other services
sh $app/deploy/wait.sh

# waiting for available database
python $app/wait.py

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
    --processes $processes --threads $threads \
    --uid $uid --gid $gid \
    --py-autoreload $autoreload
