import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from lab3.models import Author, Book, Reader, Reading

def add_test_data():
    # Очистка существующих данных
    Reading.objects.all().delete()
    Book.objects.all().delete()
    Reader.objects.all().delete()
    Author.objects.all().delete()
    
    # Создание авторов
    author1 = Author.objects.create(name='Михаил Булгаков')
    author2 = Author.objects.create(name='Виктор Пелевин')
    author3 = Author.objects.create(name='Фёдор Достоевский')
    
    # Создание книг
    book1 = Book.objects.create(title='Мастер и Маргарита', author=author1, publication_year=1967, is_read=True)
    book2 = Book.objects.create(title='Чапаев и Пустота', author=author2, publication_year=1996, is_read=True)
    book3 = Book.objects.create(title='Преступление и наказание', author=author3, publication_year=1866, is_read=False)
    
    # Создание читателей
    reader1 = Reader.objects.create(name='Иванов И.И.')
    reader2 = Reader.objects.create(name='Петров П.П.')
    
    # Создание связей
    Reading.objects.create(reader=reader1, book=book1)
    Reading.objects.create(reader=reader1, book=book2)
    Reading.objects.create(reader=reader2, book=book3)
    
    print("Тестовые данные успешно добавлены!")

if __name__ == '__main__':
    add_test_data()