up:
	docker compose up -d
build:
	docker compose build --no-cache --force-rm
server:
	docker compose exec server bash 