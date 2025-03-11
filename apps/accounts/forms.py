
from apps.accounts.models import User, Address, Building
from django import forms

class UserForm(forms.ModelForm):
    id = forms.CharField(required=False)
    
    class Meta:
        model =  User
        fields = [
            'name',
            'gender',
            'date_of_birth',
            'photo',
            'phone',
            'role',
            'is_active'
        ]
class StaffForm(forms.ModelForm):
    id = forms.CharField(required=False)
    is_staff = forms.BooleanField(required=False)
    
    class Meta:
        model =  User
        fields = [
            'name',
            'email',
            'password',
            'gender',
            'date_of_birth',
            'photo',
            'phone',
            'role',
            'is_active',
            'is_staff'
        ]
class AddressForm(forms.ModelForm):
    id = forms.CharField(required=False)
    address_type = forms.CharField(required=False)
    
    class Meta:
        model = Address
        fields = '__all__'       
   
class BuildingForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Building
        fields = '__all__'   
