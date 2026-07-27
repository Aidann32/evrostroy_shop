.PHONY: build up down restart logs migrate createsuperuser shell

build:
	sudo docker compose build

up:
	sudo docker compose up -d

down:
	sudo docker compose down

restart:
	sudo docker compose down
	sudo docker compose up -d

logs:
	sudo docker compose logs -f

migrate:
	sudo docker compose exec web python manage.py migrate

makemigrations:
	sudo docker compose exec web python manage.py makemigrations

createsuperuser:
	sudo docker compose exec web python manage.py createsuperuser

shell:
	sudo docker compose exec web python manage.py shell

db-shell:
	sudo docker compose exec db psql -U shop_user -d shop_db

clean:
	sudo docker compose down -v
