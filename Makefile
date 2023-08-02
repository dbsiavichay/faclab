# Makefile generated with pymakefile
help:
	@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "[36m%-30s[0m %s\n", $$1, $$2}'

migrations:
	docker-compose run --rm web python3 manage.py makemigrations

migrate:
	docker-compose run --rm web python3 manage.py migrate

lint:
	docker-compose run --rm web make check

check:  ## Fix code to pep8 standards
	black .
	isort . --profile black
	flake8 .

superuser: # Create django superuser
	docker-compose run --rm web python3 manage.py createsuperuser

i18n:
	docker-compose run --rm web python3 manage.py makemessages -l es --extension=html,py

i18n-compile:  ## Compile translations
	docker-compose run --rm web python3 manage.py compilemessages -l es

run:
	docker-compose run --rm -p 8000:8000 web

runtests:
	docker-compose run --rm web pytest --reuse-db --create-db --no-migrations

celery:
	docker-compose run --rm web celery -A faclab worker -l INFO

shell:
	docker-compose run --rm web python3 manage.py shell

collectstatic:
	docker-compose run --rm web python3 manage.py collectstatic
