from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add products to database'

    def handle(self, *args, **options):
        """
        Создание кастомной команды для добавления данных
        """
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(name='Средства индивидуальной защиты',
                                                     description='Средства для защиты тело во время работы')

        products = [
            {'name': 'Перчатки', 'descriptions': 'Для защиты рук', 'image':'perchatki.jpg', 'category': category,
             'price': 100},
            {'name': 'Шлем', 'descriptions': 'Для защиты головы', 'image': 'kevlar.jpg', 'category': category,
             'price': 300}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Succssesfully added product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product allready exist: {product.name}'))
