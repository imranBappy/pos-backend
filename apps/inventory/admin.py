from django.contrib import admin
from apps.inventory.models import InvoiceConsumption, Unit, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, PurchaseInvoiceItem, Waste, WasteCategory, WasteItem


@admin.register(InvoiceConsumption)
class InvoiceConsumptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_invoice_item')

@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

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
    list_display = ('id',  'invoice', 'amount', 'payment_method',  'created_at', 'updated_at')

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'unit', 'safety_stock', 'sku', 'stock', 'created_at', 'updated_at')

@admin.register(PurchaseInvoiceItem)
class PurchaseInvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity', 'price', 'created_at', 'updated_at')

@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'responsible', 'notes', 'created_at', 'updated_at')

@admin.register(WasteItem)
class WasteItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'waste', 'ingredient', 'quantity', 'loss_amount', 'created_at', 'updated_at')
