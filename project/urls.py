from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('lab1/', include('lab1.urls')),
    path('lab2/', include('lab2.urls')),
    path('lab3/', include('lab3.urls')),
    path('lab4/', include('lab4.urls')),
    path('lab5/', include('lab5.urls')),
    path('lab6/', include('lab6.urls')),
    path('lab8/', include('lab8.urls')),
    # SPA главная страница - должна быть последней
    path('', TemplateView.as_view(template_name='lab8/index.html'), name='spa_home'),
]