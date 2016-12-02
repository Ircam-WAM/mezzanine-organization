FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /srv/app
RUN mkdir /srv/lib
WORKDIR /srv/app

RUN apt-get update && apt-get install apt-transport-https
COPY etc/apt/sources.list /etc/apt/
COPY debian-requirements.txt /srv/app/
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" debian-requirements.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    echo fr_FR.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen && \
    apt-get clean

ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

ADD requirements.txt /srv/app/
RUN pip install -r requirements.txt

ADD requirements-dev.txt /srv/app/
RUN pip install -r requirements-dev.txt --src /srv/lib

RUN npm install -g bower
