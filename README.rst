================
Manifeste IRCAM
================

This is the new template for the Manifeste festival website at IRCAM. It is based on the Mezzanine CMS which is itself based on Django.


Install
=======

For easier development and production workflow, it has been dockerized including Django, Mezzanine, MariaDB and Nginx.

On Linux, first install `Git <http://git-scm.com/downloads>`_, `Docker engine <https://docs.docker.com/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_ and open a terminal.

On MacOSX or Windows install the `Docker Toolbox <https://www.docker.com/products/docker-toolbox>`_ and open a Docker Quickstart Terminal.

Then run these commands::

    git --recursive clone git://git@git.forge.ircam.fr/Manifeste.git
    cd Manifeste
    docker-compose up db

Press CTRL-C to exit (the last command is needed to init the database).


Start
=====

For a production environment setup::

     docker-compose up

Then browse the app at http://localhost:8010/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)

For a development environment setup::

    docker-compose -f docker-compose.yml -f conf/dev.yml up

Then browse the app at http://localhost:9010/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)


Backup / Restore
================

To backup the database, in another terminal (or a Docker Quickstart Terminal)::

    cd Manifeste
    scripts/backup.sh

giving your user password if asked...

To restore the backuped database, in another terminal (or a Docker Quickstart Terminal)::

    cd Manifeste
    scripts/restore.sh

If the app is broken after a restore script, restart the machine with::

    docker-compose restart


Work with gulp
==================

Gulp allow to compile scss to css, concatenate js files and has a watcher, who do this tasks on file change.
Gulp require nodejs installed on your computer to work.

- 1. Install gulp globally:
__If you have previously installed a version of gulp globally, please run `npm rm --global gulp`
to make sure your old version doesn't collide with gulp-cli.__

```
$ npm install --global gulp-cli
```

- 2. Install gulp dependancies

```
$ npm install
```

- 3. Run gulp:

```sh
$ gulp [task]
```

Paths
============

- `app/templates` : Main templates
- `app/festival/templates` : Personal templates
- `app/festival/static` : Static files
