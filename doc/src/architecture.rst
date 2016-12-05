
Architecture
============

For easier development and production workflow, this application has been dockerized.

Paths
++++++

- app \
    django application

  - app/locale \
        locales for translations
  - app/migrations \
        mezzanine migrations
  - app/organization \
        organization app
  - app/bin \
        commands to run app with docker
  - app/static \
        all assets, js, css files
  - app/templates \
        main templates

- bin \
    maintenance bin
- env \
    docker-compose environment files
- etc \
    custom config files
- lib \
    custom libraries added as git submodules
- var \
    all application data versioned on a separated repository

  - var/backup \
        database backup directory
  - var/media \
        all media uploaded through the app
  - var/lib/postgresql \
        postgresql DB (not versioned)
  - var/log/nginx \
        nginx logs (not versioned)
  - var/log/uwsgi \
        uwsgi logs (not versioned)

- bower.json \
    javascript dependencies
- debian-requirements.txt \
    used by docker to install debian packages
- docker-compose.yml \
    configuration file for docker containers used by docker-compose
- Dockerfile \
    instructions to build the app image
- Gemfile \
    gem dependecies for ruby. For our case, it will install _Sass and _Compass.
- gulpfile.js \
    script to compile all CSS and JS files
- install.py \
    daemon and init boot script installer (Linux only)
- package.json \
    gulp dependencies when running "gulp install"
- requirements-dev.txt \
    application package in dev version
- requirements.txt \
    application package



Models
++++++

Main modules embed in app/organization

- agenda \
    manage events, using _Mezzanine-Agenda
- core \
    commons or abstract functionnality
- formats \
    manage date format
- job \
    jobs and candidacies for residency
- magazine \
    all news are managed by topics, articles and briefs
- media \
    audio and video gathered in playlist
- network \
    create a tree of Organizations > Departments > Teams > Persons
- pages \
    managing diffent type of pages (admin/pages/page/) and home
- projects \
    represent projects related to a team or a person
- shop \
    manage product from prestashop (softwares and subscriptions), using _Cartridge


.. _Compass : http://compass-style.org/
.. _Sass: http://sass-lang.com/
