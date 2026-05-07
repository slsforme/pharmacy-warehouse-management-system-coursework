.PHONY: run migrate makemigrations make-app lint fix

run:
	poetry run python manage.py runserver

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

check:
	poetry run python manage.py check

check-db:
	poetry run python manage.py check --database default

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
