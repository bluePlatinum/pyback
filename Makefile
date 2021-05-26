init:
	pip install --upgrade pip
	pip install pipenv
	pipenv install --dev

tox:
	pipenv run tox