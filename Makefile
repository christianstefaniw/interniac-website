venv:
	source venv/bin/activate

cov:
	python -m coverage run --source='.' --omit 'venv/*' manage.py test .

cov-report:
	python -m coverage report