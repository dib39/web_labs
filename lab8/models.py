from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('books', 'Книги'),
        ('home', 'Товары для дома'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название товара")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    stock_quantity = models.IntegerField(default=0, verbose_name="Количество на складе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(verbose_name="Количество")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена продажи")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")
    customer_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    
    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
        ordering = ['-sale_date']
    
    def __str__(self):
        return f"Продажа {self.product.name} - {self.quantity} шт."
    
    def get_total(self):
        return self.quantity * self.sale_price

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['-registration_date']
    
    def __str__(self):
        return self.name

class AnalyticsData(models.Model):
    METRIC_CHOICES = [
        ('daily_revenue', 'Ежедневная выручка'),
        ('product_sales', 'Продажи по товарам'),
        ('category_performance', 'Эффективность категорий'),
        ('customer_activity', 'Активность клиентов'),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_CHOICES, verbose_name="Тип метрики")
    data = models.JSONField(verbose_name="Данные")
    period_start = models.DateField(verbose_name="Начало периода")
    period_end = models.DateField(verbose_name="Конец периода")
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="Сгенерировано")
    
    class Meta:
        verbose_name = "Данные аналитики"
        verbose_name_plural = "Данные аналитики"
    
    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.period_start} to {self.period_end}"