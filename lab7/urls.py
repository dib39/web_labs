from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='lab7_index'),
    path('session/', views.session_info, name='session_info'),
    path('clear-session/', views.clear_session, name='clear_session'),
    path('cookies/', views.cookie_demo, name='cookie_demo'),
    path('cookies/delete/<str:cookie_name>/', views.delete_cookie, name='delete_cookie'),
    path('set-theme/', views.set_theme, name='set_theme'),
    path('set-language/', views.set_language, name='set_language'),
    path('cart/', views.shopping_cart, name='shopping_cart'),
    path('preferences/', views.user_preferences, name='user_preferences'),
]