from django.urls import path
from django.views.i18n import set_language
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('projects/', views.project_list, name='project_list'),
    path('departments/', views.department_list, name='department_list'),
    path('statistics/', views.statistics, name='statistics'),
]