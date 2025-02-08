from django.contrib import admin
from .models import Unit, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, ParchageInvoiceItem, Waste, WasteItem

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'whatsapp_number', 'email_address')

@admin.register(SupplierInvoice)
class SupplierInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_number', 'amount', 'status', 'supplier', 'due', 'due_payment_date', 'created_at', 'updated_at')

@admin.register(SupplierPayment)
class SupplierPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'invoice', 'amount_paid', 'payment_method', 'reference_number', 'created_at', 'updated_at')

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'unit', 'alert_stock', 'sku', 'price', 'stock', 'created_at', 'updated_at')

@admin.register(ParchageInvoiceItem)
class ParchageInvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity', 'supplier_order', 'price', 'created_at', 'updated_at')

@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'responsible', 'note', 'created_at', 'updated_at')

@admin.register(WasteItem)
class WasteItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'waste', 'ingredient', 'quantity', 'loss_amount', 'created_at', 'updated_at')
