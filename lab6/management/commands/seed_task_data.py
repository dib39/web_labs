from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from lab6.models import Project, Task
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Add sample task management data'

    def handle(self, *args, **options):
        # Создаем тестовых пользователей
        users = [
            User.objects.create_user('manager', 'manager@example.com', 'password123'),
            User.objects.create_user('developer1', 'dev1@example.com', 'password123'),
            User.objects.create_user('developer2', 'dev2@example.com', 'password123'),
        ]
        
        # Делаем первого пользователя менеджером
        manager = users[0]
        can_assign = Permission.objects.get(codename='can_assign_tasks')
        can_change = Permission.objects.get(codename='can_change_status')
        manager.user_permissions.add(can_assign, can_change)
        manager.is_staff = True
        manager.save()

        # Создаем проекты
        projects = [
            Project(name='Разработка веб-сайта', 
                   description='Создание корпоративного сайта компании',
                   created_by=manager, is_public=True),
            Project(name='Внутренняя система', 
                   description='Разработка системы управления задачами',
                   created_by=manager, is_public=False),
        ]
        for project in projects:
            project.save()

        # Создаем задачи
        tasks = [
            Task(title='Дизайн главной страницы', 
                description='Создать макет главной страницы сайта',
                project=projects[0], assigned_to=users[1], created_by=manager,
                priority='high', status='in_progress',
                due_date=timezone.now() + timedelta(days=7)),
            Task(title='Настройка базы данных', 
                description='Настроить PostgreSQL базу данных для системы',
                project=projects[1], assigned_to=users[2], created_by=manager,
                priority='medium', status='todo',
                due_date=timezone.now() + timedelta(days=14)),
        ]
        for task in tasks:
            task.save()

        self.stdout.write(self.style.SUCCESS('Successfully added task management data'))
        self.stdout.write('Users created: manager/password123, developer1/password123, developer2/password123')