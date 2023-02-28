.PHONY: run_app
run_app:
	python3 manage.py runserver

.PHONY: up
up:
	docker-compose up

.PHONY: run_docker-compose_file
down:
	docker-compose down -v

.PHONY: db
db:
	docker-compose up -d db

.PHONY: makemigrations
makemigrations: db
	docker-compose run web python manage.py makemigrations

.PHONY: migrate
migrate: makemigrations
	docker-compose run web python manage.py migrate
