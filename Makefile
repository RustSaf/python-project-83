install:
	poetry install

test:
	poetry run pytest

#test-coverage:
#	poetry run pytest --cov=gendiff --cov-report xml

lint:
	poetry run flake8 app

selfcheck:
	poetry check

check: selfcheck test lint

#build: check
#	poetry build
#build:
#	./build.sh

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

#start:
#	poetry run flask --app example --debug run --port 8000

dev:
	poetry run flask --app page_analyzer:app run

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
