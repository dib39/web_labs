from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('process/', views.process_reader_request, name='process_request'),
    path('add-reader/', views.add_reader, name='add_reader'),
    path('add-book/', views.add_book, name='add_book'),
    path('statistics/', views.reader_statistics, name='reader_statistics'),
]