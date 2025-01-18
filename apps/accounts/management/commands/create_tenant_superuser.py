from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model
from apps.clients.models import Client

class Command(BaseCommand):
    help = 'Create a superuser for a specific tenant'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--schema_name', type=str, help='The schema name of the tenant', required=True)
        parser.add_argument('--email', type=str, help='The email of the superuser', required=True)
        parser.add_argument('--password', type=str, help='The password of the superuser', required=True)

    def handle(self, *args, **kwargs):
        
        # pass
        schema_name = kwargs['schema_name']
        email = kwargs['email']
        password = kwargs['password']

        try:
            tenant = Client.objects.get(schema_name=schema_name)
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Tenant with schema name {schema_name} does not exist'))
            return

        with schema_context(schema_name):
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR(f'User with email {email} already exists'))
            else:
                User.objects.create_superuser(email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully for tenant {schema_name}'))

            
# Example usage:
# python manage.py create_tenant_superuser --schema_name tenant1 --email admin@example.com --password securepassword123
