from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('lab1/', include('lab1.urls')),
    path('lab2/', include('lab2.urls')),
    path('lab3/', include('lab3.urls')),
    path('lab4/', include('lab4.urls')),
    path('lab5/', include('lab5.urls')), 
    path('lab6/', include('lab6.urls')),
    path('lab7/', include('lab7.urls')),
]