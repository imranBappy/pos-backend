from django_filters import rest_framework as filters
from .models import Unit, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, ParchageInvoiceItem, Waste, WasteItem
from django.db.models import Q
from apps.base.filters import BaseFilterOrderBy

class UnitFilter(BaseFilterOrderBy):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    
    class Meta:
        model = Unit
        fields = "__all__"

class SupplierFilter(BaseFilterOrderBy):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    search = filters.CharFilter(method='filter_search')
    class Meta:
        model = Supplier
        fields = "__all__"

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(phone_number__icontains=value) | Q(whatsapp_number__icontains=value) |   Q(email_address__icontains=value) |   Q(address__icontains=value) )
    
class SupplierInvoiceFilter(BaseFilterOrderBy):
    invoice_number = filters.CharFilter(lookup_expr="icontains", field_name="invoice_number")
    
    class Meta:
        model = SupplierInvoice
        fields = "__all__"

class SupplierPaymentFilter(BaseFilterOrderBy):
    reference_number = filters.CharFilter(lookup_expr="icontains", field_name="reference_number")
    
    class Meta:
        model = SupplierPayment
        fields = "__all__"

class ItemCategoryFilter(BaseFilterOrderBy):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = ItemCategory
        fields = "__all__"
        
    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value)|Q(description__icontains=value) )
    
class ItemFilter(BaseFilterOrderBy):
    search = filters.CharFilter(method="filter_search")
    category = filters.NumberFilter(lookup_expr="exact", field_name="category")
    price = filters.NumberFilter(lookup_expr="gte", field_name="price")
    alert_stock = filters.CharFilter(lookup_expr="exact", field_name="stock")
    stock = filters.NumberFilter(lookup_expr="gte", field_name="stock")
    class Meta:
        model = Item
        fields = "__all__"
    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value)|Q(description__icontains=value) )

class ParchageInvoiceItemFilter(BaseFilterOrderBy):
    price = filters.CharFilter(lookup_expr="icontains", field_name="price")
    
    class Meta:
        model = ParchageInvoiceItem
        fields = "__all__"

class WasteFilter(BaseFilterOrderBy):
    note = filters.CharFilter(lookup_expr="icontains", field_name="note")
    
    class Meta:
        model = Waste
        fields = "__all__"

class WasteItemFilter(BaseFilterOrderBy):
    quantity = filters.CharFilter(lookup_expr="icontains", field_name="quantity")
    
    class Meta:
        model = WasteItem
        fields = "__all__"
