from django.core.management.base import BaseCommand
from lab5.models import Customer, Product, Order, OrderItem
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add sample order data'

    def handle(self, *args, **options):
        # Создаем клиентов
        customers = [
            Customer(name='Иван Петров', email='ivan@example.com', phone='+79161234567'),
            Customer(name='Мария Сидорова', email='maria@example.com', phone='+79167654321'),
            Customer(name='Алексей Козлов', email='alex@example.com', phone='+79169998877'),
        ]
        for customer in customers:
            customer.save()

        # Создаем товары
        products = [
            Product(name='iPhone 15', category='electronics', price=Decimal('999.99'), 
                   description='Смартфон Apple', in_stock=True, stock_quantity=10),
            Product(name='MacBook Pro', category='electronics', price=Decimal('1999.99'), 
                   description='Ноутбук Apple', in_stock=True, stock_quantity=5),
            Product(name='Футболка', category='clothing', price=Decimal('29.99'), 
                   description='Хлопковая футболка', in_stock=True, stock_quantity=50),
            Product(name='Книга Python', category='books', price=Decimal('49.99'), 
                   description='Учебник по Python', in_stock=False, stock_quantity=0),
        ]
        for product in products:
            product.save()

        # Создаем заказы
        orders = [
            Order(customer=customers[0], status='processing', total_amount=Decimal('1029.98')),
            Order(customer=customers[1], status='shipped', total_amount=Decimal('29.99')),
            Order(customer=customers[2], status='delivered', total_amount=Decimal('1999.99')),
        ]
        for order in orders:
            order.save()

        # Создаем позиции заказов
        order_items = [
            OrderItem(order=orders[0], product=products[0], quantity=1, price=products[0].price),
            OrderItem(order=orders[0], product=products[2], quantity=1, price=products[2].price),
            OrderItem(order=orders[1], product=products[2], quantity=1, price=products[2].price),
            OrderItem(order=orders[2], product=products[1], quantity=1, price=products[1].price),
        ]
        for item in order_items:
            item.save()

        self.stdout.write(self.style.SUCCESS('Successfully added order data'))