import graphene

# from .inputObjectTypes import OutletInput
from .forms import OutletForm
from graphene_django.filter import DjangoFilterConnectionField
from .models import Outlet
from apps.base.utils import get_object_by_kwargs
from .objectType import OutletType
from backend.authentication import isAuthenticated
from apps.accounts.models import  UserRole


class Query(graphene.ObjectType):
    outlet = graphene.Field(OutletType, id=graphene.ID(required=True))
    outlets = DjangoFilterConnectionField(OutletType)
    
    @isAuthenticated([UserRole.ADMIN, UserRole.MANAGER, UserRole.MANAGER, UserRole.CHEF, UserRole.WAITER])
    def resolve_outlet(self, info, id):
        return get_object_by_kwargs(Outlet, {"id": id})
    
    @isAuthenticated([UserRole.ADMIN])
    def resolve_outlets(self, info, **kwargs):
        return Outlet.objects.all()