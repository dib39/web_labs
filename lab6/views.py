from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.db.models import Q, Count
from .models import Task, Project, Team
from .forms import CustomAuthenticationForm, CustomUserCreationForm, TaskForm, ProjectForm

def is_manager(user):
    """Проверка, является ли пользователь менеджером"""
    return user.has_perm('lab6.can_assign_tasks') or user.is_staff

# Представления аутентификации
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/lab6/')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'lab6/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/lab6/')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'lab6/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/lab6/')

# Основные представления с контролем доступа
@login_required
def dashboard(request):
    """Панель управления - доступна только авторизованным пользователям"""
    user_tasks = Task.objects.filter(
        Q(assigned_to=request.user) | Q(created_by=request.user)
    ).select_related('project')
    
    # Проекты, к которым у пользователя есть доступ
    accessible_projects = Project.objects.filter(
        Q(created_by=request.user) | Q(is_public=True)
    )
    
    # Статистика
    stats = {
        'total_tasks': user_tasks.count(),
        'tasks_todo': user_tasks.filter(status='todo').count(),
        'tasks_in_progress': user_tasks.filter(status='in_progress').count(),
        'tasks_done': user_tasks.filter(status='done').count(),
        'total_projects': accessible_projects.count(),
    }
    
    context = {
        'user_tasks': user_tasks[:10],  # Последние 10 задач
        'accessible_projects': accessible_projects[:5],  # Последние 5 проектов
        'stats': stats,
        'is_manager': is_manager(request.user),
    }
    return render(request, 'lab6/dashboard.html', context)

@login_required
def task_list(request):
    """Список задач с фильтрацией"""
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    tasks = Task.objects.filter(
        Q(assigned_to=request.user) | Q(created_by=request.user) |
        Q(project__is_public=True) | Q(project__created_by=request.user)
    ).distinct()
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'is_manager': is_manager(request.user),
    }
    return render(request, 'lab6/task_list.html', context)

@login_required
def task_detail(request, task_id):
    """Детальная информация о задаче"""
    task = get_object_or_404(Task, id=task_id)
    
    # Проверка доступа к задаче
    if not (task.assigned_to == request.user or 
            task.created_by == request.user or
            task.project.is_public or
            task.project.created_by == request.user):
        return HttpResponseForbidden("У вас нет доступа к этой задаче")
    
    context = {
        'task': task,
        'can_edit': task.created_by == request.user or is_manager(request.user),
    }
    return render(request, 'lab6/task_detail.html', context)

@login_required
@permission_required('lab6.can_assign_tasks', raise_exception=True)
def create_task(request):
    """Создание задачи - только для менеджеров"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm()
        # Ограничиваем выбор проектов только доступными
        form.fields['project'].queryset = Project.objects.filter(
            Q(created_by=request.user) | Q(is_public=True)
        )
        # Ограничиваем выбор исполнителей
        form.fields['assigned_to'].queryset = User.objects.all()
    
    context = {
        'form': form,
        'title': 'Создание задачи',
    }
    return render(request, 'lab6/task_form.html', context)

@login_required
def create_project(request):
    """Создание проекта - доступно всем авторизованным пользователям"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'title': 'Создание проекта',
    }
    return render(request, 'lab6/project_form.html', context)

@login_required
def project_list(request):
    """Список проектов"""
    projects = Project.objects.filter(
        Q(created_by=request.user) | Q(is_public=True)
    ).annotate(
        task_count=Count('task')
    )
    
    context = {
        'projects': projects,
        'can_create_project': True,  # Все авторизованные могут создавать проекты
    }
    return render(request, 'lab6/project_list.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """Панель администратора - только для staff пользователей"""
    total_users = User.objects.count()
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    
    context = {
        'total_users': total_users,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
    }
    return render(request, 'lab6/admin_dashboard.html', context)