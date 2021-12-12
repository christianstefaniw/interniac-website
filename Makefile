SHELL := /bin/bash

.PHONY: venv

all: run

venv:
	source ./venv/bin/activate

run:
	python manage.py runserver

redis:
	redis-server

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	python manage.py test --debug-mode

install:
	pip install virtualenv
	virtualenv venv
	source ./venv/bin/activate
	pip install -r requirements.txt