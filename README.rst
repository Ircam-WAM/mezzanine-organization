================
Manifeste IRCAM
================

This is the new template for the Manifeste festival website at IRCAM. It is based on the Mezzanine CMS which is itself based on Django.


Install
=========

For easier development and production workflow, it has been dockerized including the MariaDB and the Nginx webserver.

First install `Git <http://git-scm.com/downloads>`_, `Docker engine <https://docs.docker.com/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_.


Linux
------

Run these commands in a terminal::

    git clone --recursive git://git.forge.ircam.fr/Manifeste.git
    cd Manifeste
    docker-compose up db

The last command is needed to init the database. Press CTRL-C to exit. Then fire up the whole composition::

     docker-compose up

To restore the backuped database, in another terminal::

    cd Manifeste
    docker-compose run db /srv/backup/restore_db.sh

You should be able to browse the site at http://localhost:9000/


MacOS or Windows:
------------------

Run these commands in a terminal::

    docker-machine create --driver virtualbox --virtualbox-memory 8096 manifeste
    docker-machine manifeste start
    eval "$(docker-machine env manifeste)"
    docker-machine ip manifeste
    git clone --recursive git://git.forge.ircam.fr/Manifeste.git
    cd Manifeste
    docker-compose up

The last command is needed to init the database. Press CTRL-C to exit. Then fire up the whole composition::

    docker-compose up

Then, in another terminal::

    eval "$(docker-machine env manifeste)"
    cd Manifeste
    docker-compose run db /srv/backup/restore_db.sh

`More info <https://docs.docker.com/>`_ about using docker and related tools.
The 3rd command should give you the IP of the VM. For example, if IP is 192.168.59.103, you should be able to browse the site at http://192.168.59.103:8010/
