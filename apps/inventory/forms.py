from django import forms
from apps.inventory.models import WasteCategory, Unit, Supplier, SupplierInvoice, SupplierPayment, ItemCategory, Item, PurchaseInvoiceItem, Waste, WasteItem

class WasteCategoryForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = WasteCategory
        fields = "__all__"

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
    due_payment_date = forms.DateField(required=False)
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
    stock = forms.IntegerField(required=False)
    current_stock = forms.IntegerField(required=False)
    class Meta:
        model = Item
        fields = "__all__"

class PurchaseInvoiceItemForm(forms.ModelForm):
    id = forms.CharField(required=False)
    total_quantity=forms.DecimalField(required=False)
    class Meta:
        model = PurchaseInvoiceItem
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
