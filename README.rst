======================
Mezzanine-organization
======================

Overview
=========

This application is a CMS dedicated to organizations which is based on Mezzanine and Django.

Usecases


Architecture
============

For easier development and production workflow, this application has been dockerized.

Paths
++++++

- `app` : django application

 - `app/templates` : main templates
 - `app/locale` : locales

- `data` : all application data versioned on a separated repository

    - `data/backup` : database backup directory
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

app/organization

- agenda
- core
...



Install
=======

Clone
++++++

On Linux, first install Git_, Docker-engine_ and docker-compose_ and open a terminal.

On MacOS or Windows install Git_ and the Docker-Toolbox_ and open a Docker Quickstart Terminal.

Then run these commands::

    git clone --recursive https://github.com/Ircam-RnD/mezzanine-organization.git


Compile static files
+++++++++++++++++++++

Gulp_ allow to compile scss to css, concatenate js files and has a watcher, who do this tasks on file change.
Gulp_ require NodeJS_ installed on your computer to work.

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

    cd mezzanine-organization
    docker-compose up

which builds, (re)creates, starts, and attaches to containers.

Then browse the app at http://localhost:8020/

On MacOS or Windows, we need to replace 'localhost' by the IP given by the docker terminal.


Install as a daemon
+++++++++++++++++++++

Run daemon install script::

    sudo ./install.py

This will install a init script in /etc/init.d. For example, if your app directory is named `mezzanine-organization`, `/etc/init.d/mezzanine-organization` becomes the init script for the OS booting procedure and for you if you need to start the daemon by hand::

    sudo /etc/init.d/mezzanine-organization start


Development
============


Start in dev mode
+++++++++++++++++

For a development environment setup::

    docker-compose -f docker-compose.yml -f env/dev.yml up

Then browse the app at http://localhost:9020/

On MacOS or Windows, we need to replace 'localhost' by the IP given by the docker terminal.

In this mode, Django is run with the `runserver` tool in DEBUG mode. NEVER use this in production!


Back
+++++

If you modify or add django models, you can produce migration files with::

    ./scripts/makemigrations.sh

To apply new migrations::

    ./scripts/migrate.sh

Accessing the app container shell::

    docker-compose run app bash


Front
+++++

1. Installing gulp dependencies::

    See previous section: "Compile static files".

2. Run gulp::

    gulp

Gulp will launch BrowserSync. BrowserSync is a middleware that expose the website on port 3000.
Any change on CSS or JS files will trigger the build system and reload the browser.


Maintenance
============

Find logs
+++++++++

- `data/var/log/nginx/app-access.log` : nginx access log of the app
- `data/var/log/nginx/app-error.log` : nginx error log of the app
- `data/var/log/uwsgi/app.log` : uwsgi log of the app


Upgrade
+++++++++

Upgrade application, all dependencies, data from master branch and also recompile assets::

    scripts/upgrade.sh


Backup / Restore database
++++++++++++++++++++++++++

To backup the database, in **another** terminal (or a Docker Quickstart Terminal)::

    scripts/push.sh #(only prod !)

giving your user password if asked...

To restore the backuped database, in another terminal (or a Docker Quickstart Terminal)::

    scripts/pull.sh


In case of broken app
++++++++++++++++++++++

For all commands run un this section, you need to be in the app directory::

    cd mezzanine-organization

If the app is not accessible, first try to restart the composition with::

    docker-compose restart

If the app is not responding yet, try to restart the docker service and then the app::

    docker-compose stop
    sudo /etc/init.d/docker restart
    docker-compose up

If the containers are still broken, try to delete exisiting containers (this will NOT delete critical data as database or media)::

    docker-compose stop
    docker-compose rm
    docker-compose up

In case you have installed the init script to run the app as a daemon (cf. section "Install as a daemon"), you can use it to restart the app:

    /etc/init.d/mezzanine-organization restart

If you need more informations about running containers::

    docker-compose ps

Or more, inspecting any container of the composition (usefully to know IP of a container)::

    docker inspect [CONTAINER_ID]


Copyrights
==========

* Copyright (c) 2016 Ircam
* Copyright (c) 2016 Guillaume Pellerin
* Copyright (c) 2016 Emilie Zawadzki
* Copyright (c) 2016 Jérémy Fabre


License
========

mezzanine-organization is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

mezzanine-organization is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

Read the LICENSE.txt file for more details.



.. _Docker-engine: https://docs.docker.com/installation/
.. _docker-compose: https://docs.docker.com/compose/install/
.. _docker-compose reference: https://docs.docker.com/compose/reference/
.. _Docker-Toolbox: https://www.docker.com/products/docker-toolbox
.. _Git: http://git-scm.com/downloads
.. _NodeJS: https://nodejs.org
.. _Gulp: http://gulpjs.com/
