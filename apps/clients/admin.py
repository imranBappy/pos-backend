from django.contrib import admin
from django.urls import path
from django.http import HttpResponseNotFound
from django_tenants.admin import TenantAdminMixin
from django.db import connection

from apps.clients.models import Client, Domain
from django_tenants.utils import get_tenant_model, get_public_schema_name
 

class DomainInline(admin.StackedInline):
    model = Domain
    extra = 0

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    inlines = [DomainInline]
    list_display = ('name', 'schema_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        current_schema_name = connection.schema_name
        print("Current schema name: ", current_schema_name)
        print("get_public_schema_name() : ", get_public_schema_name())
        if current_schema_name != get_public_schema_name():
            return HttpResponseNotFound("Custom 404 Not Found Page")
        return qs







