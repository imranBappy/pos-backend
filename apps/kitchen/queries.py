import graphene

from .models import Kitchen
from apps.base.utils import get_object_by_kwargs
from .objectType import KitchenType


class Query(graphene.ObjectType):
    kitchen = graphene.Field(KitchenType, id=graphene.ID(required=True))
    kitchens = graphene.List(KitchenType)
    
    def resolve_kitchen(self, info, id):
        return get_object_by_kwargs(Kitchen, {"id": id})
    
    def resolve_kitchens(self, info):
        return Kitchen.objects.all()
