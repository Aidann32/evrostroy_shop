import os
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from openpyxl import load_workbook

from apps.catalog.models import Brand, Category, Product


class Command(BaseCommand):
    help = 'Импорт товаров из Excel (краски.xlsx)'

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_path',
            type=str,
            help='Путь к Excel-файлу, например: /app/data/краски.xlsx',
        )
        parser.add_argument(
            '--images-dir',
            type=str,
            default='',
            help='Папка с картинками (имя файла = id, например 1к.jpg)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Только показать, что будет импортировано, без записи в БД',
        )

    def handle(self, *args, **options):
        excel_path = options['excel_path']
        images_dir = options['images_dir']
        dry_run = options['dry_run']

        if not os.path.exists(excel_path):
            self.stderr.write(self.style.ERROR(f'Файл не найден: {excel_path}'))
            return

        wb = load_workbook(excel_path, read_only=True, data_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            self.stderr.write(self.style.ERROR('Excel пустой'))
            return

        header = [str(c).strip().lower() if c is not None else '' for c in rows[0]]
        # ожидаемые колонки: id, title, description, brand, category, price
        col = {name: idx for idx, name in enumerate(header)}

        required = ['id', 'title', 'price']
        for r in required:
            if r not in col:
                self.stderr.write(self.style.ERROR(f'Нет колонки: {r}'))
                return

        created = 0
        updated = 0
        skipped = 0

        for row in rows[1:]:
            if not row or all(c is None or str(c).strip() == '' for c in row):
                continue

            raw_id = row[col['id']]
            title = row[col['title']]
            description = row[col.get('description')] if 'description' in col else ''
            brand_name = row[col.get('brand')] if 'brand' in col else ''
            category_name = row[col.get('category')] if 'category' in col else ''
            price_raw = row[col['price']]

            if not title:
                skipped += 1
                continue

            title = str(title).strip()
            description = str(description or '').strip()
            brand_name = str(brand_name or '').strip() or 'Без бренда'
            category_name = str(category_name or '').strip()

            try:
                price = Decimal(str(price_raw).replace(' ', '').replace(',', '.'))
            except (InvalidOperation, TypeError, ValueError):
                self.stderr.write(self.style.WARNING(f'Пропуск (цена): {title}'))
                skipped += 1
                continue

            product_id_key = str(raw_id).strip() if raw_id is not None else ''

            if dry_run:
                self.stdout.write(f'[DRY] {product_id_key} | {title} | {brand_name} | {category_name} | {price}')
                created += 1
                continue

            # Brand
            brand, _ = Brand.objects.get_or_create(
                name=brand_name,
                defaults={'slug': self._unique_slug(Brand, brand_name)},
            )

            # Category
            category = None
            if category_name:
                category, _ = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'slug': self._unique_slug(Category, category_name)},
                )

            # Product: ищем по имени + бренду, чтобы не плодить дубли
            product = Product.objects.filter(name=title, brand=brand).first()

            if product:
                product.description = description
                product.category = category
                product.price = price
                product.is_active = True
                if not product.slug:
                    product.slug = self._unique_slug(Product, title, instance=product)
                product.save()
                updated += 1
                action = 'обновлён'
            else:
                product = Product(
                    name=title,
                    brand=brand,
                    category=category,
                    description=description,
                    price=price,
                    is_active=True,
                )
                product.slug = self._unique_slug(Product, title)
                product.save()
                created += 1
                action = 'создан'

            # Картинка: имя файла = id (1к.jpg, 1к.png, ...)
            if images_dir and product_id_key:
                image_path = self._find_image(images_dir, product_id_key)
                if image_path:
                    with open(image_path, 'rb') as f:
                        filename = os.path.basename(image_path)
                        product.image.save(filename, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'{action}: {title} + image'))
                else:
                    self.stdout.write(self.style.WARNING(f'{action}: {title} (нет картинки для id={product_id_key})'))
            else:
                self.stdout.write(self.style.SUCCESS(f'{action}: {title}'))

        wb.close()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Готово. Создано: {created}, обновлено: {updated}, пропущено: {skipped}'
        ))

    def _unique_slug(self, model, text, instance=None):
        base = slugify(text, allow_unicode=True) or 'item'
        slug = base
        n = 1
        qs = model.objects.all()
        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)
        while qs.filter(slug=slug).exists():
            slug = f'{base}-{n}'
            n += 1
        return slug

    def _find_image(self, images_dir, product_id):
        """
        Ищет файл с именем = id и расширениями jpg/jpeg/png/webp.
        Примеры: 1к.jpg, 1к.JPG, 12к.png
        """
        images_dir = Path(images_dir)
        if not images_dir.exists():
            return None

        extensions = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP']
        for ext in extensions:
            path = images_dir / f'{product_id}{ext}'
            if path.is_file():
                return str(path)

        # запасной вариант: любой файл, имя которого начинается с id
        for path in images_dir.iterdir():
            if path.is_file() and path.stem == product_id:
                return str(path)

        return None