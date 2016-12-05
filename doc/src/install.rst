
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

Run daemon and install cron::

    sudo ./install.py --user=$USER --cron

    You can find logs at /var/log/mezzanine-organization

options::

    --uninstall : uninstall the daemon
    --cron : install cron backup rule (every 6 hours)
    --user : specify user
    --systemd : use systemd
    --composition_file : the path of the YAML composition file to use (optional)

This will install a init script in /etc/init.d. For example, if your app directory is named `mezzanine-organization`, `/etc/init.d/mezzanine-organization` becomes the init script for the OS booting procedure and for you if you need to start the daemon by hand::

    sudo /etc/init.d/mezzanine-organization start


Browsing
+++++++++

Local
-------
- front : http://localhost:9020
- admin: http://localhost:9020/admin

Dev
----
- front : http://cri-dev01.ircam.fr/
- admin : http://cri-dev01.ircam.fr/admin
- ssh : ssh cri@cri-dev01.ircam.fr
- cd /srv/ircam-www

Prod
-----
- front : http://www.ircam.fr
- admin : http://www.ircam.fr/admin
- ssh : ssh cri@www.ircam.fr
- cd /srv/ircam-www


.. _Docker-engine: https://docs.docker.com/installation/
.. _docker-compose: https://docs.docker.com/compose/install/
.. _docker-compose reference: https://docs.docker.com/compose/reference/
.. _Docker-Toolbox: https://www.docker.com/products/docker-toolbox
.. _Git: http://git-scm.com/downloads
.. _NodeJS: https://nodejs.org
.. _Gulp: http://gulpjs.com/
.. _Mezzanine-Agenda : https://github.com/jpells/mezzanine-agenda
.. _Cartridge : https://github.com/stephenmcd/cartridge/
.. _Sass: http://sass-lang.com/
.. _Compass : http://compass-style.org/
