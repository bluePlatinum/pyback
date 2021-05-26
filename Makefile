init:
	pip install --upgrade pip
	pip install pipenv typing_extensions
	pipenv install --dev

tox:
	pipenv run tox