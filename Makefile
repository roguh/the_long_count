NAME=hrpypy
ALLPYFILES=*.py
PYFILES=*.py

pipenv_install:
	pipenv install -r requirements.txt
	pipenv install -r requirements_for_development.txt
	echo ACTIVATE VIRTUALENV WITH pipenv shell
	echo OR USE pipenv run PROGRAM

test:
	python3 -m doctest -v $(PYFILES)
	nose2 --output-buffer --pretty-assert --log-capture --with-coverage --coverage .

format:
	autopep8 --in-place --aggressive $(ALLPYFILES)
	isort $(ALLPYFILES)
