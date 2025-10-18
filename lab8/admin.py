from django.contrib import admin
from .models import Product, Sale, Customer, AnalyticsData

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock_quantity']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'sale_price', 'get_total', 'customer_name', 'sale_date']
    list_filter = ['sale_date', 'product__category']
    search_fields = ['product__name', 'customer_name']
    readonly_fields = ['sale_date']
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Общая сумма'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'registration_date']
    search_fields = ['name', 'email']
    readonly_fields = ['registration_date']

@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'period_start', 'period_end', 'generated_at']
    list_filter = ['metric_type', 'generated_at']
    readonly_fields = ['generated_at']