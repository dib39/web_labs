from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('lab1/', include('lab1.urls')),
    path('lab2/', include('lab2.urls')),
    path('lab3/', include('lab3.urls')),
    path('lab4/', include('lab4.urls')),
]