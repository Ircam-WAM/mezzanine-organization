#!/bin/sh

docker-compose stop
mv data var
mkdir var/lib
sudo mv var/postgresql var/lib
sudo mv var/external var/opt
sudo mv var/var/log var
sudo rm -rf var/var
mkdir etc/nginx
mkdir etc/nginx/conf.d/
mv etc/nginx.conf etc/nginx/conf.d/default.conf
mkdir etc/apt
mv etc/sources.list etc/apt/
