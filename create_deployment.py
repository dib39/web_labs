import os
import shutil
from pathlib import Path

def create_deployment_package():
    """Создает архив для развертывания проекта"""
    exclude_dirs = ['.vscode', '__pycache__', 'venv', '.git', 'migrations']
    exclude_files = ['db.sqlite3', 'create_deployment.py']
    
    package_name = 'django_lab_project'
    
    # Создаем временную папку для упаковки
    temp_dir = Path('deployment_temp')
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # Копируем файлы проекта
    for item in Path('.').iterdir():
        if item.name in exclude_dirs or item.name in exclude_files:
            continue
        if item.is_dir():
            shutil.copytree(item, temp_dir / item.name)
        else:
            shutil.copy2(item, temp_dir / item.name)
    
    # Создаем архив
    shutil.make_archive(package_name, 'zip', temp_dir)
    
    # Удаляем временную папку
    shutil.rmtree(temp_dir)
    
    print(f"Создан архив для развертывания: {package_name}.zip")
    print("Для установки:")
    print("1. Распакуйте архив")
    print("2. Создайте виртуальное окружение: python -m venv venv")
    print("3. Активируйте окружение")
    print("4. Установите зависимости: pip install -r requirements.txt")
    print("5. Примените миграции: python manage.py migrate")
    print("6. Создайте суперпользователя: python manage.py createsuperuser")
    print("7. Запустите сервер: python manage.py runserver")

if __name__ == "__main__":
    create_deployment_package()