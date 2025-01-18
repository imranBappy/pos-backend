from django.contrib import admin
from .models import Kitchen, KitchenOrder, Printer
# Register your models here.

@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    list_display = ['id','name']
   
@admin.register(KitchenOrder)
class KitchenOrderAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ['id']