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

collectstatic:
	sudo docker compose exec web python manage.py collectstatic --noinput

# Обновить фронтенд и сбросить кэш у пользователей: пишет новую FRONTEND_VERSION в .env
frontend-release:
	sed -i '/^FRONTEND_VERSION=/d' .env
	echo "FRONTEND_VERSION=$$(date +%Y%m%d%H%M%S)" >> .env
	sudo docker compose -f docker-compose.prod.yml build web
	sudo docker compose -f docker-compose.prod.yml up -d web
	sudo docker compose -f docker-compose.prod.yml exec web python manage.py migrate
	sudo docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

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

import-products-dry:
	sudo docker compose exec web python manage.py import_products /app/data/краски.xlsx --images-dir /app/data/product_images --dry-run

import-products:
	sudo docker compose exec web python manage.py import_products /app/data/iron_doors.xlsx --images-dir /app/data/iron_doors_images

import-doors:
	sudo docker compose exec web python manage.py import_doors /app/data/doors.xlsx --images-dir /app/data/doors_images
