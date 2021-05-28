venv:
	source venv/bin/activate

test:
	python manage.py test --debug-mode

cov:
	python -m coverage run --source='.' --omit 'venv/*' manage.py test .

cov-report:
	python -m coverage report