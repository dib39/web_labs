from django.contrib import admin
from django.urls import path, include  # убедитесь, что include импортирован

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lab1/', include('lab1.urls')),
    path('lab2/', include('lab2.urls')),
    path('lab3/', include('lab3.urls')),
]
