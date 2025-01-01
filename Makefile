.DEFAULT_GOAL := help
.PHONY: help dev

up: ## Run all the services, web (Django), Celery, Postgres, Redis
	docker-compose up --build

sh: ## Open a shell with all dependencies
	docker-compose run web sh

psql: ## Open a Postgres shell
	docker-compose run web python manage.py dbshell

build: ## Build the docker image
	docker-compose build

build-no-cache: ## Build the docker image, without the the docker build cache
	docker-compose build web --no-cache

createsuperuser: ## Create the root Django superuser with username=root password=root
	docker-compose \
	    run \
	    -e DJANGO_SUPERUSER_PASSWORD=root \
	    -e DJANGO_SUPERUSER_USERNAME=root \
	    -e DJANGO_SUPERUSER_EMAIL=root@email.com \
	    web \
	    python manage.py createsuperuser --noinput

migrate: ## Create and apply database migrations
	docker-compose run web python manage.py makemigrations
	docker-compose run web python manage.py migrate

open-admin: ## Open the Django admin page
	open http://localhost:8000/admin

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
