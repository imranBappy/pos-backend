import graphene

# from .inputObjectTypes import OutletInput
from .forms import OutletForm
from graphene_django.filter import DjangoFilterConnectionField
from .models import Outlet
from apps.base.utils import get_object_by_kwargs
from .objectType import OutletType
from backend.permissions import login_required

class Query(graphene.ObjectType):
    outlet = graphene.Field(OutletType, id=graphene.ID(required=True))
    outlets = graphene.List(OutletType)
    
    def resolve_outlet(self, info, id):
        return get_object_by_kwargs(Outlet, {"id": id})
    
    @login_required
    def resolve_outlets(self, info,):
        print("OKKK")
        return Outlet.objects.all()
