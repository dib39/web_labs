from rest_framework import serializers
from .models import Product, Sale, Customer, AnalyticsData

class ProductSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_display', 'price', 'description', 'stock_quantity', 'created_at']

class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Sale
        fields = ['id', 'product', 'product_name', 'quantity', 'sale_price', 'total_amount', 'sale_date', 'customer_name']
    
    def get_total_amount(self, obj):
        return obj.get_total()

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'registration_date']

class AnalyticsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsData
        fields = ['id', 'metric_type', 'data', 'period_start', 'period_end', 'generated_at']

class DashboardStatsSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_customers = serializers.IntegerField()
    recent_sales = SaleSerializer(many=True)
    top_products = serializers.ListField()