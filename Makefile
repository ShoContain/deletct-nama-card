up:
	docker-compose up -d
build:
	docker-compose build --no-cache --force-rm
down:
	docker-compose down --remove-orphans
server:
	docker-compose exec server bash
front:
	docker-compose exec front sh

.PHONY: server front