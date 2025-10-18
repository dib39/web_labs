from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Product, Sale, Customer, AnalyticsData
from .serializers import *

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category = request.GET.get('category', '')
        if category:
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    
    def perform_create(self, serializer):
        # Автоматически устанавливаем цену продажи из цены товара, если не указана
        if not serializer.validated_data.get('sale_price'):
            product = serializer.validated_data['product']
            serializer.save(sale_price=product.price)
        else:
            serializer.save()

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class AnalyticsDataViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsData.objects.all()
    serializer_class = AnalyticsDataSerializer

class DashboardView(APIView):
    def get(self, request):
        # Основная статистика
        total_products = Product.objects.count()
        total_sales = Sale.objects.count()
        total_revenue = Sale.objects.aggregate(Sum('sale_price'))['sale_price__sum'] or 0
        total_customers = Customer.objects.count()
        
        # Последние продажи
        recent_sales = Sale.objects.select_related('product').order_by('-sale_date')[:5]
        
        # Топ товаров
        top_products = Sale.objects.values(
            'product__name', 'product__category'
        ).annotate(
            total_sold=Sum('quantity'),
            total_revenue=Sum('sale_price')
        ).order_by('-total_sold')[:5]
        
        data = {
            'total_products': total_products,
            'total_sales': total_sales,
            'total_revenue': float(total_revenue),
            'total_customers': total_customers,
            'recent_sales': SaleSerializer(recent_sales, many=True).data,
            'top_products': list(top_products),
        }
        
        return Response(data)

class SalesAnalyticsView(APIView):
    def get(self, request):
        # Аналитика продаж за последние 30 дней
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Продажи по дням
        daily_sales = Sale.objects.filter(
            sale_date__range=[start_date, end_date]
        ).extra(
            {'sale_day': "date(sale_date)"}
        ).values('sale_day').annotate(
            daily_revenue=Sum('sale_price'),
            daily_sales=Count('id')
        ).order_by('sale_day')
        
        # Продажи по категориям
        category_sales = Sale.objects.filter(
            sale_date__range=[start_date, end_date]
        ).values('product__category').annotate(
            category_revenue=Sum('sale_price'),
            total_sold=Sum('quantity')
        ).order_by('-category_revenue')
        
        data = {
            'period': {
                'start': start_date.date(),
                'end': end_date.date()
            },
            'daily_sales': list(daily_sales),
            'category_sales': list(category_sales),
        }
        
        return Response(data)