from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from .models import Project, Task, Team, TeamMembership

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'priority', 'status', 'due_date']
    list_filter = ['priority', 'status', 'due_date']
    search_fields = ['title', 'description']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    search_fields = ['name', 'description']

@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ['team', 'user', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']

# Настройка разрешений для групп
def setup_permissions():
    """Создание групп и назначение разрешений"""
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from lab6.models import Project, Task
    
    # Группа "Менеджеры"
    managers_group, created = Group.objects.get_or_create(name='Менеджеры')
    
    # Добавляем разрешения для менеджеров
    task_permissions = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(Task),
        codename__in=['can_assign_tasks', 'can_change_status']
    )
    for perm in task_permissions:
        managers_group.permissions.add(perm)
    
    project_permissions = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(Project),
        codename='can_manage_projects'
    )
    for perm in project_permissions:
        managers_group.permissions.add(perm)

# Вызов функции при загрузке
setup_permissions()