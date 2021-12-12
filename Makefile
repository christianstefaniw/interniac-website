SHELL:=/bin/bash

.PHONY: venv

all: run

run:
	python manage.py runserver

redis:
	redis-server

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	python manage.py test --debug-mode

init-venv:
	pip install virtualenv
	virtualenv venv

install-reqs:
	pip install -r requirements.txt

docs:
	pycco accounts/*.py -p
	pycco applications/*.py -p
	pycco authentication/*.py -p
