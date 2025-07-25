from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass')
        phone = os.environ.get('DJANGO_SUPERUSER_PHONE', '254700000000')
        if not User.objects.filter(username=username).exists():
            user = User(username=username, phone_number=phone, is_superuser=True, is_staff=True, is_admin=True)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.')) 