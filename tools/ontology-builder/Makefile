include ../coverage.mk

unit-tests:
	python -m pytest

install:
	pip install -r requirements.txt
	# Poke
	docker pull obolibrary/robot:v1.9.8
