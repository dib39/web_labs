from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json
from .models import UserPreference, UserSession, ShoppingCart, CartItem

def index(request):
    """Главная страница с демонстрацией работы Cookies и сессий"""
    
    # Работа с сессией - счетчик посещений
    visit_count = request.session.get('visit_count', 0)
    visit_count += 1
    request.session['visit_count'] = visit_count
    request.session['last_visit'] = timezone.now().isoformat()
    
    # Работа с Cookies - тема оформления
    theme = request.COOKIES.get('theme', 'light')
    language = request.COOKIES.get('language', 'ru')
    
    # Получаем или создаем корзину
    cart = get_or_create_cart(request)
    
    context = {
        'visit_count': visit_count,
        'theme': theme,
        'language': language,
        'cart_items_count': cart.get_total_items() if cart else 0,
        'user_preferences': get_user_preferences(request),
    }
    return render(request, 'lab7/index.html', context)

def set_theme(request):
    """Установка темы оформления через Cookie"""
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        response = redirect('lab7_index')
        response.set_cookie('theme', theme, max_age=365*24*60*60)  # 1 год
        return response
    return redirect('lab7_index')

def set_language(request):
    """Установка языка через Cookie"""
    if request.method == 'POST':
        language = request.POST.get('language', 'ru')
        response = redirect('lab7_index')
        response.set_cookie('language', language, max_age=365*24*60*60)  # 1 год
        return response
    return redirect('lab7_index')

def session_info(request):
    """Информация о сессии"""
    session_data = {
        'session_key': request.session.session_key,
        'visit_count': request.session.get('visit_count', 0),
        'last_visit': request.session.get('last_visit', 'Никогда'),
        'session_expiry': request.session.get_expiry_age(),
        'all_session_keys': list(request.session.keys()),
    }
    
    # Сохраняем информацию о сессии в базе для авторизованных пользователей
    if request.user.is_authenticated:
        UserSession.objects.update_or_create(
            session_key=request.session.session_key,
            defaults={
                'user': request.user,
                'ip_address': get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'last_activity': timezone.now(),
                'is_active': True,
            }
        )
    
    context = {
        'session_data': session_data,
        'cookies': request.COOKIES,
    }
    return render(request, 'lab7/session_info.html', context)

def clear_session(request):
    """Очистка сессии"""
    request.session.flush()
    return redirect('lab7_index')

@login_required
def user_preferences(request):
    """Настройки пользователя (сохраняются в БД)"""
    preferences, created = UserPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preferences.theme = request.POST.get('theme', 'light')
        preferences.language = request.POST.get('language', 'ru')
        preferences.notifications_enabled = 'notifications' in request.POST
        preferences.items_per_page = int(request.POST.get('items_per_page', 10))
        preferences.save()
        
        # Также устанавливаем Cookies для немедленного применения
        response = redirect('lab7_user_preferences')
        response.set_cookie('theme', preferences.theme, max_age=365*24*60*60)
        response.set_cookie('language', preferences.language, max_age=365*24*60*60)
        return response
    
    context = {
        'preferences': preferences,
        'user_sessions': UserSession.objects.filter(user=request.user, is_active=True),
    }
    return render(request, 'lab7/user_preferences.html', context)

def shopping_cart(request):
    """Корзина покупок (работает через сессии для анонимных и через БД для авторизованных)"""
    cart = get_or_create_cart(request)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            product_name = request.POST.get('product_name')
            price = float(request.POST.get('price', 0))
            quantity = int(request.POST.get('quantity', 1))
            
            # Добавляем товар в корзину
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_name=product_name,
                defaults={'price': price, 'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
                
        elif action == 'update':
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))
            
            if quantity > 0:
                CartItem.objects.filter(id=item_id, cart=cart).update(quantity=quantity)
            else:
                CartItem.objects.filter(id=item_id, cart=cart).delete()
                
        elif action == 'remove':
            item_id = request.POST.get('item_id')
            CartItem.objects.filter(id=item_id, cart=cart).delete()
            
        elif action == 'clear':
            cart.items.all().delete()
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all() if cart else [],
        'total_price': cart.get_total_price() if cart else 0,
    }
    return render(request, 'lab7/shopping_cart.html', context)

def cookie_demo(request):
    """Демонстрация работы с Cookies"""
    cookie_data = {}
    
    if request.method == 'POST':
        cookie_name = request.POST.get('cookie_name')
        cookie_value = request.POST.get('cookie_value')
        cookie_age = int(request.POST.get('cookie_age', 3600))
        
        if cookie_name and cookie_value:
            response = redirect('lab7_cookie_demo')
            response.set_cookie(cookie_name, cookie_value, max_age=cookie_age)
            return response
    
    # Собираем информацию о всех Cookies
    for name, value in request.COOKIES.items():
        cookie_data[name] = value
    
    context = {
        'cookies': cookie_data,
    }
    return render(request, 'lab7/cookie_demo.html', context)

def delete_cookie(request, cookie_name):
    """Удаление Cookie"""
    response = redirect('lab7_cookie_demo')
    response.delete_cookie(cookie_name)
    return response

# Вспомогательные функции
def get_or_create_cart(request):
    """Получение или создание корзины"""
    if request.user.is_authenticated:
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart, created = ShoppingCart.objects.get_or_create(
            session_key=session_key,
            user__isnull=True
        )
    
    return cart

def get_client_ip(request):
    """Получение IP адреса клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_preferences(request):
    """Получение настроек пользователя"""
    if request.user.is_authenticated:
        try:
            return UserPreference.objects.get(user=request.user)
        except UserPreference.DoesNotExist:
            return None
    return None