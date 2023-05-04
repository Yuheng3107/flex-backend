# Backend for Flex Application

![Django CI Tests Status](https://github.com/Yuheng3107/flex-backend/actions/workflows/django.yml/badge.svg?branch=dev)
[![Docker Image CD Pipeline](https://github.com/Yuheng3107/flex-backend/actions/workflows/docker-image.yml/badge.svg?branch=prod)](https://github.com/Yuheng3107/flex-backend/actions/workflows/docker-image.yml)
## To use virtual environment

do `pip install pipenv` to get pipenv
to activate virtual environment: `pipenv shell`
to install dependencies: `pipenv install`

To make sure sessions are active in view, make sure that GET or POST AJAX requests have
credentials included and also csrf token, for example:

## To prevent import error from showing up

`#type: ignore` to ignore the line

## To start PostgreSQL

`sudo systemctl start postgresql.service`

## To interact with PostgreSQL

`sudo -u postgres psql`

## To create database

CREATE DATABASE flex;

## To create user

CREATE USER admin WITH PASSWORD 'P@ssword1234';

### To give superuser

ALTER USER admin WITH SUPERUSER;


## To reset active status for all users

`python manage.py refreshactivestatus`

In production this will be run every 24h by a CRON job

To run backend server:
daphne backend.asgi:application
exec web python manage.py migrate --noinput

## For Docker

Take note that need to put service name under host in order for django to connect to db

### To run migrations in the container

docker compose exec web python manage.py migrate --noinput
