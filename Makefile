.PHONY: run migrate makemigrations make-app lint fix

run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

makemigrations:
	poetry run python manage.py makemigrations

shell:
	poetry run python manage.py shell

NAME ?= app

make-app:
	poetry run python manage.py startapp $(NAME) apps/$(NAME)

lint:
	poetry run ruff check .
	poetry run ruff format --check .

fix:
	poetry run ruff check . --fix




