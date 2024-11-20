from .forms import OutletForm

from graphene_django.forms.types import DjangoFormInputObjectType, InputObjectType
import graphene


class OutletInput(DjangoFormInputObjectType):
    class Meta:
        form_class = OutletForm
