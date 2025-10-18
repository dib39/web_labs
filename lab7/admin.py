from django.contrib import admin
from .models import UserPreference, UserSession, ShoppingCart, CartItem

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'language', 'notifications_enabled', 'last_activity']
    list_filter = ['theme', 'language', 'notifications_enabled']
    search_fields = ['user__username']

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'created_at', 'last_activity', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'ip_address']

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'created_at', 'updated_at', 'get_total_items', 'get_total_price']
    list_filter = ['created_at']
    search_fields = ['user__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product_name', 'price', 'quantity', 'added_at', 'get_total_price']
    list_filter = ['added_at']
    search_fields = ['product_name']