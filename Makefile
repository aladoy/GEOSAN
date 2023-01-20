UID := $(shell id -u)
GID := $(shell id -g)

generate-selfsigned-cert:
	cd cert && OWNER="${UID}.${GID}" docker-compose up --remove-orphans

setup: 
	poetry install -vvv

dev: # local
	cd geosan; poetry run gunicorn webmapping.wsgi

run: # main entry for on server, can be run on desktop also
	docker-compose build --pull
	docker-compose up --remove-orphans --force-recreate -d
