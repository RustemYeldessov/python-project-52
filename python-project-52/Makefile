PY := .venv/bin/python

.PHONY: install migrate collectstatic build render-start dev-start run

install:
	uv sync --frozen

migrate:
	. .venv/bin/activate && python manage.py migrate --noinput

collectstatic:
	. .venv/bin/activate && python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

dev-start:
	. .venv/bin/activate && python manage.py runserver 0.0.0.0:8000

run: install migrate collectstatic dev-start

