help:			## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------- #

build:			## Build or rebuild services
	docker-compose -f docker-compose-local.yml build

up:				## Create and start containers
	docker-compose -f docker-compose-local.yml up

start:			## Start services
	docker-compose -f docker-compose-local.yml start

stop:			## Stop services
	docker-compose -f docker-compose-local.yml stop

down:			## Stop and remove containers, networks, images, and volumes
	docker-compose -f docker-compose-local.yml down

migrations:		## make migrations in running container
	docker exec bookstore python manage.py makemigrations

migrate:		## apply migrations in running container
	docker exec bookstore python manage.py migrate