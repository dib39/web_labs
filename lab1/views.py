from django.http import HttpResponse
from django.shortcuts import render
import socket
import platform

def index(request):
    """Главная страница лабораторной работы"""
    import django
    context = {
        'python_version': platform.python_version(),
        'django_version': django.get_version(),
    }
    return render(request, 'lab1/index.html', context)

def system_info(request):
    """Страница с информацией о системе - аналог диагностики"""
    hostname = socket.gethostname()
    system_info = {
        'hostname': hostname,
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'django_version': __import__('django').get_version(),
    }
    
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Информация о системе</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            table {{ border-collapse: collapse; width: 100%; max-width: 600px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Информация о системе</h1>
        <table>
            <tr><th>Параметр</th><th>Значение</th></tr>
            <tr><td>Имя хоста</td><td>{system_info['hostname']}</td></tr>
            <tr><td>Операционная система</td><td>{system_info['platform']}</td></tr>
            <tr><td>Версия Python</td><td>{system_info['python_version']}</td></tr>
            <tr><td>Версия Django</td><td>{system_info['django_version']}</td></tr>
            <tr><td>Сервер</td><td>Django Development Server</td></tr>
            <tr><td>База данных</td><td>SQLite</td></tr>
        </table>
        <br>
        <a href="/lab1/">Назад к статусу сервера</a>
    </body>
    </html>
    """)