from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='lab1_index'),
    path('info/', views.system_info, name='system_info'),
]