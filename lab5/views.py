from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum, Count, Avg
from .models import Customer, Product, Order, OrderItem

def order_list(request):
    """Список заказов с фильтрацией"""
    status_filter = request.GET.get('status', '')
    customer_filter = request.GET.get('customer', '')
    
    orders = Order.objects.all()
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    if customer_filter:
        orders = orders.filter(customer__name__icontains=customer_filter)
    
    customers = Customer.objects.all()
    
    # Статистика для отображения в шаблоне
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    context = {
        'orders': orders,
        'customers': customers,
        'status_filter': status_filter,
        'customer_filter': customer_filter,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }
    return render(request, 'lab5/order_list.html', context)

def order_detail(request, order_id):
    """Детальная информация о заказе"""
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'lab5/order_detail.html', context)

def product_catalog(request):
    """Каталог товаров с фильтрацией"""
    category_filter = request.GET.get('category', '')
    in_stock_only = request.GET.get('in_stock', '')
    
    products = Product.objects.all()
    
    if category_filter:
        products = products.filter(category=category_filter)
    if in_stock_only:
        products = products.filter(in_stock=True)
    
    # Группировка по категориям для статистики
    category_stats = products.values('category').annotate(
        total_products=Count('id'),
        avg_price=Avg('price')
    )
    
    context = {
        'products': products,
        'category_filter': category_filter,
        'in_stock_only': in_stock_only,
        'category_stats': category_stats,
    }
    return render(request, 'lab5/product_catalog.html', context)

def customer_orders(request, customer_id):
    """Заказы конкретного клиента"""
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer)
    
    customer_stats = {
        'total_orders': orders.count(),
        'total_spent': orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'first_order': orders.last().order_date if orders.exists() else None,
    }
    
    context = {
        'customer': customer,
        'orders': orders,
        'customer_stats': customer_stats,
    }
    return render(request, 'lab5/customer_orders.html', context)

def dashboard(request):
    """Панель управления с общей статистикой"""
    # Общая статистика
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    
    # Статистика по заказам
    order_stats = Order.objects.aggregate(
        total_revenue=Sum('total_amount'),
        avg_order_value=Avg('total_amount')
    )
    
    # Статистика по статусам заказов
    status_stats = Order.objects.values('status').annotate(
        count=Count('id'),
        revenue=Sum('total_amount')
    )
    
    # Последние заказы
    recent_orders = Order.objects.select_related('customer').order_by('-order_date')[:5]
    
    context = {
        'total_customers': total_customers,
        'total_products': total_products,
        'total_orders': total_orders,
        'order_stats': order_stats,
        'status_stats': status_stats,
        'recent_orders': recent_orders,
    }
    return render(request, 'lab5/dashboard.html', context)