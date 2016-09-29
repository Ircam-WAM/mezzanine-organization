=========
WWW IRCAM
=========

This is the new IRCAM www website. It is based on the Mezzanine CMS which is itself based on Django.


Install
=======

For easier development and production workflow, it has been dockerized including Django, Mezzanine, MariaDB and Nginx.

On Linux, first install Git_, Docker-engine_ and docker-compose_ and open a terminal.

On MacOSX or Windows install the Docker-Toolbox_ and open a Docker Quickstart Terminal.

Then run these commands::

    git clone --recursive git+ssh://git@git.forge.ircam.fr/ircam-www.git
    cd ircam-www
    docker-compose up db

Press CTRL-C to exit (the last command is needed to init the database).


Start
=====

For a production environment setup::

     docker-compose up

Then browse the app at http://localhost:8020/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)

For a development environment setup::

    docker-compose -f docker-compose.yml -f env/dev.yml up

Then browse the app at http://localhost:9020/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)


Backup / Restore
================

To backup the database, in **another** terminal (or a Docker Quickstart Terminal)::

    cd ircam-www
    scripts/push.sh

giving your user password if asked...

To restore the backuped database, in another terminal (or a Docker Quickstart Terminal)::

    cd ircam-www
    scripts/pull.sh

If the app is broken after a restore script, restart the composition with::

    docker-compose restart


Installing dependencies
==================

Gulp allow to compile scss to css, concatenate js files and has a watcher, who do this tasks on file change.
Gulp require nodejs installed on your computer to work.

1. Install gulp globally:

    sudo npm install --g gulp

2. Install bower globally:

    sudo npm install -g bower

3. Install gulp dependencies::

    npm install

4. Install ruby dependencies::

    sudo apt install ruby
    sudo gem install bundler
    bundle install


/!\ If you have an issue with ffi module, try to install dev package from ruby:
apt-get install ruby-dev

Compile static files
==================

Static files are not included in Git. You need to compile them locally.

1. Installing gulp dependencies::

  See previous section.

2. Fetching Bower components::

    bower install

3. Run gulp::

    gulp build


Paths
======

- `app/templates` : Main templates
- `app/festival/templates` : Personal templates
- `app/festival/static` : Static files

.. _Git: http://git-scm.com/downloads
.. _Docker-engine: https://docs.docker.com/installation/
.. _docker-compose: https://docs.docker.com/compose/install/
.. _Docker-Toolbox: https://www.docker.com/products/docker-toolbox
