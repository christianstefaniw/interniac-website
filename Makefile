.PHONY: venv

venv:
	source venv/bin/activate

run:
	python manage.py runserver

redis:
	redis-server

make-migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	python manage.py test --debug-mode

cov:
	python -m coverage run --source='.' --omit 'venv/*' manage.py test .

cov-report:
	python -m coverage report