from django.core.management.base import BaseCommand
from lab8.models import Product, Sale, Customer
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Add sample analytics data'

    def handle(self, *args, **options):
        # Создаем товары
        products_data = [
            {'name': 'iPhone 15', 'category': 'electronics', 'price': Decimal('899.99'), 'stock_quantity': 50},
            {'name': 'MacBook Air', 'category': 'electronics', 'price': Decimal('1299.99'), 'stock_quantity': 25},
            {'name': 'Футболка хлопковая', 'category': 'clothing', 'price': Decimal('29.99'), 'stock_quantity': 100},
            {'name': 'Джинсы', 'category': 'clothing', 'price': Decimal('79.99'), 'stock_quantity': 60},
            {'name': 'Книга "Python для начинающих"', 'category': 'books', 'price': Decimal('39.99'), 'stock_quantity': 30},
            {'name': 'Настольная лампа', 'category': 'home', 'price': Decimal('49.99'), 'stock_quantity': 40},
        ]
        
        products = []
        for product_data in products_data:
            product, created = Product.objects.get_or_create(**product_data)
            products.append(product)
            if created:
                self.stdout.write(f'Создан товар: {product.name}')

        # Создаем клиентов
        customers_data = [
            {'name': 'Иван Петров', 'email': 'ivan@example.com', 'phone': '+79161234567'},
            {'name': 'Мария Сидорова', 'email': 'maria@example.com', 'phone': '+79167654321'},
            {'name': 'Алексей Козлов', 'email': 'alex@example.com', 'phone': '+79169998877'},
            {'name': 'Екатерина Новикова', 'email': 'ekaterina@example.com', 'phone': '+79165554433'},
        ]
        
        customers = []
        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(**customer_data)
            customers.append(customer)
            if created:
                self.stdout.write(f'Создан клиент: {customer.name}')

        # Создаем продажи за последние 30 дней
        for i in range(100):
            product = random.choice(products)
            customer = random.choice(customers + [None])  # Иногда без клиента
            days_ago = random.randint(0, 30)
            
            sale = Sale(
                product=product,
                quantity=random.randint(1, 3),
                sale_price=product.price * Decimal('0.95'),  # Небольшая скидка
                customer_name=customer.name if customer else '',
                sale_date=timezone.now() - timedelta(days=days_ago)
            )
            sale.save()

        self.stdout.write(self.style.SUCCESS('Successfully created analytics data with 100 sales!'))