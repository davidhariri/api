env:
	pipenv shell

test:
	pipenv shell
	clear
	nosetests

dev:
	pipenv shell
	clear
	python main.py
