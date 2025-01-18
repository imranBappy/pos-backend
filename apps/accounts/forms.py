
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
class AddressForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Address
        fields = '__all__'       
   
class BuildingForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Building
        fields = '__all__'   
