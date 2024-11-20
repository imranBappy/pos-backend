from typing import Any
from django import forms
from .models import Outlet


class OutletForm(forms.ModelForm):
    class Meta:
        model = Outlet
        fields = "__all__"
