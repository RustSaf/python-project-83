install:
	pip install --upgrade pip && poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 page_analyzer/app.py

selfcheck:
	poetry check

check: selfcheck test lint

build:
	./build.sh

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

dev:
	poetry run flask --app page_analyzer:app run --debug

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

.PHONY:
	install
	test
	test-coverage
	lint
	selfcheck
	check
	build
	publish
	package-install
	start
	dev
