from django.contrib import admin

# Register your models here.
from .models import Ingredient, Category,Payment, TableBooking, Product, Order, OrderProduct, ExtraFood, Floor, FloorTable


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity', 'product', 'item')
    fields = ('item', 'product', 'quantity')  

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','final_amount')
    search_fields = ['user__email']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id','quantity','price')
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','amount','trx_id')


@admin.register(ExtraFood)
class ExtraFoodAdmin(admin.ModelAdmin):
    list_display = ('id','product','name','price','cooking_time','description','is_active')
    search_fields = ['product__name']


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(FloorTable)
class FloorTableAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'is_booked']


@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ['id','is_active']
