from django.core.management.base import BaseCommand
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Create a superuser with default credentials'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='The email of the superuser', required=True)
        parser.add_argument('--password', type=str, help='The password of the superuser', required=True)
    
    def handle(self, *args, **kwargs):
        email = kwargs['email']
        password = kwargs['password']

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password, name='admin')
            self.stdout.write(self.style.SUCCESS(f'Superuser "{email}" created successfully!'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{email}" already exists.'))
