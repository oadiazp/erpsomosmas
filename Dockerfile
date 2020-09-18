FROM ubuntu:20.04

MAINTAINER Omar Antonio Diaz <tecnologia@somosmascuba.com.com>

ENV DJANGO_SETTINGS_MODULE manager.settings.live
ENV DEBIAN_FRONTEND noninteractive
ENV TZ Europe/Berlin

RUN apt-get update && apt-get upgrade -y

# Set the locale
RUN apt install -y locales
RUN locale-gen es_US.UTF-8
ENV LANG es_US.UTF-8
ENV LANGUAGE es_US:en
ENV LC_ALL es_US.UTF-8


RUN apt-get install -y  python3-dev \
    build-essential \
    apt-utils \
    python3-dev \
    gcc \
    libpq-dev \
    libffi-dev \
    zlib1g-dev \ 
    libssl-dev \
    libpcre3-dev \
    gettext \
    sudo \
    nginx \
    git \
    nodejs \
    python3-venv \
    npm \
    gettext

RUN mkdir -p /home/docker/src
RUN python3 -m venv /home/docker/venv

WORKDIR /home/docker/src
RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
COPY conf/uwsgi.ini /home/docker/src
COPY conf/uwsgi_params /home/docker/src
COPY conf/nginx.conf /etc/nginx
COPY conf/nginx-app.conf /etc/nginx/sites-enabled

ADD . .

RUN npm install
RUN ln -sf $PWD/node_modules apps/core/static

RUN . /home/docker/venv/bin/activate; \
      pip install -r /home/docker/src/requirements-live.txt;

RUN chown www-data:www-data -R /home/docker


CMD DJANGO_SETTINGS_MODULE=manager.settings.live /home/docker/venv/bin/python /home/docker/src/manage.py createcachetable & \
    DJANGO_SETTINGS_MODULE=manager.settings.live /home/docker/venv/bin/python /home/docker/src/manage.py compilemessages & \
    DJANGO_SETTINGS_MODULE=manager.settings.live /home/docker/venv/bin/python /home/docker/src/manage.py collectstatic --clear --traceback --noinput -v=3 & \
    DJANGO_SETTINGS_MODULE=manager.settings.live /home/docker/venv/bin/python /home/docker/src/manage.py migrate & \
    sudo -Eu www-data /home/docker/venv/bin/uwsgi --ini /home/docker/src/uwsgi.ini & \
    sudo nginx
