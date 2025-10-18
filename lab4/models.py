from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название отдела")
    
    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    position = models.CharField(max_length=100, verbose_name="Должность")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")
    hire_date = models.DateField(verbose_name="Дата найма")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    budget = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Бюджет")
    employees = models.ManyToManyField(Employee, through='ProjectAssignment', verbose_name="Сотрудники")
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self):
        return self.name

class ProjectAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, verbose_name="Роль в проекте")
    assignment_date = models.DateField(auto_now_add=True, verbose_name="Дата назначения")
    
    class Meta:
        verbose_name = "Назначение на проект"
        verbose_name_plural = "Назначения на проекты"