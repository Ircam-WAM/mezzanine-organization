#!/bin/sh

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'

# uwsgi params
port=8000
processes=2
threads=2
autoreload=3

# waiting for other services
sh $app/deploy/wait.sh

if [ ! -f $app/.init ]; then
 python $manage telemeta-create-admin-user
 python $manage telemeta-create-boilerplate
 python $manage update_index --workers $processes
 touch $app/.init
fi

# django init
python $manage makemigrations --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
    --processes $processes --threads $threads --py-autoreload $autoreload
