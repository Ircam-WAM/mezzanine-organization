#!/bin/sh

# paths
root='/opt/'
sandbox=$root'app/'
manage=$sandbox'manage.py'
wsgi=$sandbox'wsgi.py'
static=$root'static/'
media=$root'media/'

# waiting for other services
sh $sandbox/deploy/wait.sh

# django init
python $manage migrate --noinput
python $manage collectstatic --noinput

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
     --command='python '$manage' collectstatic --noinput' $sandbox &

# app start
uwsgi --socket :8000 --wsgi-file $wsgi --chdir $sandbox --master --processes 4 --threads 2 --py-autoreload 3

#python $manage runserver 0.0.0.0:8000
