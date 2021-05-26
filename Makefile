init:
	pip install --upgrade pip
	pip install pipenv typing_extensions importlib_resources
	pipenv install --dev

tox:
	pipenv run tox