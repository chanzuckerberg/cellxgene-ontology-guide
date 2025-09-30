include ../coverage.mk

ROBOT_DOCKER_IMAGE := $(shell cat docker-versions.env | grep ROBOT_DOCKER_IMAGE | cut -d'=' -f2)

unit-tests:
	python -m pytest

install:
	pip install -r requirements.txt
	docker pull $(ROBOT_DOCKER_IMAGE)
