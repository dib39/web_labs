from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext as _
from .models import Employee, Project, Department

def employee_list(request):
    """Список сотрудников"""
    employees = Employee.objects.all()
    return render(request, 'lab4/employee_list.html', {'employees': employees})

def project_list(request):
    """Список проектов"""
    projects = Project.objects.all()
    return render(request, 'lab4/project_list.html', {'projects': projects})

def department_list(request):
    """Список отделов"""
    departments = Department.objects.all()
    return render(request, 'lab4/department_list.html', {'departments': departments})

def statistics(request):
    """Статистика по компании"""
    total_employees = Employee.objects.count()
    total_projects = Project.objects.count()
    total_departments = Department.objects.count()
    
    stats = {
        'total_employees': total_employees,
        'total_projects': total_projects,
        'total_departments': total_departments,
    }
    
    return render(request, 'lab4/statistics.html', {'stats': stats})