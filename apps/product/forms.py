from django import forms
from  apps.product.models import Ingredient, Coupon, Product, Category, Order, OrderProduct, FloorTable,Floor, Payment



class IngredientForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Ingredient
        fields = '__all__'

class ProductForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Product
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Category
        fields = '__all__'
        

class OrderForm(forms.ModelForm):
    id = forms.CharField(required=False)
    table_bookings = forms.CharField(required=False)
    class Meta:
        model = Order
        fields = '__all__'

class OrderProductForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = OrderProduct
        fields = '__all__'


class FloorForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Floor
        fields = '__all__'
    
class FloorTableForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = FloorTable
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Payment
        fields = '__all__'       
        

    
class CouponForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Coupon
        fields = '__all__'