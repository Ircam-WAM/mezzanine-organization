================
Manifeste IRCAM
================

This is the new template for the Manifeste festival website at IRCAM. It is based on the Mezzanine CMS which is itself based on Django.


Install
=========

For easier development and production workflow, it has been dockerized including Django, Mezzanine, MariaDB and Nginx.

On Linux, first install `Git <http://git-scm.com/downloads>`_, `Docker engine <https://docs.docker.com/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_ and open a terminal.

On MacOSX or Windows install the `Docker Toolbox <https://www.docker.com/products/docker-toolbox>`_ and open a Docker Quickstart Terminal.

Then run these commands::

    git clone git://git.forge.ircam.fr/Manifeste.git
    cd Manifeste
    docker-compose up db

The last command is needed to init the database. Press CTRL-C to exit, then fire up the whole composition::

     docker-compose up

Restore the backuped database, in another terminal (or a Docker Quickstart Terminal)::

    cd Manifeste
    ./scripts/restore.sh

Give you user password if asked.

You should be able to browse the app at http://localhost:8010/ (replacing 'localhost' by the IP given by the docker terminal on OSX and Windows)
