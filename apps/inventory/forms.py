from django import forms
from apps.inventory.models import Unit, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, ParchageInvoiceItem, Waste, WasteItem

class UnitForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Unit
        fields = "__all__"

class SupplierForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Supplier
        fields = "__all__"

class SupplierInvoiceForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = SupplierInvoice
        fields = "__all__"

class SupplierPaymentForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = SupplierPayment
        fields = "__all__"

class ItemCategoryForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = ItemCategory
        fields = "__all__"

class ItemForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Item
        fields = "__all__"

class ParchageInvoiceItemForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = ParchageInvoiceItem
        fields = "__all__"

class WasteForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Waste
        fields = "__all__"

class WasteItemForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = WasteItem
        fields = "__all__"
