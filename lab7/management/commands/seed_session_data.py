from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lab7.models import UserPreference

class Command(BaseCommand):
    help = 'Add sample session and preference data'

    def handle(self, *args, **options):
        # Создаем тестового пользователя
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        
        # Создаем настройки пользователя
        UserPreference.objects.get_or_create(
            user=user,
            defaults={
                'theme': 'dark',
                'language': 'ru',
                'notifications_enabled': True,
                'items_per_page': 25,
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully added session data'))
        self.stdout.write('Test user: testuser/testpass123')