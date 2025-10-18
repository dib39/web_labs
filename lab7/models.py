from django.db import models
from django.contrib.auth.models import User

class UserPreference(models.Model):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Темная'),
        ('auto', 'Авто'),
    ]
    
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light', verbose_name="Тема")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru', verbose_name="Язык")
    notifications_enabled = models.BooleanField(default=True, verbose_name="Уведомления")
    items_per_page = models.IntegerField(default=10, verbose_name="Элементов на странице")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Последняя активность")
    
    class Meta:
        verbose_name = "Настройка пользователя"
        verbose_name_plural = "Настройки пользователей"
    
    def __str__(self):
        return f"Настройки {self.user.username}"

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    session_key = models.CharField(max_length=40, verbose_name="Ключ сессии")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    user_agent = models.TextField(verbose_name="User Agent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Последняя активность")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Сессия пользователя"
        verbose_name_plural = "Сессии пользователей"
    
    def __str__(self):
        return f"Сессия {self.user.username}"

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name="Ключ сессии (для анонимных)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")
    
    class Meta:
        verbose_name = "Корзина покупок"
        verbose_name_plural = "Корзины покупок"
    
    def __str__(self):
        return f"Корзина {self.user.username if self.user else 'Анонимная'}"
    
    def get_total_items(self):
        return self.items.count()
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")
    
    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
    
    def get_total_price(self):
        return self.price * self.quantity