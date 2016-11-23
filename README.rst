======================
Mezzanine-organization
======================

This application is a CMS dedicated to organizations which is based on Mezzanine and Django.

Architecture
============

For easier development and production workflow, this application has been dockerized.

Paths
++++++

- `app` : django application

 - `app/templates` : main templates
 - `app/locale` : locales

- `data` : all application data versioned on a separate repository

    - `data/media` : all media uploaded through the app
    - `data/var/lib/postgresql` : postgresql DB (not versioned)
    - `data/var/log/nginx` : nginx logs (not versioned)
    - `data/var/log/uwsgi` : uwsgi logs (not versioned)

- `env` : docker-compose environment files
- `etc` : custom config files
- `lib` : custom libraries added as git submodules
- `scripts` : maintenance scripts


Models
++++++



Install
=======

Clone
++++++

On Linux, first install Git_, Docker-engine_ and docker-compose_ and open a terminal.

On MacOSX or Windows install the Docker-Toolbox_ and open a Docker Quickstart Terminal.

Then run these commands::

    git clone --recursive git+ssh://git@git.forge.ircam.fr/ircam-www.git


Compile static files
+++++++++++++++++++++

Gulp allow to compile scss to css, concatenate js files and has a watcher, who do this tasks on file change.
Gulp require nodejs installed on your computer to work.

1. Install gulp globally::

    sudo npm install --g gulp

2. Install bower globally::

    sudo npm install -g bower

3. Install gulp dependencies::

    npm install

4. Install ruby dependencies::

    sudo apt install ruby
    sudo gem install bundler
    bundle install

5. Build::

    bower install
    gulp build


/!\ If you have an issue with ffi module, try to install dev package from ruby::

    apt-get install ruby-dev


Start
+++++

For a production environment setup::

    cd ircam-www
    docker-compose up (it will builds, (re)creates, starts, and attaches to containers for a service.)

Then browse the app at http://localhost:8020/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)


Install as a daemon
+++++++++++++++++++++

Run daemon install script::

    sudo ./install.py


Prod
======

Update prod on master branch::

    ./scripts/upgrade.sh

Backup manually database::

    ./scripts/push.sh (only prod !)


Development
============


Start in dev mode
+++++++++++++++++

For a development environment setup::

    docker-compose -f docker-compose.yml -f env/dev.yml up

Then browse the app at http://localhost:9020/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)


Modify CSS or JS
+++++++++++++++++

1. Installing gulp dependencies::

    See previous section.

2. Run gulp::

    gulp

Gulp will launch BrowserSync. BrowserSync is a middleware that expose the website on port 3000.
Any change on CSS or JS files will trigger the build system and reload the browser.


Maintenance
============

Find logs
+++++++++


Backup / Restore DB
+++++++++++++++++++++

To backup the database, in **another** terminal (or a Docker Quickstart Terminal)::

    cd ircam-www
    scripts/push.sh

giving your user password if asked...

To restore the backuped database, in another terminal (or a Docker Quickstart Terminal)::

    cd ircam-www
    scripts/pull.sh

If the app is broken after a restore script, restart the composition with::

    docker-compose restart


Docker
+++++++

Restart service docker::

 sudo /etc/init.d/docker restart

List containers::

 docker-compose ps

Inspect a container (usefully to know IP of a container)::

 docker inspect [CONTAINER_ID]



.. _Docker-engine: https://docs.docker.com/installation/
.. _docker-compose: https://docs.docker.com/compose/install/
.. _docker-compose reference: https://docs.docker.com/compose/reference/
.. _Docker-Toolbox: https://www.docker.com/products/docker-toolbox
.. _Git: http://git-scm.com/downloads
