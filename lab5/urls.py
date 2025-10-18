from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('products/', views.product_catalog, name='product_catalog'),
    path('customers/<int:customer_id>/orders/', views.customer_orders, name='customer_orders'),
]