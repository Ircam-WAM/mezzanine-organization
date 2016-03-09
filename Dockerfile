FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get -y --force-yes install locales netcat pandoc && \
    echo fr_FR.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen

ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

RUN mkdir /srv/app
RUN mkdir /srv/src
WORKDIR /srv/app

ADD requirements.txt /srv/app/
RUN pip install -r requirements.txt

ADD requirements-dev.txt /srv/app/
RUN pip install -r requirements-dev.txt --src /srv/lib
