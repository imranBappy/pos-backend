from django.utils.deprecation import MiddlewareMixin
from apps.clients.models import Client as Tenant

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        
        # Fallback for missing tenant
        try:
            hostname = request.get_host().split(':')[0].lower()
            schema_name = hostname.split('.')[0]
            tenant_name  = Tenant.objects.get(schema_name='tenant1')
            request.tenant = tenant_name
        except Tenant.DoesNotExist:
            request.tenant = None  # Handle cases with no tenant gracefully
        except Exception as e:
            request.tenant = None
            # Optionally log the error for debugging
            print(f"Error in TenantMiddleware: {e}")
