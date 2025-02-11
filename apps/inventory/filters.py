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
    search = filters.CharFilter(method="filter_search")
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(supplier__supplier_name__icontains=value)|
            Q(supplier__supplier_email__icontains=value)|
            Q(invoice_number__icontains=value) |
            Q(status__icontains=value)|
            Q(amount__icontains=value)
        )
    class Meta:
        model = SupplierInvoice
        fields = "__all__"

class SupplierPaymentFilter(BaseFilterOrderBy):
    reference_number = filters.CharFilter(lookup_expr="icontains", field_name="reference_number")
    search = filters.CharFilter(method="filter_search")
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(supplier__supplier_name__icontains=value)|
            Q(supplier__supplier_email__icontains=value)|
            Q(invoice_number__icontains=value) |
            Q(status__icontains=value)|
            Q(amount__icontains=value)
        )
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
    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) )
    category = filters.NumberFilter(lookup_expr="exact", field_name="category")
    price = filters.NumberFilter(lookup_expr="gte", field_name="price")
    alert_stock = filters.NumberFilter(lookup_expr="exact", field_name="stock")
    stock = filters.NumberFilter(lookup_expr="gte", field_name="stock")
    class Meta:
        model = Item
        fields = "__all__"
    

class ParchageInvoiceItemFilter(BaseFilterOrderBy):
    price = filters.CharFilter(lookup_expr="icontains", field_name="price")
    
    class Meta:
        model = ParchageInvoiceItem
        fields = "__all__"

class WasteFilter(BaseFilterOrderBy):
    search = filters.CharFilter(method="filter_search")
    created_at_start = filters.DateFilter(method='filter_created_at_range', field_name='start')
    created_at_end = filters.DateFilter(method='filter_created_at_range', field_name='end')
    total_loss_amount = filters.NumberFilter(lookup_expr="gte", field_name="total_loss_amount")
    
    class Meta:
        model = Waste
        fields = "__all__"
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(responsible__responsible_name__icontains=value)|
            Q(responsible__responsible_email__icontains=value)|
            Q(note__icontains=value) |
            Q(total_loss_amount__icontains=value) 
        )

class WasteItemFilter(BaseFilterOrderBy):
    quantity = filters.CharFilter(lookup_expr="icontains", field_name="quantity")
    
    class Meta:
        model = WasteItem
        fields = "__all__"
