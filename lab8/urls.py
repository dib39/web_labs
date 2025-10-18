from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'sales', views.SaleViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'analytics', views.AnalyticsDataViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/dashboard/', views.DashboardView.as_view(), name='dashboard_api'),
    path('api/analytics/sales/', views.SalesAnalyticsView.as_view(), name='sales_analytics_api'),
]