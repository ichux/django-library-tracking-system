# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help: Django Library Tracking System help
# help:

SHELL := /bin/bash
PC_USER := $(shell whoami)
ENV_FILE ?= .env

.PHONY: help
# help: help				- Please use "make <target>" where <target> is one of
help:
	@grep "^# help\:" Makefile | sed 's/\# help\: //' | sed 's/\# help\://'

.PHONY: e
# help: e               - create .env
e:
	@cp env.example .env
	@sed -i "s/^PC_USER=.*/PC_USER=$(PC_USER)/" "$(ENV_FILE)"

.PHONY: b
# help: b				- build containers
b:
	@COMPOSE_BAKE=true BUILDKIT_PROGRESS=plain docker compose -f docker-compose.yml up --build -d

.PHONY: a
# help: a				- create admin
a:
	@docker compose run if_lib_web python manage.py createsuperuser
.PHONY: t
# help: t				- test library
t:
	@docker exec -it cf_lib_web python manage.py test library --verbosity=2

.PHONY: fr
# help: fr				- pip freeze
fr:
	@pip freeze | grep -v 'wheel\|setuptools' > requirements.txt
