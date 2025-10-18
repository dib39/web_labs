from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_info, name='lab2_index'),
    path('books/', views.book_list, name='book_list'),
    path('add-data/', views.add_sample_data, name='add_sample_data'),
]