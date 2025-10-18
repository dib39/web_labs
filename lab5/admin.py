from django.contrib import admin
from .models import Customer, Product, Order, OrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'registration_date']
    list_filter = ['registration_date']
    search_fields = ['name', 'email', 'phone']
    ordering = ['-registration_date']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'in_stock', 'stock_quantity']
    list_filter = ['category', 'in_stock']
    search_fields = ['name', 'description']
    list_editable = ['price', 'in_stock', 'stock_quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_date', 'status', 'total_amount']
    list_filter = ['status', 'order_date']
    search_fields = ['customer__name', 'id']
    readonly_fields = ['order_date']
    ordering = ['-order_date']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total']
    list_filter = ['order__status']
    search_fields = ['order__id', 'product__name']
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Общая стоимость'