
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
    javascript dependencies (cf `Front`_ section)
- debian-requirements.txt \
    used by docker to install debian packages (cf `In case of broken app`_ section)
- docker-compose.yml \
    description of all docker containers. This file is used by command "docker-compose" (cf `In case of broken app`_ section)
- Dockerfile \
    instructions to build app image (cf `In case of broken app`_ section)
- Gemfile \
    gem dependecies for ruby. For our case, it will install _Sass and _Compass. (cf `Front`_ section)
- gulpfile.js \
    script to compile all css, js files (cf `Front`_ section)
- install.py \
    cf section 'Install as a daemon' (cf `Install as a daemon`_ section)
- package.json \
    gulp dependencies when running "gulp install" (cf `Front`_ section)
- requirements-dev.txt \
    application package in dev version (cf `In case of broken app`_ section)
- requirements.txt \
    application package (cf `In case of broken app`_ section)



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
