from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

def project_info(request):
    """Информация о проекте - аналог index.jsp"""
    return render(request, 'lab2/project_info.html')

def book_list(request):
    """Список книг - демонстрация работы с данными"""
    books = Book.objects.all()
    return render(request, 'lab2/book_list.html', {'books': books})

def add_sample_data(request):
    """Добавление тестовых данных в базу"""
    sample_books = [
        {'title': 'Мастер и Маргарита', 'author': 'Булгаков', 'is_read': True},
        {'title': 'Чапаев и пустота', 'author': 'Пелевин', 'is_read': False},
        {'title': '1984', 'author': 'Оруэлл', 'is_read': True},
    ]
    
    for book_data in sample_books:
        Book.objects.get_or_create(**book_data)
    
    return HttpResponse("Тестовые данные добавлены! <a href='/lab2/books/'>Посмотреть список книг</a>")