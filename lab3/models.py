from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    publication_year = models.IntegerField(verbose_name="Год публикации")
    is_read = models.BooleanField(default=False, verbose_name="Прочитана")
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
    
    def __str__(self):
        return f"{self.title} ({self.author})"

class Reader(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя читателя")
    books = models.ManyToManyField(Book, through='Reading', verbose_name="Книги")
    
    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"
    
    def __str__(self):
        return self.name

class Reading(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_date = models.DateField(auto_now_add=True, verbose_name="Дата прочтения")
    
    class Meta:
        verbose_name = "Чтение"
        verbose_name_plural = "Чтения"