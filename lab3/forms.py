from django import forms
from .models import Book, Reader, Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'is_read']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'publication_year': 'Год публикации',
            'is_read': 'Прочитана',
        }

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя читателя'}),
        }
        labels = {
            'name': 'Имя читателя',
        }