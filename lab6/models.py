from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_public = models.BooleanField(default=False, verbose_name="Публичный проект")
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        permissions = [
            ("can_manage_projects", "Может управлять проектами"),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'project_id': self.id})

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('critical', 'Критический'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'К выполнению'),
        ('in_progress', 'В работе'),
        ('review', 'На проверке'),
        ('done', 'Выполнено'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  verbose_name="Исполнитель")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks',
                                 verbose_name="Создатель")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium',
                              verbose_name="Приоритет")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo',
                            verbose_name="Статус")
    due_date = models.DateField(null=True, blank=True, verbose_name="Срок выполнения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-priority', '-created_at']
        permissions = [
            ("can_assign_tasks", "Может назначать задачи"),
            ("can_change_status", "Может менять статус задач"),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'task_id': self.id})

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название команды")
    description = models.TextField(verbose_name="Описание")
    members = models.ManyToManyField(User, through='TeamMembership', verbose_name="Участники")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams',
                                 verbose_name="Создатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
    
    def __str__(self):
        return self.name

class TeamMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Участник'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member',
                          verbose_name="Роль в команде")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата вступления")
    
    class Meta:
        verbose_name = "Участник команды"
        verbose_name_plural = "Участники команд"
        unique_together = ['team', 'user']