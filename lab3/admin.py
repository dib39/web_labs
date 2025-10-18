from django.contrib import admin
from .models import Author, Book, Reader, Reading

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'is_read']
    list_filter = ['author', 'is_read', 'publication_year']
    search_fields = ['title', 'author__name']

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ['reader', 'book', 'read_date']
    list_filter = ['read_date']
    search_fields = ['reader__name', 'book__title']