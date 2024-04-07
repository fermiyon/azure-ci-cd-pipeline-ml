setup:
	python3.10 -m venv ~/.venv
	#source ~/.venv/bin/activate

install:
	pip3.10 install --upgrade pip &&\
		pip3.10 install -r requirements.txt

test:
	#python -m pytest -vv --cov=myrepolib tests/*.py
	#python -m pytest --nbval notebook.ipynb


lint:
	#hadolint Dockerfile #uncomment to explore linting Dockerfiles
	pylint --disable=R,C,W1203 app.py

all: install lint test
