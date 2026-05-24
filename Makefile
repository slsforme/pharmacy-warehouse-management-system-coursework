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
	@mkdir -p logs
	-poetry run ruff check . --output-format=json > logs/lint.json
	-poetry run ruff format --check .
	@echo "project linted succesfully. Log saved at: logs/lint.json"

fix:
	poetry run ruff check . --fix

format:
	poetry run ruff format .

test:
	poetry run pytest tests/test_all.py -v --tb=long --showlocals 

test-cov:
	poetry run pytest tests/test_all.py --cov=apps --cov-report=html
