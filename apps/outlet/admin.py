from django.contrib import admin
from .models import Outlet
# Register your models here.

@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email', 
        'name' 
    ]
    search_fields = ('email', 'name')