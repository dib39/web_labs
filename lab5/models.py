from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    registration_date = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('books', 'Книги'),
        ('home', 'Для дома'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название товара")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    stock_quantity = models.IntegerField(default=0, verbose_name="Количество на складе")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Клиент")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая сумма")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-order_date']
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
    
    def save(self, *args, **kwargs):
        # Автоматически устанавливаем цену из товара при сохранении
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
    
    def get_total(self):
        return self.quantity * self.price