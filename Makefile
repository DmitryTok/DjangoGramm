.PHONY: run
run:
	docker-compose up

.PHONY: up
up: migrate
	docker-compose up

.PHONY: stop_docker
stop:
	docker-compose stop

.PHONY: close_docker-compose_file
down:
	docker-compose down -v

.PHONY: db
db:
	docker-compose up -d db

makemigrations: db
	docker-compose run web python manage.py makemigrations

migrate: makemigrations
	docker-compose run web python manage.py migrate

.PHONY: superuser
superuser: migrate
	docker-compose run web python manage.py createsuperuser

.PHONY: flake8
flake8:
	 docker-compose run web flake8 .

.PHONY: isort
isort:
	docker-compose run web isort .

.PHONY: mypy
mypy:
	docker-compose run web mypy . --explicit-package-bases

.PHONY: tests
tests:
	docker-compose run web coverage run manage.py test

.PHONY: tests_report
tests_report:
	docker-compose run web coverage report
