from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Book, Reader, Author, Reading
from .forms import BookForm, ReaderForm

def books_list(request):
    """Представление для отображения списка книг читателя - аналог сервлета BooksList"""
    
    reader_name = request.GET.get('reader_name', '')
    
    books = Book.objects.all()
    readers = Reader.objects.all()
    
    reader_books = []
    if reader_name:
        try:
            reader = Reader.objects.get(name=reader_name)
            reader_books = reader.books.all()
        except Reader.DoesNotExist:
            reader_books = []
    
    context = {
        'reader_name': reader_name,
        'books': books,
        'readers': readers,
        'reader_books': reader_books,
    }
    
    return render(request, 'lab3/books_list.html', context)

def process_reader_request(request):
    """Обработка сложных запросов - аналог processRequest в сервлетах"""
    
    if request.method == 'POST':
        reader_name = request.POST.get('reader_name', '')
        action = request.POST.get('action', 'view')
        
        if action == 'add_book':
            book_id = request.POST.get('book_id')
            if reader_name and book_id:
                try:
                    reader = Reader.objects.get(name=reader_name)
                    book = Book.objects.get(id=book_id)
                    Reading.objects.get_or_create(reader=reader, book=book)
                except (Reader.DoesNotExist, Book.DoesNotExist):
                    pass
        
    else:
        reader_name = request.GET.get('reader_name', '')
        action = 'view'
    
    redirect_url = reverse('books_list') + f'?reader_name={reader_name}'
    return HttpResponseRedirect(redirect_url)

def add_reader(request):
    """Представление для добавления нового читателя"""
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('books_list'))
    else:
        form = ReaderForm()
    
    return render(request, 'lab3/add_reader.html', {'form': form})

def add_book(request):
    """Представление для добавления новой книги"""
    books = Book.objects.all()
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('books_list'))
    else:
        form = BookForm()
    
    return render(request, 'lab3/add_book.html', {
        'form': form,
        'books': books
    })

def reader_statistics(request):
    """Представление для отображения статистики"""
    readers = Reader.objects.all()
    stats = []
    
    for reader in readers:
        book_count = reader.books.count()
        read_count = reader.books.filter(is_read=True).count()
        stats.append({
            'reader': reader,
            'total_books': book_count,
            'read_books': read_count,
        })
    
    return render(request, 'lab3/statistics.html', {'stats': stats})